"""Orpheus LoRA local TTS backend using generation + SNAC decode."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import soundfile as sf
import torch
from snac import SNAC
from transformers import AutoModelForCausalLM, AutoTokenizer


DEFAULT_ORPHEUS_MODEL_ID = os.getenv("TTS_ORPHEUS_MODEL_ID", "griffing52/orpheus-swiss-german-lora")
DEFAULT_ORPHEUS_BASE_MODEL = os.getenv("TTS_ORPHEUS_BASE_MODEL", "")
DEFAULT_ORPHEUS_TOKENIZER_ID = os.getenv("TTS_ORPHEUS_TOKENIZER_ID", "")
DEFAULT_HF_TOKEN = os.getenv("HF_TOKEN", "")
DEFAULT_SNAC_MODEL_ID = os.getenv("TTS_ORPHEUS_SNAC_MODEL_ID", "hubertsiuzdak/snac_24khz")
DEFAULT_TARGET_SR = int(os.getenv("TTS_ORPHEUS_TARGET_SR", "24000"))

SOH_TOKEN = 128259
EOT_TOKEN = 128009
EOH_TOKEN = 128260
SOA_TOKEN = 128257
EOA_TOKEN = 128258
SPEECH_TOKEN_BASE = 128266


def _resolve_device() -> str:
    configured = os.getenv("TTS_ORPHEUS_DEVICE", "auto").strip().lower()
    if configured in {"cuda", "cpu"}:
        return configured
    return "cuda" if torch.cuda.is_available() else "cpu"


def _resolve_dtype(device: str) -> torch.dtype:
    configured = os.getenv("TTS_ORPHEUS_DTYPE", "auto").strip().lower()
    if configured == "bf16":
        return torch.bfloat16
    if configured == "fp16":
        return torch.float16
    if configured == "fp32":
        return torch.float32

    if device == "cuda":
        if torch.cuda.is_bf16_supported():
            return torch.bfloat16
        return torch.float16
    return torch.float32


def _load_model_and_tokenizer(
    *,
    model_id: str,
    api_token: str | None,
    dtype: torch.dtype,
    device: str,
):
    tokenizer_id = DEFAULT_ORPHEUS_TOKENIZER_ID or model_id
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_id, token=api_token)

    base_model_id = DEFAULT_ORPHEUS_BASE_MODEL.strip()
    if base_model_id:
        from peft import PeftModel

        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            torch_dtype=dtype,
            token=api_token,
        )
        if device == "cuda":
            base_model = base_model.to(device)
        model = PeftModel.from_pretrained(base_model, model_id, token=api_token)
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=dtype,
            token=api_token,
        )
        if device == "cuda":
            model = model.to(device)

    model.eval()
    return model, tokenizer


def _load_snac_model(device: str):
    snac_model = SNAC.from_pretrained(DEFAULT_SNAC_MODEL_ID)
    snac_model = snac_model.to(device)
    snac_model.eval()
    return snac_model


_MODEL_CACHE: dict[tuple[str, str, str], tuple[Any, Any]] = {}
_SNAC_CACHE: dict[str, Any] = {}


def load_model(
    *,
    model_id: str | None = None,
    api_token: str | None = None,
    endpoint_url: str | None = None,
    voice: str | None = None,
    language: str | None = None,
    **_: Any,
) -> dict[str, str]:
    """Preload Orpheus model, tokenizer, and SNAC decoder into cache."""
    resolved_model = model_id or endpoint_url or DEFAULT_ORPHEUS_MODEL_ID
    resolved_token = api_token or DEFAULT_HF_TOKEN or None

    if not resolved_model:
        raise ValueError("Orpheus model id must be configured")

    device = _resolve_device()
    dtype = _resolve_dtype(device)
    _get_model_and_tokenizer(
        model_id=resolved_model,
        api_token=resolved_token,
        dtype=dtype,
        device=device,
    )
    _get_snac(device)

    return {
        "status": "loaded",
        "model_id": resolved_model,
        "device": device,
        "dtype": str(dtype),
        "voice": voice or "",
        "language": language or "",
    }


def _get_model_and_tokenizer(model_id: str, api_token: str | None, dtype: torch.dtype, device: str):
    cache_key = (model_id, str(dtype), device)
    if cache_key not in _MODEL_CACHE:
        _MODEL_CACHE[cache_key] = _load_model_and_tokenizer(
            model_id=model_id,
            api_token=api_token,
            dtype=dtype,
            device=device,
        )
    return _MODEL_CACHE[cache_key]


def _get_snac(device: str):
    if device not in _SNAC_CACHE:
        _SNAC_CACHE[device] = _load_snac_model(device)
    return _SNAC_CACHE[device]


def _build_input_ids(prompt: str, tokenizer, device: str):
    prompt_ids = tokenizer(prompt, return_tensors="pt").input_ids
    start_token = torch.tensor([[SOH_TOKEN]], dtype=torch.int64)
    end_tokens = torch.tensor([[EOT_TOKEN, EOH_TOKEN]], dtype=torch.int64)
    modified_input_ids = torch.cat([start_token, prompt_ids, end_tokens], dim=1)
    attention_mask = torch.ones_like(modified_input_ids)
    return modified_input_ids.to(device), attention_mask.to(device)


def _extract_speech_tokens(generated_ids: torch.Tensor) -> list[int]:
    row = generated_ids[0]
    soa_positions = (row == SOA_TOKEN).nonzero(as_tuple=True)[0]
    if len(soa_positions) > 0:
        row = row[soa_positions[-1].item() + 1 :]

    row = row[row != EOA_TOKEN]
    if row.numel() == 0:
        raise RuntimeError("Generated output contains no speech tokens")

    trimmed = row[: (row.numel() // 7) * 7]
    if trimmed.numel() == 0:
        raise RuntimeError("Generated speech token sequence is too short")

    return [int(token.item()) - SPEECH_TOKEN_BASE for token in trimmed]


def _decode_with_snac(code_list: list[int], snac_model, device: str) -> torch.Tensor:
    n = len(code_list) // 7
    layer_1: list[int] = []
    layer_2: list[int] = []
    layer_3: list[int] = []

    for i in range(n):
        layer_1.append(code_list[7 * i])
        layer_2.append(code_list[7 * i + 1] - 4096)
        layer_3.append(code_list[7 * i + 2] - (2 * 4096))
        layer_3.append(code_list[7 * i + 3] - (3 * 4096))
        layer_2.append(code_list[7 * i + 4] - (4 * 4096))
        layer_3.append(code_list[7 * i + 5] - (5 * 4096))
        layer_3.append(code_list[7 * i + 6] - (6 * 4096))

    codes = [
        torch.tensor(layer_1, dtype=torch.long, device=device).unsqueeze(0),
        torch.tensor(layer_2, dtype=torch.long, device=device).unsqueeze(0),
        torch.tensor(layer_3, dtype=torch.long, device=device).unsqueeze(0),
    ]
    return snac_model.decode(codes)


def generate_audio(
    text: str,
    output_path: str | os.PathLike[str] = "output.wav",
    *,
    model_id: str | None = None,
    api_token: str | None = None,
    endpoint_url: str | None = None,
    voice: str | None = None,
    language: str | None = None,
    **options: Any,
) -> str:
    """Generate speech locally using Orpheus text generation and SNAC decode."""
    resolved_model = model_id or endpoint_url or DEFAULT_ORPHEUS_MODEL_ID
    resolved_token = api_token or DEFAULT_HF_TOKEN or None

    if not resolved_model:
        raise ValueError("Orpheus model id must be configured")

    if language:
        # Language is currently handled via prompt content/voice convention.
        options.setdefault("language", language)

    prompt = f"{voice}: {text}" if voice else text
    device = _resolve_device()
    dtype = _resolve_dtype(device)

    model, tokenizer = _get_model_and_tokenizer(
        model_id=resolved_model,
        api_token=resolved_token,
        dtype=dtype,
        device=device,
    )
    snac_model = _get_snac(device)

    input_ids, attention_mask = _build_input_ids(prompt, tokenizer, device)

    generation_defaults = {
        "max_new_tokens": int(os.getenv("TTS_ORPHEUS_MAX_NEW_TOKENS", "1200")),
        "do_sample": True,
        "temperature": float(os.getenv("TTS_ORPHEUS_TEMPERATURE", "0.6")),
        "top_p": float(os.getenv("TTS_ORPHEUS_TOP_P", "0.95")),
        "repetition_penalty": float(os.getenv("TTS_ORPHEUS_REPETITION_PENALTY", "1.1")),
        "num_return_sequences": 1,
        "eos_token_id": EOA_TOKEN,
    }
    generation_defaults.update(options)

    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            **generation_defaults,
        )

    code_list = _extract_speech_tokens(generated_ids)
    audio_hat = _decode_with_snac(code_list, snac_model, device)

    audio_np = audio_hat.detach().squeeze().to("cpu").numpy()

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output_file, audio_np, DEFAULT_TARGET_SR)
    return str(output_file)

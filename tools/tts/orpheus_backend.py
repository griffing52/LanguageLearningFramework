"""Orpheus LoRA TTS backend using Hugging Face Inference API."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from huggingface_hub import InferenceClient


DEFAULT_ORPHEUS_MODEL_ID = os.getenv("TTS_ORPHEUS_MODEL_ID", "griffing52/orpheus-swiss-german-lora")
DEFAULT_HF_TOKEN = os.getenv("HF_TOKEN", "")


def _collect_bytes(response: Any) -> bytes:
    if isinstance(response, (bytes, bytearray)):
        return bytes(response)
    if hasattr(response, "read"):
        return response.read()
    if isinstance(response, str):
        return response.encode("utf-8")
    return b"".join(chunk for chunk in response)


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
    """Generate speech using the Orpheus LoRA model through Hugging Face inference."""
    resolved_model = endpoint_url or model_id or DEFAULT_ORPHEUS_MODEL_ID
    resolved_token = api_token or DEFAULT_HF_TOKEN or None

    if not resolved_model:
        raise ValueError("Orpheus model id or endpoint_url must be configured")

    client = InferenceClient(token=resolved_token)

    generation_options = dict(options)
    if voice:
        generation_options["voice"] = voice
    if language:
        generation_options["language"] = language

    response = client.text_to_speech(text=text, model=resolved_model, **generation_options)
    audio_bytes = _collect_bytes(response)
    if not audio_bytes:
        raise RuntimeError("Orpheus backend returned no audio data")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(audio_bytes)
    return str(output_file)

"""SpeechT5 TTS backend implementation."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import soundfile as sf
import torch
from transformers import SpeechT5ForTextToSpeech, SpeechT5HifiGan, SpeechT5Processor

from .helper import format_text


DEFAULT_CHECKPOINT = os.getenv("TTS_SPEECHT5_CHECKPOINT", "microsoft/speecht5_tts")
DEFAULT_MODEL_NAME = os.getenv(
    "TTS_SPEECHT5_MODEL",
    "griffing52/speecht5_finetuned_griffin_ch_lu",
)
DEFAULT_VOCODER_NAME = os.getenv("TTS_SPEECHT5_VOCODER", "microsoft/speecht5_hifigan")
DEFAULT_SAMPLE_RATE = int(os.getenv("TTS_SPEECHT5_SAMPLE_RATE", "16000"))
DEFAULT_SPEAKER_EMBEDDINGS_PATH = os.getenv("TTS_SPEAKER_EMBEDDINGS_PATH")


@lru_cache(maxsize=4)
def _load_components(checkpoint: str, model_name: str, vocoder_name: str):
    processor = SpeechT5Processor.from_pretrained(checkpoint)
    model = SpeechT5ForTextToSpeech.from_pretrained(model_name)
    vocoder = SpeechT5HifiGan.from_pretrained(vocoder_name)
    return processor, model, vocoder


def load_model(
    *,
    checkpoint: str | None = None,
    model_name: str | None = None,
    vocoder_name: str | None = None,
    speaker_embeddings_path: str | None = None,
) -> dict[str, str]:
    """Preload SpeechT5 components and speaker embeddings into cache."""
    resolved_checkpoint = checkpoint or DEFAULT_CHECKPOINT
    resolved_model_name = model_name or DEFAULT_MODEL_NAME
    resolved_vocoder_name = vocoder_name or DEFAULT_VOCODER_NAME
    embeddings_path = _resolve_path(speaker_embeddings_path, DEFAULT_SPEAKER_EMBEDDINGS_PATH)

    if not embeddings_path.exists():
        raise FileNotFoundError(f"Speaker embeddings file not found: {embeddings_path}")

    _load_components(resolved_checkpoint, resolved_model_name, resolved_vocoder_name)
    _load_speaker_embeddings(str(embeddings_path))
    return {
        "status": "loaded",
        "checkpoint": resolved_checkpoint,
        "model_name": resolved_model_name,
        "vocoder_name": resolved_vocoder_name,
        "speaker_embeddings_path": str(embeddings_path),
    }


@lru_cache(maxsize=2)
def _load_speaker_embeddings(embeddings_path: str):
    return torch.load(embeddings_path, map_location="cpu")


def _resolve_path(candidate: str | None, fallback_env: str | None = None) -> Path:
    if candidate:
        return Path(candidate)
    if fallback_env:
        return Path(fallback_env)
    raise ValueError(
        "speaker_embeddings_path must be provided explicitly or via TTS_SPEAKER_EMBEDDINGS_PATH"
    )


def generate_audio(
    text: str,
    output_path: str | os.PathLike[str] = "output.wav",
    *,
    checkpoint: str | None = None,
    model_name: str | None = None,
    vocoder_name: str | None = None,
    speaker_embeddings_path: str | None = None,
    sample_rate: int | None = None,
    **_: Any,
) -> str:
    """Generate audio from text and save it to the requested path."""
    resolved_checkpoint = checkpoint or DEFAULT_CHECKPOINT
    resolved_model_name = model_name or DEFAULT_MODEL_NAME
    resolved_vocoder_name = vocoder_name or DEFAULT_VOCODER_NAME
    resolved_sample_rate = sample_rate or DEFAULT_SAMPLE_RATE
    embeddings_path = _resolve_path(speaker_embeddings_path, DEFAULT_SPEAKER_EMBEDDINGS_PATH)

    if not embeddings_path.exists():
        raise FileNotFoundError(f"Speaker embeddings file not found: {embeddings_path}")

    final_text = format_text(text)
    processor, model, vocoder = _load_components(resolved_checkpoint, resolved_model_name, resolved_vocoder_name)
    speaker_embeddings = _load_speaker_embeddings(str(embeddings_path))

    inputs = processor(text=final_text, return_tensors="pt")
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output_file, speech.numpy(), resolved_sample_rate)
    return str(output_file)

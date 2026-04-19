"""Compatibility wrapper for the SpeechT5 backend."""

from __future__ import annotations

from .speecht5_backend import generate_audio as _generate_audio


def generate_audio(text, output_path="output.wav", **options):
    """Generate SpeechT5 audio and write it to ``output_path``."""
    return _generate_audio(text, output_path=output_path, **options)


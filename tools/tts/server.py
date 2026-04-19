"""Standalone TTS server for remote inference execution.

Run this service on a dedicated inference machine and register it as a provider
in the platform API. It supports method-level dispatch to local backends.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backends import (
    LEGACY_STITCHED_METHOD,
    ORPHEUS_LORA_METHOD,
    SPEECHT5_METHOD,
    is_local_method,
    load_local_backend,
    normalize_method,
)


SERVER_HOST = os.getenv("TTS_SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("TTS_SERVER_PORT", "7001"))
SERVER_OUTPUT_DIR = Path(os.getenv("TTS_SERVER_OUTPUT_DIR", "./output"))
SERVER_DEFAULT_METHOD = normalize_method(os.getenv("TTS_SERVER_DEFAULT_METHOD", SPEECHT5_METHOD))
SERVER_RETURN_AUDIO_BASE64 = os.getenv("TTS_SERVER_RETURN_AUDIO_BASE64", "true").lower() == "true"


class TtsSynthesizeRequest(BaseModel):
    text: str = Field(..., min_length=1)
    tts_method: str = Field(default=SERVER_DEFAULT_METHOD)
    language: str | None = None
    voice: str | None = None
    options: dict[str, Any] = Field(default_factory=dict)


app = FastAPI(title="LanguageLearningFramework TTS Server", version="0.1.0")


def _method_defaults(method: str) -> dict[str, Any]:
    if method == SPEECHT5_METHOD:
        return {
            "speaker_embeddings_path": os.getenv("TTS_SPEECHT5_SPEAKER_EMBEDDINGS", ""),
            "checkpoint": os.getenv("TTS_SPEECHT5_CHECKPOINT", ""),
            "model_name": os.getenv("TTS_SPEECHT5_MODEL", ""),
            "vocoder_name": os.getenv("TTS_SPEECHT5_VOCODER", ""),
        }

    if method == LEGACY_STITCHED_METHOD:
        return {
            "legacy_root": os.getenv("TTS_LEGACY_ROOT", ""),
            "mode": os.getenv("TTS_LEGACY_MODE", "stitched"),
        }

    if method == ORPHEUS_LORA_METHOD:
        return {
            "model_id": os.getenv("TTS_ORPHEUS_MODEL_ID", "griffing52/orpheus-swiss-german-lora"),
            "api_token": os.getenv("HF_TOKEN", ""),
            "endpoint_url": os.getenv("TTS_ORPHEUS_ENDPOINT_URL", ""),
        }

    return {}


def _clean_options(options: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in options.items() if value not in (None, "")}


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "host": SERVER_HOST,
        "port": SERVER_PORT,
        "default_method": SERVER_DEFAULT_METHOD,
    }


@app.get("/methods")
def methods() -> dict[str, Any]:
    return {
        "methods": [SPEECHT5_METHOD, LEGACY_STITCHED_METHOD, ORPHEUS_LORA_METHOD],
        "default_method": SERVER_DEFAULT_METHOD,
    }


@app.post("/synthesize")
def synthesize(request: TtsSynthesizeRequest) -> dict[str, Any]:
    method = normalize_method(request.tts_method)
    if not is_local_method(method):
        raise HTTPException(status_code=400, detail=f"Unsupported method '{request.tts_method}'")

    try:
        backend = load_local_backend(method)
    except Exception as err:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(err)) from err

    options = _method_defaults(method)
    options.update(request.options or {})
    options = _clean_options(options)
    if request.language:
        options.setdefault("language", request.language)
    if request.voice:
        options.setdefault("voice", request.voice)

    SERVER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_format = str(options.pop("output_format", "wav")).lstrip(".") or "wav"
    output_file = SERVER_OUTPUT_DIR / f"tts_{method}_{abs(hash(request.text))}.{output_format}"

    try:
        audio_path = backend.generate_audio(request.text, output_path=output_file, **options)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {err}") from err

    response: dict[str, Any] = {
        "status": "success",
        "tts_method": method,
        "audio_file": str(audio_path),
    }

    if SERVER_RETURN_AUDIO_BASE64:
        audio_bytes = Path(audio_path).read_bytes()
        response["audio_base64"] = base64.b64encode(audio_bytes).decode("ascii")

    return response

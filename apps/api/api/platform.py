"""
Platform API routes for cohesive management across vocabulary, lessons, and TTS providers.
"""

from fastapi import APIRouter, HTTPException

from core.models import (
    CreateLessonRequest,
    CreatePhraseRequest,
    CreateWordRequest,
    TtsInferenceRequest,
    TtsProviderConfig,
)
from services.platform_service import PlatformService

router = APIRouter(prefix="/api/platform", tags=["platform"])
service = PlatformService()


@router.get("/status", response_model=dict)
async def get_status():
    """Get cross-module platform status."""
    return service.get_platform_status()


@router.post("/words", response_model=dict)
async def create_word(payload: CreateWordRequest):
    """Create a word and persist it to seed storage."""
    try:
        created = service.add_word(payload)
        return {"status": "success", "word": created}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.post("/phrases", response_model=dict)
async def create_phrase(payload: CreatePhraseRequest):
    """Create a phrase and persist it to seed storage."""
    try:
        created = service.add_phrase(payload)
        return {"status": "success", "phrase": created}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.get("/lessons", response_model=list)
async def list_lessons():
    """List user-defined lessons."""
    return service.list_lessons()


@router.post("/lessons", response_model=dict)
async def create_lesson(payload: CreateLessonRequest):
    """Create a user-defined lesson linking existing words and phrases."""
    try:
        lesson = service.create_lesson(payload)
        return {"status": "success", "lesson": lesson}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.get("/tts/providers", response_model=dict)
async def get_tts_providers():
    """List configured TTS providers."""
    return service.list_tts_providers()


@router.post("/tts/providers", response_model=dict)
async def upsert_tts_provider(payload: TtsProviderConfig):
    """Create or update a TTS provider entry."""
    try:
        result = service.upsert_tts_provider(payload)
        return {"status": "success", "config": result}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.post("/tts/providers/{provider_id}/default", response_model=dict)
async def set_default_provider(provider_id: str):
    """Set default TTS provider."""
    try:
        result = service.set_default_provider(provider_id)
        return {"status": "success", "config": result}
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.post("/tts/infer", response_model=dict)
async def run_tts_inference(payload: TtsInferenceRequest):
    """Forward TTS inference request to configured provider endpoint."""
    try:
        return service.run_tts_inference(payload)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except RuntimeError as err:
        raise HTTPException(status_code=502, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err

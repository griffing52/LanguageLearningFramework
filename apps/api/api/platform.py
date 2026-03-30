"""
Platform API routes for cohesive management across vocabulary, lessons, and TTS providers.
"""

from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

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


@router.post("/import/words", response_model=dict)
async def import_words(file: UploadFile = File(...), mode: str = Form("replace")):
    """Upload a word list file in CLI format and import into seed storage."""
    try:
        content = await file.read()
        result = service.import_words(content=content, mode=mode)
        return {"status": "success", "result": result}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.post("/import/phrases", response_model=dict)
async def import_phrases(file: UploadFile = File(...), mode: str = Form("replace")):
    """Upload a phrase list file in CLI format and import into seed storage."""
    try:
        content = await file.read()
        result = service.import_phrases(content=content, mode=mode)
        return {"status": "success", "result": result}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.post("/import/memory", response_model=dict)
async def import_memory(file: UploadFile = File(...), mode: str = Form("replace")):
    """Upload a memory file in JSON or key|frequency format."""
    try:
        content = await file.read()
        result = service.import_memory(content=content, mode=mode)
        return {"status": "success", "result": result}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.post("/memory/save", response_model=dict)
async def save_memory_state(export_file_name: Optional[str] = Query(default=None)):
    """Persist current in-memory frequencies and optionally export to an additional state file."""
    try:
        result = service.save_memory_state(export_file_name=export_file_name)
        return {"status": "success", "result": result}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.post("/clear", response_model=dict)
async def clear_dataset(target: str = Query(..., description="words|phrases|memory|all")):
    """Clear one or more platform datasets."""
    try:
        result = service.clear_dataset(target=target)
        return {"status": "success", "result": result}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.get("/statistics", response_model=dict)
async def get_teaching_statistics(top_n: int = Query(10, ge=1, le=50)):
    """Get aggregate and top-item teaching statistics for words and phrases."""
    return service.get_teaching_statistics(top_n=top_n)

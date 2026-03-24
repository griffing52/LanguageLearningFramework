"""
Audio serving API routes.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from services.audio_service import AudioService

router = APIRouter(prefix="/api/audio", tags=["audio"])
service = AudioService()


@router.get("/{filename}")
async def get_audio(filename: str):
    """
    Serve audio file by filename.
    """
    file_path = service.get_audio_file(filename)
    
    if not file_path:
        raise HTTPException(status_code=404, detail=f"Audio file '{filename}' not found")
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=filename
    )


@router.get("", response_model=dict)
async def list_audio_files(limit: int = 100):
    """
    List available audio files.
    """
    files = service.list_audio_files(limit=limit)
    return {
        "files": files,
        "count": len(files)
    }


@router.get("/stats", response_model=dict)
async def get_audio_stats():
    """
    Get statistics about audio library.
    """
    return service.get_audio_stats()

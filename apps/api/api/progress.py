"""
Progress reporting API routes.
"""

from fastapi import APIRouter
from core.models import ProgressSnapshot
from services.progress_service import ProgressService

router = APIRouter(prefix="/api/progress", tags=["progress"])
service = ProgressService()


@router.get("/snapshot", response_model=ProgressSnapshot)
async def get_progress_snapshot():
    """
    Get current learning progress snapshot.
    """
    return service.get_progress_snapshot()


@router.get("/detailed", response_model=dict)
async def get_detailed_progress():
    """
    Get detailed progress report with breakdowns.
    """
    return service.get_detailed_progress()

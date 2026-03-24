"""
Study session API routes.
"""

from fastapi import APIRouter, HTTPException, Query
from core.models import StudyTarget, StudyFeedback
from services.study_service import StudyService

router = APIRouter(prefix="/api/study", tags=["study"])
service = StudyService()


@router.get("/next", response_model=list)
async def get_next_study_targets(batch_size: int = Query(5, ge=1, le=20)):
    """
    Get next recommended items to study.
    Uses spaced repetition algorithm for optimal learning.
    """
    return service.get_study_recommendation(batch_size=batch_size)


@router.post("/feedback", response_model=dict)
async def submit_study_feedback(feedback: StudyFeedback):
    """
    Submit feedback on a studied item.
    Updates frequency and calculates next recommendation.
    """
    success = service.record_feedback(feedback)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to record feedback")
    
    return {
        "status": "success",
        "message": "Feedback recorded",
        "next_batch": service.get_study_recommendation(batch_size=1)
    }


@router.get("/lesson", response_model=list)
async def get_lesson_plan(lesson_size: int = Query(10, ge=1, le=30)):
    """
    Get a full lesson plan with multiple study items.
    """
    return service.get_lesson_plan(lesson_count=lesson_size)

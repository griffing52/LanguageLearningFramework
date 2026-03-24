"""
Progress service - tracks and reports learning progress.
"""

from datetime import datetime
from typing import Optional
from core.models import ProgressSnapshot
from data_access.repository import get_repository
from utils.logger import get_logger

logger = get_logger(__name__)


class ProgressService:
    """Service layer for progress tracking."""
    
    def __init__(self):
        """Initialize with repository access."""
        self.repo = get_repository()
    
    def get_progress_snapshot(self) -> ProgressSnapshot:
        """
        Get current learning progress snapshot.
        
        Returns:
            ProgressSnapshot with overall statistics
        """
        stats = self.repo.get_all_stats()
        
        return ProgressSnapshot(
            total_words=stats["total_words"],
            words_learned=stats["words_learned"],
            total_phrases=stats["total_phrases"],
            phrases_learned=stats["phrases_learned"],
            average_complexity=stats["average_complexity"],
            session_count=0,  # TODO: Implement session tracking
            last_session_time=None  # TODO: Implement session history
        )
    
    def get_detailed_progress(self) -> dict:
        """
        Get detailed progress report.
        
        Returns:
            Dict with comprehensive progress metrics
        """
        stats = self.repo.get_all_stats()
        
        return {
            "vocabulary": {
                "total_words": stats["total_words"],
                "words_learned": stats["words_learned"],
                "words_percentage": (
                    round(stats["words_learned"] / stats["total_words"] * 100, 1)
                    if stats["total_words"] > 0
                    else 0
                ),
                "words_remaining": stats["total_words"] - stats["words_learned"]
            },
            "phrases": {
                "total_phrases": stats["total_phrases"],
                "phrases_learned": stats["phrases_learned"],
                "phrases_percentage": (
                    round(stats["phrases_learned"] / stats["total_phrases"] * 100, 1)
                    if stats["total_phrases"] > 0
                    else 0
                ),
                "phrases_remaining": stats["total_phrases"] - stats["phrases_learned"]
            },
            "overall": {
                "total_items": stats["total_items"],
                "items_learned": stats["items_learned"],
                "items_percentage": (
                    round(stats["items_learned"] / stats["total_items"] * 100, 1)
                    if stats["total_items"] > 0
                    else 0
                ),
                "average_complexity": stats["average_complexity"]
            },
            "milestones": self._calculate_milestones(stats)
        }
    
    def _calculate_milestones(self, stats: dict) -> dict:
        """Calculate achievement milestones."""
        return {
            "first_words": stats["words_learned"] >= 10,
            "first_phrases": stats["phrases_learned"] >= 5,
            "quarter_vocabulary": stats["words_learned"] >= int(stats["total_words"] * 0.25),
            "half_vocabulary": stats["words_learned"] >= int(stats["total_words"] * 0.5),
            "nearly_done": stats["words_learned"] >= int(stats["total_words"] * 0.9),
        }

"""
Study service - business logic for study session planning and feedback.
Recommends words/phrases for study based on spaced repetition heuristics.
"""

import random
from typing import List, Optional
from datetime import datetime
import json
from core.models import StudyTarget, StudyFeedback, PhraseDTO, WordDTO
from core.constants import (
    FREQUENCY_THRESHOLD_LEARNED,
    AGE_THRESHOLD_URGENT,
    COMPLEXITY_MIN,
    COMPLEXITY_MAX
)
from data_access.repository import get_repository
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class StudyService:
    """Service layer for study session management and planning."""
    
    def __init__(self):
        """Initialize with repository access."""
        self.repo = get_repository()
    
    def get_study_recommendation(self, batch_size: int = 5) -> List[StudyTarget]:
        """
        Get next items to study using spaced repetition heuristics.
        
        Scoring logic:
        - Items with frequency == 0 get highest priority
        - Items with age > AGE_THRESHOLD_URGENT get boosted
        - Lower complexity gets slight priority (easier wins for motivation)
        - Random selection within scored bucket for variety
        
        Args:
            batch_size: Number of recommendations to return
        
        Returns:
            List of StudyTarget objects ordered by urgency
        """
        words = self.repo.get_all_words()
        phrases = self.repo.get_all_phrases()
        
        # Build candidate pool with urgency scores
        candidates = []
        
        for word in words:
            score = self._calculate_urgency_score(
                frequency=word.frequency,
                age=word.age,
                complexity=word.complexity,
                is_phrase=False
            )
            candidates.append({
                "target": word,
                "target_type": "word",
                "score": score
            })
        
        for phrase in phrases:
            score = self._calculate_urgency_score(
                frequency=phrase.frequency,
                age=phrase.age,
                complexity=phrase.complexity,
                is_phrase=True
            )
            candidates.append({
                "target": phrase,
                "target_type": "phrase",
                "score": score
            })
        
        # Sort by score (descending) and shuffle within score tiers
        candidates.sort(key=lambda x: x["score"], reverse=True)
        
        # Build results
        results = []
        for i, candidate in enumerate(candidates[:batch_size * 3]):  # Oversample for randomization
            target = candidate["target"]
            target_type = candidate["target_type"]
            
            study_target = StudyTarget(
                target_id=f"{target_type}-{target.value}",
                target_type=target_type,
                target_value=target.value,
                target_translation=target.translation,
                urgency_score=min(1.0, candidate["score"]),  # Normalize to 0-1
                reason=self._get_urgency_reason(
                    frequency=target.frequency,
                    age=target.age,
                    complexity=target.complexity
                ),
                audio_url=f"/api/audio/{target_type}-{target.value}.mp3"
            )
            results.append(study_target)
        
        # Final shuffle and truncate
        random.shuffle(results)
        return results[:batch_size]
    
    def _calculate_urgency_score(
        self,
        frequency: int,
        age: int,
        complexity: int,
        is_phrase: bool = False
    ) -> float:
        """
        Calculate urgency score for an item.
        Higher scores = more urgent to study.
        """
        score = 0.0
        
        # Never-studied items get priority
        if frequency == 0:
            score += 100.0
        else:
            # Studied items: boost if they need review
            score += frequency ** -1  # Invert: lower frequency = higher score
        
        # Age-based boost (items not studied recently)
        if age > AGE_THRESHOLD_URGENT:
            score += age * 0.5  # Significant boost for old items
        else:
            score += age * 0.1  # Small boost for recently studied
        
        # Complexity adjustment (slight preference for simpler items)
        complexity_factor = (COMPLEXITY_MAX - complexity) / COMPLEXITY_MAX
        score += complexity_factor * 5.0
        
        # Phrase bonus (phrases are often worth prioritizing)
        if is_phrase:
            score += 10.0
        
        return score
    
    def _get_urgency_reason(self, frequency: int, age: int, complexity: int) -> str:
        """Generate human-readable reason for selection."""
        if frequency == 0:
            return "Never studied"
        elif age > AGE_THRESHOLD_URGENT:
            return f"Needs review (age: {age} sessions)"
        elif frequency == 1:
            return "New, needs reinforcement"
        else:
            return f"Regular review (frequency: {frequency})"
    
    def record_feedback(self, feedback: StudyFeedback) -> bool:
        """
        Record study feedback and update item frequency.
        
        Args:
            feedback: StudyFeedback object with results
        
        Returns:
            True if feedback was recorded successfully
        """
        try:
            target_id = feedback.target_id  # Format: "word-value" or "phrase-value"
            item_type, item_value = target_id.split("-", 1)
            
            # Get current item
            if item_type == "word":
                item = self.repo.get_word(item_value)
            elif item_type == "phrase":
                item = self.repo.get_phrase(item_value)
            else:
                logger.warning(f"Unknown item type: {item_type}")
                return False
            
            if not item:
                logger.warning(f"Item not found: {target_id}")
                return False
            
            # Update based on feedback
            if feedback.correct:
                # Correct answer: increase frequency
                new_frequency = item.frequency + 1
                logger.info(f"Correct answer for {item_value}, frequency now {new_frequency}")
            else:
                # Incorrect answer: slight penalty, but still mark as studied
                new_frequency = max(1, item.frequency)  # At least 1 if studied wrong
                logger.info(f"Incorrect answer for {item_value}")
            
            # Update repository
            success = self.repo.update_item_frequency(item_type, item_value, new_frequency)
            
            if success:
                # Save to disk
                self.repo.save_memory()
            
            return success
        
        except Exception as e:
            logger.error(f"Error recording feedback: {e}")
            return False
    
    def get_lesson_plan(self, lesson_count: int = 10) -> List[StudyTarget]:
        """
        Get a full lesson plan (collection of study targets).
        
        Args:
            lesson_count: Number of items in lesson
        
        Returns:
            List of StudyTarget objects for the lesson
        """
        return self.get_study_recommendation(batch_size=lesson_count)

    def get_lesson_by_id(self, lesson_id: str) -> List[StudyTarget]:
        """Load a lesson from lessons catalog and map to study targets."""
        catalog_path = settings.LESSONS_CATALOG_FILE
        if not catalog_path.exists():
            return []

        try:
            with open(catalog_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)

            lessons = payload.get("lessons", [])
            lesson = next((item for item in lessons if item.get("lesson_id") == lesson_id), None)
            if not lesson:
                return []

            targets: List[StudyTarget] = []
            for entry in lesson.get("items", []):
                item_type = entry.get("item_type")
                value = entry.get("value")
                if not value or item_type not in {"word", "phrase"}:
                    continue

                item = self.repo.get_word(value) if item_type == "word" else self.repo.get_phrase(value)
                if not item:
                    continue

                targets.append(
                    StudyTarget(
                        target_id=f"{item_type}-{item.value}",
                        target_type=item_type,
                        target_value=item.value,
                        target_translation=item.translation,
                        urgency_score=0.8,
                        reason=f"Lesson '{lesson_id}'",
                        audio_url=f"/api/audio/{item_type}-{item.value}.mp3",
                    )
                )

            return targets
        except Exception as exc:
            logger.error("Failed to load lesson '%s': %s", lesson_id, exc)
            return []

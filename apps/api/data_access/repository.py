"""
Repository pattern for managing vocabulary and study state.
Provides in-memory access to loaded data with persistence hooks.
"""

from typing import Dict, List, Optional, Set
from datetime import datetime
from core.models import WordDTO, PhraseDTO, VocabularyStats
from data_access.loader import DataLoader
from config import settings
from utils.logger import get_logger
import json

logger = get_logger(__name__)


class VocabularyRepository:
    """
    Central repository for vocabulary state.
    Implements lazy loading and caching of vocabulary data.
    """
    
    def __init__(self):
        """Initialize empty repository."""
        self._words: Optional[Dict[str, WordDTO]] = None
        self._phrases: Optional[Dict[str, PhraseDTO]] = None
        self._memory: Optional[Dict[str, int]] = None
        self._initialized = False
    
    def initialize(self) -> None:
        """Load all data from files."""
        if self._initialized:
            return
        
        logger.info("Initializing vocabulary repository...")
        
        # Load words
        self._words = DataLoader.load_words(settings.WORDS_FILE)
        
        # Load phrases with dependency inference
        self._phrases, _ = DataLoader.load_phrases(
            settings.LESSONS_FILE,
            self._words
        )
        
        # Load memory state (updates frequencies)
        self._memory = DataLoader.load_memory(settings.MEMORY_FILE)
        
        # Apply memory updates to items
        self._apply_memory_updates()
        
        self._initialized = True
        logger.info(f"Repository ready: {len(self._words)} words, {len(self._phrases)} phrases")
    
    def _apply_memory_updates(self) -> None:
        """Apply memory-based frequency updates to words and phrases."""
        if not self._memory or not self._words or not self._phrases:
            return
        
        for key, frequency in self._memory.items():
            if key in self._words:
                self._words[key].frequency = frequency
            elif key in self._phrases:
                self._phrases[key].frequency = frequency
    
    # Word operations
    
    def get_word(self, value: str) -> Optional[WordDTO]:
        """Get a word by its value."""
        self.initialize()
        return self._words.get(value)

    def _unique_words(self) -> List[WordDTO]:
        """Return unique words when aliases map to the same WordDTO."""
        if not self._words:
            return []

        unique_by_value: Dict[str, WordDTO] = {}
        for word in self._words.values():
            unique_by_value[word.value] = word
        return list(unique_by_value.values())
    
    def get_all_words(self) -> List[WordDTO]:
        """Get all words."""
        self.initialize()
        return self._unique_words()
    
    def get_words_page(self, page: int = 1, page_size: int = 20) -> tuple:
        """
        Get paginated words.
        
        Returns:
            Tuple of (words, total_count)
        """
        self.initialize()
        all_words = self.get_all_words()
        total = len(all_words)
        
        start = (page - 1) * page_size
        end = start + page_size
        
        return all_words[start:end], total
    
    def search_words(self, query: str) -> List[WordDTO]:
        """Search words by value or translation."""
        self.initialize()
        query_lower = query.lower()

        if not self._words:
            return []

        matched_by_value: Dict[str, WordDTO] = {}
        for alias, word in self._words.items():
            if (
                query_lower in alias.lower()
                or query_lower in word.value.lower()
                or query_lower in word.translation.lower()
            ):
                matched_by_value[word.value] = word

        return list(matched_by_value.values())
    
    # Phrase operations
    
    def get_phrase(self, value: str) -> Optional[PhraseDTO]:
        """Get a phrase by its value."""
        self.initialize()
        return self._phrases.get(value)
    
    def get_all_phrases(self) -> List[PhraseDTO]:
        """Get all phrases."""
        self.initialize()
        return list(self._phrases.values()) if self._phrases else []
    
    def get_phrases_page(self, page: int = 1, page_size: int = 20) -> tuple:
        """Get paginated phrases."""
        self.initialize()
        all_phrases = self.get_all_phrases()
        total = len(all_phrases)
        
        start = (page - 1) * page_size
        end = start + page_size
        
        return all_phrases[start:end], total
    
    def search_phrases(self, query: str) -> List[PhraseDTO]:
        """Search phrases by value or translation."""
        self.initialize()
        query_lower = query.lower()
        
        results = [
            p for p in self._phrases.values()
            if query_lower in p.value.lower()
            or query_lower in p.translation.lower()
        ]
        
        return results
    
    # Statistics
    
    def get_word_stats(self, value: str) -> Optional[VocabularyStats]:
        """Get statistics for a word."""
        word = self.get_word(value)
        if not word:
            return None
        
        return VocabularyStats(
            id=f"word-{word.value}",
            value=word.value,
            item_type="word",
            frequency=word.frequency,
            age=word.age,
            complexity=word.complexity,
            last_studied=None  # Would come from a study history table
        )
    
    def get_phrase_stats(self, value: str) -> Optional[VocabularyStats]:
        """Get statistics for a phrase."""
        phrase = self.get_phrase(value)
        if not phrase:
            return None
        
        return VocabularyStats(
            id=f"phrase-{value}",
            value=value,
            item_type="phrase",
            frequency=phrase.frequency,
            age=phrase.age,
            complexity=phrase.complexity,
            last_studied=None
        )
    
    def get_all_stats(self) -> tuple:
        """Get overall learning statistics."""
        self.initialize()

        words = self._unique_words()
        phrases = self._phrases.values() if self._phrases else []
        
        total_words = len(words)
        words_learned = sum(1 for w in words if w.frequency > 0)
        
        total_phrases = len(phrases)
        phrases_learned = sum(1 for p in phrases if p.frequency > 0)
        
        all_items = list(words) + list(phrases)
        avg_complexity = (
            sum(item.complexity for item in all_items) / len(all_items)
            if all_items
            else 0
        )
        
        return {
            "total_words": total_words,
            "words_learned": words_learned,
            "total_phrases": total_phrases,
            "phrases_learned": phrases_learned,
            "average_complexity": round(avg_complexity, 2),
            "total_items": total_words + total_phrases,
            "items_learned": words_learned + phrases_learned
        }
    
    # Update operations
    
    def update_item_frequency(self, item_type: str, value: str, new_frequency: int) -> bool:
        """
        Update frequency of a word or phrase.
        
        Args:
            item_type: "word" or "phrase"
            value: The word/phrase value
            new_frequency: New frequency value
        
        Returns:
            True if successful
        """
        self.initialize()
        
        try:
            if item_type == "word" and value in self._words:
                word = self._words[value]
                word.frequency = new_frequency
                self._memory[word.value] = new_frequency
                return True
            elif item_type == "phrase" and value in self._phrases:
                self._phrases[value].frequency = new_frequency
                self._memory[value] = new_frequency
                return True
        except Exception as e:
            logger.error(f"Error updating frequency: {e}")
        
        return False
    
    def save_memory(self) -> bool:
        """Save current state to memory file."""
        if not self._memory:
            return False
        
        try:
            with open(settings.MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._memory, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved memory state to {settings.MEMORY_FILE}")
            return True
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
            return False

    def get_memory_snapshot(self) -> Dict[str, int]:
        """Return a copy of the in-memory frequency map."""
        self.initialize()
        return dict(self._memory or {})

    def get_teaching_statistics(self, top_n: int = 10) -> dict:
        """Aggregate learning and teaching statistics across words and phrases."""
        self.initialize()

        words = self._unique_words()
        phrases = list(self._phrases.values()) if self._phrases else []

        total_word_frequency = sum(item.frequency for item in words)
        total_phrase_frequency = sum(item.frequency for item in phrases)

        taught_words = [item for item in words if item.frequency > 0]
        taught_phrases = [item for item in phrases if item.frequency > 0]

        top_words = sorted(words, key=lambda item: item.frequency, reverse=True)[:top_n]
        top_phrases = sorted(phrases, key=lambda item: item.frequency, reverse=True)[:top_n]

        return {
            "summary": {
                "total_words": len(words),
                "total_phrases": len(phrases),
                "taught_words": len(taught_words),
                "taught_phrases": len(taught_phrases),
                "total_word_frequency": total_word_frequency,
                "total_phrase_frequency": total_phrase_frequency,
                "total_taught_frequency": total_word_frequency + total_phrase_frequency,
            },
            "top_words": [
                {
                    "value": item.value,
                    "translation": item.translation,
                    "frequency": item.frequency,
                    "complexity": item.complexity,
                    "age": item.age,
                }
                for item in top_words
            ],
            "top_phrases": [
                {
                    "value": item.value,
                    "translation": item.translation,
                    "frequency": item.frequency,
                    "complexity": item.complexity,
                    "age": item.age,
                }
                for item in top_phrases
            ],
        }


# Global repository instance
_repository: Optional[VocabularyRepository] = None


def get_repository() -> VocabularyRepository:
    """Get or create global repository instance."""
    global _repository
    if _repository is None:
        _repository = VocabularyRepository()
        _repository.initialize()
    return _repository


def reset_repository() -> None:
    """Reset repository (for testing)."""
    global _repository
    _repository = None

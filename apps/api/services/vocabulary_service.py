"""
Vocabulary service - business logic for vocabulary operations.
"""

from typing import List, Optional
from core.models import WordDTO, PhraseDTO, VocabularyStats
from data_access.repository import get_repository
from utils.logger import get_logger

logger = get_logger(__name__)


class VocabularyService:
    """Service layer for vocabulary operations."""
    
    def __init__(self):
        """Initialize with repository access."""
        self.repo = get_repository()
    
    # Word operations
    
    def get_word(self, value: str) -> Optional[WordDTO]:
        """Get a word by value."""
        return self.repo.get_word(value)
    
    def get_all_words(self, page: Optional[int] = None, page_size: int = 20) -> dict:
        """
        Get all words, optionally paginated.
        
        Returns:
            Dict with 'words' list and 'total' count
        """
        if page is None:
            words = self.repo.get_all_words()
            return {"words": words, "total": len(words), "page": 1, "page_size": len(words)}
        
        words, total = self.repo.get_words_page(page, page_size)
        return {
            "words": words,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": (total + page_size - 1) // page_size
        }
    
    def search_words(self, query: str) -> List[WordDTO]:
        """Search for words."""
        if not query or len(query.strip()) == 0:
            return []
        
        return self.repo.search_words(query)
    
    def get_word_stats(self, value: str) -> Optional[VocabularyStats]:
        """Get statistics for a word."""
        return self.repo.get_word_stats(value)
    
    # Phrase operations
    
    def get_phrase(self, value: str) -> Optional[PhraseDTO]:
        """Get a phrase by value."""
        return self.repo.get_phrase(value)
    
    def get_all_phrases(self, page: Optional[int] = None, page_size: int = 20) -> dict:
        """Get all phrases, optionally paginated."""
        if page is None:
            phrases = self.repo.get_all_phrases()
            return {"phrases": phrases, "total": len(phrases), "page": 1, "page_size": len(phrases)}
        
        phrases, total = self.repo.get_phrases_page(page, page_size)
        return {
            "phrases": phrases,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": (total + page_size - 1) // page_size
        }
    
    def search_phrases(self, query: str) -> List[PhraseDTO]:
        """Search for phrases."""
        if not query or len(query.strip()) == 0:
            return []
        
        return self.repo.search_phrases(query)
    
    def get_phrase_stats(self, value: str) -> Optional[VocabularyStats]:
        """Get statistics for a phrase."""
        return self.repo.get_phrase_stats(value)
    
    # Statistics
    
    def get_progress_snapshot(self) -> dict:
        """Get overall learning progress."""
        stats = self.repo.get_all_stats()
        
        return {
            "total_words": stats["total_words"],
            "words_learned": stats["words_learned"],
            "words_learned_percentage": (
                round(stats["words_learned"] / stats["total_words"] * 100, 1)
                if stats["total_words"] > 0
                else 0
            ),
            "total_phrases": stats["total_phrases"],
            "phrases_learned": stats["phrases_learned"],
            "phrases_learned_percentage": (
                round(stats["phrases_learned"] / stats["total_phrases"] * 100, 1)
                if stats["total_phrases"] > 0
                else 0
            ),
            "average_complexity": stats["average_complexity"],
            "total_items": stats["total_items"],
            "items_learned": stats["items_learned"],
        }

"""
Vocabulary API routes.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from core.models import WordDTO, PhraseDTO, VocabularyStats
from services.vocabulary_service import VocabularyService

router = APIRouter(prefix="/api/vocabulary", tags=["vocabulary"])
service = VocabularyService()


@router.get("/words", response_model=dict)
async def get_words(
    page: Optional[int] = Query(None, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query")
):
    """
    Get all words, optionally with pagination and search.
    """
    if search:
        words = service.search_words(search)
        return {
            "words": words,
            "total": len(words),
            "search_query": search
        }
    
    return service.get_all_words(page=page, page_size=page_size)


@router.get("/words/{word_value}", response_model=WordDTO)
async def get_word(word_value: str):
    """
    Get a specific word by value.
    """
    word = service.get_word(word_value)
    if not word:
        raise HTTPException(status_code=404, detail=f"Word '{word_value}' not found")
    return word


@router.get("/words/{word_value}/stats", response_model=VocabularyStats)
async def get_word_stats(word_value: str):
    """
    Get statistics for a word.
    """
    stats = service.get_word_stats(word_value)
    if not stats:
        raise HTTPException(status_code=404, detail=f"Word '{word_value}' not found")
    return stats


@router.get("/phrases", response_model=dict)
async def get_phrases(
    page: Optional[int] = Query(None, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query")
):
    """
    Get all phrases, optionally with pagination and search.
    """
    if search:
        phrases = service.search_phrases(search)
        return {
            "phrases": phrases,
            "total": len(phrases),
            "search_query": search
        }
    
    return service.get_all_phrases(page=page, page_size=page_size)


@router.get("/phrases/{phrase_value}", response_model=PhraseDTO)
async def get_phrase(phrase_value: str):
    """
    Get a specific phrase by value.
    """
    phrase = service.get_phrase(phrase_value)
    if not phrase:
        raise HTTPException(status_code=404, detail=f"Phrase '{phrase_value}' not found")
    return phrase


@router.get("/phrases/{phrase_value}/stats", response_model=VocabularyStats)
async def get_phrase_stats(phrase_value: str):
    """
    Get statistics for a phrase.
    """
    stats = service.get_phrase_stats(phrase_value)
    if not stats:
        raise HTTPException(status_code=404, detail=f"Phrase '{phrase_value}' not found")
    return stats


@router.get("/progress", response_model=dict)
async def get_progress():
    """
    Get overall learning progress snapshot.
    """
    return service.get_progress_snapshot()

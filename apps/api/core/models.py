"""
Domain models and DTOs for the Language Learning Framework API.(Pydantic models for type safety and validation)
"""

from typing import List, Optional, Set
from pydantic import BaseModel, Field
from enum import Enum


class WordDTO(BaseModel):
    """Data Transfer Object for Word domain model."""
    value: str = Field(..., description="The word in target language")
    translation: str = Field(..., description="Translation to native language")
    complexity: int = Field(default=1, ge=1, description="Learning difficulty level")
    frequency: int = Field(default=0, ge=0, description="How often the word appears")
    age: int = Field(default=0, ge=0, description="Age in learning sessions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "value": "Grüezi",
                "translation": "Hello",
                "complexity": 1,
                "frequency": 15,
                "age": 30
            }
        }


class PhraseDTO(BaseModel):
    """Data Transfer Object for Phrase domain model."""
    value: str = Field(..., description="The phrase in target language")
    translation: str = Field(..., description="Translation to native language")
    complexity: int = Field(default=1, ge=1, description="Learning difficulty level")
    frequency: int = Field(default=0, ge=0, description="How often the phrase appears")
    age: int = Field(default=0, ge=0, description="Age in learning sessions")
    words: List[str] = Field(default_factory=list, description="Words contained in phrase")
    dependencies: List[str] = Field(default_factory=list, description="Phrases that must be learned first")
    
    class Config:
        json_schema_extra = {
            "example": {
                "value": "Guten Morgen",
                "translation": "Good morning",
                "complexity": 1,
                "frequency": 5,
                "age": 10,
                "words": ["Guten", "Morgen"],
                "dependencies": []
            }
        }


class StudyTarget(BaseModel):
    """Study recommendation from the planner."""
    target_id: str = Field(..., description="Word or Phrase identifier")
    target_type: str = Field(..., description="Either 'word' or 'phrase'")
    target_value: str = Field(..., description="The actual word/phrase text")
    target_translation: str = Field(..., description="Translation of target")
    urgency_score: float = Field(..., ge=0.0, le=1.0, description="Priority (0-1)")
    reason: str = Field(..., description="Why this was selected")
    audio_url: Optional[str] = Field(None, description="URL to audio file if available")
    
    class Config:
        json_schema_extra = {
            "example": {
                "target_id": "word-123",
                "target_type": "word",
                "target_value": "Wasser",
                "target_translation": "Water",
                "urgency_score": 0.85,
                "reason": "High frequency, recent age",
                "audio_url": "/api/audio/word-123.mp3"
            }
        }


class StudyFeedback(BaseModel):
    """Feedback after a study interaction."""
    target_id: str = Field(..., description="Word or Phrase studied")
    correct: bool = Field(..., description="Whether the answer was correct")
    confidence: int = Field(..., ge=1, le=5, description="User confidence (1-5)")
    time_spent_seconds: int = Field(..., ge=0, description="Time spent on this item")
    
    class Config:
        json_schema_extra = {
            "example": {
                "target_id": "word-123",
                "correct": True,
                "confidence": 4,
                "time_spent_seconds": 12
            }
        }


class ProgressSnapshot(BaseModel):
    """Current learning progress summary."""
    total_words: int = Field(..., description="Total unique words in system")
    words_learned: int = Field(..., description="Words with non-zero frequency")
    total_phrases: int = Field(..., description="Total unique phrases in system")
    phrases_learned: int = Field(..., description="Phrases with non-zero frequency")
    average_complexity: float = Field(..., description="Average complexity of known items")
    session_count: int = Field(..., description="Total study sessions completed")
    last_session_time: Optional[str] = Field(None, description="ISO timestamp of last session")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_words": 500,
                "words_learned": 145,
                "total_phrases": 200,
                "phrases_learned": 32,
                "average_complexity": 2.3,
                "session_count": 48,
                "last_session_time": "2026-03-23T14:30:00Z"
            }
        }


class VocabularyStats(BaseModel):
    """Statistics for a word or phrase."""
    id: str = Field(..., description="Item identifier")
    value: str = Field(..., description="The word or phrase")
    item_type: str = Field(..., description="'word' or 'phrase'")
    frequency: int = Field(..., description="Appearance count")
    age: int = Field(..., description="Sessions since last study")
    complexity: int = Field(..., description="Difficulty rating")
    last_studied: Optional[str] = Field(None, description="ISO timestamp")


class LessonItem(BaseModel):
    """A single item in a lesson study sequence."""
    target_id: str
    value: str
    translation: str
    item_type: str  # 'word' or 'phrase'
    audio_url: Optional[str] = None
    image_url: Optional[str] = None
    context_phrase: Optional[str] = None
    hints: List[str] = Field(default_factory=list)


class CreateWordRequest(BaseModel):
    """Request payload for creating a new word entry."""
    value: str = Field(..., min_length=1)
    translation: str = Field(..., min_length=1)
    complexity: int = Field(default=1, ge=1)
    frequency: int = Field(default=0, ge=0)
    age: int = Field(default=0, ge=0)


class CreatePhraseRequest(BaseModel):
    """Request payload for creating a new phrase entry."""
    value: str = Field(..., min_length=1)
    translation: str = Field(..., min_length=1)
    complexity: int = Field(default=1, ge=1)
    frequency: int = Field(default=0, ge=0)
    age: int = Field(default=0, ge=0)


class LessonEntry(BaseModel):
    """A lesson reference to a word or phrase item."""
    item_type: str = Field(..., description="word or phrase")
    value: str = Field(..., min_length=1)


class TtsMethod(str, Enum):
    """Supported TTS synthesis methods."""

    PROVIDER = "provider"
    SPEECHT5 = "speecht5"
    LEGACY_STITCHED = "legacy_stitched"
    ORPHEUS_LORA = "orpheus_lora"


class LessonDefinition(BaseModel):
    """A user-defined lesson containing item references."""
    lesson_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    items: List[LessonEntry] = Field(default_factory=list)
    tts_method: TtsMethod = Field(default=TtsMethod.PROVIDER)
    tts_provider_id: Optional[str] = None


class CreateLessonRequest(BaseModel):
    """Request payload for creating a lesson."""
    lesson_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    items: List[LessonEntry] = Field(default_factory=list)
    tts_method: TtsMethod = Field(default=TtsMethod.PROVIDER)
    tts_provider_id: Optional[str] = None


class TtsProviderConfig(BaseModel):
    """Configuration for a TTS provider endpoint."""
    provider_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    base_url: str = Field(..., min_length=1)
    synthesize_path: str = Field(default="/synthesize")
    health_path: str = Field(default="/health")
    api_key: Optional[str] = None
    enabled: bool = True
    extra_headers: dict = Field(default_factory=dict)


class TtsInferenceRequest(BaseModel):
    """Request payload for running TTS inference via a provider."""
    provider_id: Optional[str] = None
    text: str = Field(..., min_length=1)
    language: Optional[str] = None
    voice: Optional[str] = None
    tts_method: TtsMethod = Field(default=TtsMethod.PROVIDER)
    options: dict = Field(default_factory=dict)

"""
Application constants and enumerations.
"""

from enum import Enum

# Default file paths (relative to repository root)
DEFAULT_WORDS_FILE = "data/seed/words.txt"
DEFAULT_LESSONS_FILE = "data/seed/lesson1.txt"
DEFAULT_MEMORY_FILE = "data/state/mem0"
DEFAULT_AUDIO_DIR = "data/audio"

# API defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
DEFAULT_STUDY_BATCH_SIZE = 5

# Study thresholds
COMPLEXITY_MIN = 1
COMPLEXITY_MAX = 10
FREQUENCY_THRESHOLD_LEARNED = 1  # Frequency > this means "studied"
AGE_THRESHOLD_URGENT = 50  # Age > this means "needs review"

# Audio settings
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".ogg"]
AUDIO_SERVE_URL_PREFIX = "/api/audio"

# Response statuses
class ResponseStatus(str, Enum):
    """Standard response status."""
    SUCCESS = "success"
    ERROR = "error"
    NOT_FOUND = "not_found"
    INVALID_INPUT = "invalid_input"

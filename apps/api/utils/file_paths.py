"""
Utility functions for file path management.
Centralizes all path operations for easy maintenance.
"""

from pathlib import Path
from typing import Optional
from config import settings


def get_audio_file_path(filename: str) -> Optional[Path]:
    """
    Get absolute path to audio file if it exists.
    
    Args:
        filename: Audio filename (e.g., "word-123.mp3")
    
    Returns:
        Path to audio file if it exists, None otherwise
    """
    file_path = settings.AUDIO_DIR / filename
    return file_path if file_path.exists() else None


def get_audio_filename(item_id: str, format_ext: str = "mp3") -> str:
    """
    Generate standardized audio filename for a word/phrase.
    
    Args:
        item_id: Word or phrase identifier
        format_ext: File extension (mp3, wav, ogg)
    
    Returns:
        Standardized filename
    """
    return f"{item_id}.{format_ext}"


def get_data_file_path(file_path: Path) -> str:
    """
    Get absolute path to a data file.
    
    Args:
        file_path: Configured file path
    
    Returns:
        Absolute path string
    """
    return str(file_path.resolve())


def ensure_audio_directory() -> None:
    """Ensure audio directory exists."""
    settings.AUDIO_DIR.mkdir(parents=True, exist_ok=True)

"""
Audio service - manages audio file serving and streaming.
"""

from pathlib import Path
from typing import Optional, Tuple
from config import settings
from utils.file_paths import get_audio_file_path
from utils.logger import get_logger

logger = get_logger(__name__)


class AudioService:
    """Service layer for audio operations."""
    
    @staticmethod
    def get_audio_file(filename: str) -> Optional[Path]:
        """
        Get audio file path if it exists.
        
        Args:
            filename: Audio filename (e.g., "word-Grüezi.mp3")
        
        Returns:
            Path to file if it exists, None otherwise
        """
        try:
            return get_audio_file_path(filename)
        except Exception as e:
            logger.error(f"Error getting audio file: {e}")
            return None
    
    @staticmethod
    def list_audio_files(limit: int = 100) -> list:
        """
        List available audio files.
        
        Args:
            limit: Maximum files to return
        
        Returns:
            List of filenames
        """
        try:
            if not settings.AUDIO_DIR.exists():
                return []
            
            files = list(settings.AUDIO_DIR.glob("*.*"))
            return [f.name for f in files[:limit]]
        except Exception as e:
            logger.error(f"Error listing audio files: {e}")
            return []
    
    @staticmethod
    def get_audio_stats() -> dict:
        """Get statistics about available audio files."""
        try:
            if not settings.AUDIO_DIR.exists():
                return {"total_files": 0, "formats": {}}
            
            files = list(settings.AUDIO_DIR.glob("*.*"))
            formats = {}
            
            for f in files:
                ext = f.suffix.lower()
                formats[ext] = formats.get(ext, 0) + 1
            
            return {
                "total_files": len(files),
                "formats": formats,
                "audio_dir": str(settings.AUDIO_DIR)
            }
        except Exception as e:
            logger.error(f"Error getting audio stats: {e}")
            return {"total_files": 0, "formats": {}, "error": str(e)}

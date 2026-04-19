"""
Application configuration and settings.
Centralizes environment variables and configuration management.
"""

import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


_CURRENT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _CURRENT_DIR.parents[1]

# Load environment values from repo root first, then local override in apps/api/.env.
load_dotenv(_REPO_ROOT / ".env", override=False)
load_dotenv(_CURRENT_DIR / ".env", override=True)

# Environment configurations
class Settings:
    """Application settings with sensible defaults."""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "5000"))
    API_DEBUG: bool = os.getenv("API_DEBUG", "False").lower() == "true"
    API_RELOAD: bool = os.getenv("API_RELOAD", "False").lower() == "true"
    
    # CORS Configuration
    _cors_env: str = os.getenv("CORS_ORIGINS", "")
    if _cors_env:
        try:
            CORS_ORIGINS: list = json.loads(_cors_env)
        except json.JSONDecodeError:
            CORS_ORIGINS: list = [origin.strip() for origin in _cors_env.split(",") if origin.strip()]
    else:
        CORS_ORIGINS: list = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            os.getenv("FRONTEND_URL", "http://localhost:3000"),
        ]
    
    # Data Paths
    DATA_ROOT: Path = Path(__file__).resolve().parent / "data"
    SEED_DIR: Path = DATA_ROOT / "seed"
    STATE_DIR: Path = DATA_ROOT / "state"
    AUDIO_DIR: Path = DATA_ROOT / "audio"
    
    # File paths
    WORDS_FILE: Path = SEED_DIR / "words.txt"
    LESSONS_FILE: Path = SEED_DIR / "lesson1.txt"
    LESSONS_CATALOG_FILE: Path = SEED_DIR / "lessons.json"
    MEMORY_FILE: Path = STATE_DIR / "mem0"
    TTS_PROVIDERS_FILE: Path = STATE_DIR / "tts_providers.json"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[Path] = (
        Path(os.getenv("LOG_FILE"))
        if os.getenv("LOG_FILE")
        else None
    )
    
    @classmethod
    def get_api_url(cls) -> str:
        """Get full API URL."""
        return f"http://{cls.API_HOST}:{cls.API_PORT}"
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        cls.DATA_ROOT.mkdir(parents=True, exist_ok=True)
        cls.SEED_DIR.mkdir(parents=True, exist_ok=True)
        cls.STATE_DIR.mkdir(parents=True, exist_ok=True)
        cls.AUDIO_DIR.mkdir(parents=True, exist_ok=True)


# Create global settings instance
settings = Settings()

# Ensure directories on import
settings.ensure_directories()

"""
Logging configuration and utilities.
"""

import logging
from typing import Optional
from config import settings

def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with configured settings.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Set level
        level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
        logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (if configured)
        if settings.LOG_FILE:
            file_handler = logging.FileHandler(settings.LOG_FILE)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger

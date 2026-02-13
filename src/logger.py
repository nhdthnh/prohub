"""
Logging module for OQR Dashboard.
Centralized logging configuration and utilities.
"""

import logging
import logging.handlers
from typing import Optional
import config

# Configure root logger
logger = logging.getLogger("oqr_dashboard")
logger.setLevel(getattr(logging, config.LOG_LEVEL))

# Remove existing handlers to avoid duplicates
logger.handlers.clear()

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
formatter = logging.Formatter(config.LOG_FORMAT)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler (if configured)
if config.LOG_FILE:
    file_handler = logging.handlers.RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5,
    )
    file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"oqr_dashboard.{name}")

"""
Database connection module.
Handles SQLAlchemy engine creation and connection pooling.
"""

from sqlalchemy import create_engine, Engine, event, text
from urllib.parse import quote_plus
import streamlit as st
from typing import Optional
import config
from src.logger import get_logger

logger = get_logger(__name__)


@st.cache_resource
def get_engine() -> Optional[Engine]:
    """
    Get or create SQLAlchemy engine with connection pooling.
    
    Returns:
        SQLAlchemy Engine instance or None if connection fails
        
    Raises:
        Exception: If connection string is invalid
    """
    try:
        # URL encode password to handle special characters like @
        encoded_password = quote_plus(config.DB_PASSWORD)
        
        # Build connection string
        connection_string = (
            f"mysql+pymysql://{config.DB_USER}:{encoded_password}"
            f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
            f"?charset={config.DB_CHARSET}"
        )
        
        # Create engine with connection pooling
        engine = create_engine(
            connection_string,
            pool_size=config.DB_POOL_SIZE,
            max_overflow=config.DB_MAX_OVERFLOW,
            pool_timeout=config.DB_POOL_TIMEOUT,
            pool_recycle=config.DB_POOL_RECYCLE,
            echo=False,  # Set to True for SQL debugging
        )
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            
        logger.info("✓ Database connection successful")
        return engine
        
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        st.error(f"{config.ERROR_MESSAGES['db_connection']}\nError: {e}")
        return None


def close_engine(engine: Engine) -> None:
    """
    Close database engine and dispose of connection pool.
    
    Args:
        engine: SQLAlchemy Engine instance
    """
    if engine:
        try:
            engine.dispose()
            logger.info("Database engine closed")
        except Exception as e:
            logger.error(f"Error closing database engine: {e}")

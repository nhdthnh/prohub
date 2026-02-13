"""
Query file management utilities.
Load SQL queries from query directory.
"""

import os
from typing import Optional
import streamlit as st
import config
from src.logger import get_logger

logger = get_logger(__name__)

# Query directory path
QUERY_DIR = "query"


def load_query(filename: str) -> str:
    """
    Load SQL query from query directory.
    
    Args:
        filename: SQL file name (e.g., "GET_BRAND.sql")
        
    Returns:
        SQL query string
        
    Raises:
        FileNotFoundError: If query file not found
    """
    file_path = os.path.join(QUERY_DIR, filename)
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            query = f.read().strip()
            logger.debug(f"Loaded query: {filename}")
            return query
    except FileNotFoundError:
        error_msg = config.ERROR_MESSAGES["query_not_found"].format(filename=filename)
        logger.error(error_msg)
        st.error(error_msg)
        return ""
    except Exception as e:
        logger.error(f"Error loading query {filename}: {e}")
        st.error(f"Error reading query file: {e}")
        return ""


def get_query_by_key(key: str) -> str:
    """
    Load query using configuration key.
    
    Args:
        key: Key in config.QUERY_FILES (e.g., 'kpi', 'trend')
        
    Returns:
        SQL query string
    """
    if key not in config.QUERY_FILES:
        logger.error(f"Unknown query key: {key}")
        return ""
    
    filename = config.QUERY_FILES[key]
    return load_query(filename)

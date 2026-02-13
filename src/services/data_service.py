"""
Data service module.
Handles all data fetching, transformation, and aggregation logic.
"""

from typing import Tuple, Dict, List, Optional
import pandas as pd
from sqlalchemy import Engine
import streamlit as st

import config
from src.logger import get_logger
from src.utils.query_manager import load_query, get_query_by_key
from src.utils.sql_helpers import build_filters, build_inventory_filters

logger = get_logger(__name__)


@st.cache_data(ttl=config.CACHE_TTL_DATA)
def fetch_data(
    query: str,
    _engine: Engine,
    params: Optional[Tuple] = None
) -> pd.DataFrame:
    """
    Execute SQL query and return pandas DataFrame.
    Results are cached for performance.
    
    Args:
        query: SQL query string
        _engine: SQLAlchemy Engine (prefixed with _ to prevent Streamlit hashing)
        params: Query parameters tuple (optional)
        
    Returns:
        DataFrame with query results, empty DataFrame on error
    """
    try:
        df = pd.read_sql(query, _engine, params=params)
        logger.info(f"Fetched {len(df)} rows from database")
        return df
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=config.CACHE_TTL_OPTIONS)
def load_filter_options(query_file: str, column: str, _engine: Engine) -> List[str]:
    """
    Load options for filter dropdowns (brand, shop, status, etc.).
    Results cached for 1 hour.
    
    Args:
        query_file: SQL filename to load
        column: Column name to extract unique values
        _engine: SQLAlchemy Engine
        
    Returns:
        Sorted list of unique values from column
    """
    try:
        df = fetch_data(
            load_query(query_file),
            _engine,
            params=(config.MIN_DATE_STR, config.MAX_DATE_STR),
        )
        if not df.empty and column in df.columns:
            options = sorted(df[column].unique().tolist())
            logger.info(f"Loaded {len(options)} options from {query_file} column {column}")
            return options
        return []
    except Exception as e:
        logger.error(f"Error loading filter options from {query_file}: {e}")
        return []


def get_kpi_data(
    start_date_str: str,
    end_date_str: str,
    prev_start_str: str,
    prev_end_str: str,
    filters: str,
    engine: Engine,
) -> pd.DataFrame:
    """
    Fetch KPI metrics (Revenue, Orders, AOV, Growth).
    
    Args:
        start_date_str: Current period start (YYYY-MM-DD HH:MM:SS)
        end_date_str: Current period end (YYYY-MM-DD HH:MM:SS)
        prev_start_str: Previous period start
        prev_end_str: Previous period end
        filters: SQL WHERE clause
        engine: SQLAlchemy Engine
        
    Returns:
        DataFrame with KPI metrics
    """
    try:
        query = load_query(config.QUERY_FILES["kpi"]).format(filters=filters)
        params = (
            start_date_str, end_date_str,
            start_date_str, end_date_str,
            prev_start_str, prev_end_str,
            prev_start_str, prev_end_str,
            prev_start_str, end_date_str,
        )
        df = fetch_data(query, engine, params=params)
        logger.info(f"Fetched KPI data: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error fetching KPI data: {e}")
        return pd.DataFrame()


def get_trend_data(
    start_date_str: str,
    end_date_str: str,
    filters: str,
    engine: Engine,
) -> pd.DataFrame:
    """
    Fetch hourly trend data (Revenue and Orders by hour).
    
    Args:
        start_date_str: Period start (YYYY-MM-DD HH:MM:SS)
        end_date_str: Period end (YYYY-MM-DD HH:MM:SS)
        filters: SQL WHERE clause
        engine: SQLAlchemy Engine
        
    Returns:
        DataFrame with columns: HOURNUM, Revenue, Orders
    """
    try:
        query = load_query(config.QUERY_FILES["trend"]).format(filters=filters)
        params = (start_date_str, end_date_str)
        df = fetch_data(query, engine, params=params)
        logger.info(f"Fetched trend data: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error fetching trend data: {e}")
        return pd.DataFrame()


def get_status_summary(
    start_date_str: str,
    end_date_str: str,
    filters: str,
    engine: Engine,
) -> pd.DataFrame:
    """
    Fetch order status summary (count by status).
    
    Args:
        start_date_str: Period start
        end_date_str: Period end
        filters: SQL WHERE clause
        engine: SQLAlchemy Engine
        
    Returns:
        DataFrame with Status and Orders columns
    """
    try:
        query = load_query(config.QUERY_FILES["status"]).format(filters=filters)
        params = (start_date_str, end_date_str)
        df = fetch_data(query, engine, params=params)
        logger.info(f"Fetched status summary: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error fetching status summary: {e}")
        return pd.DataFrame()


def get_province_data(
    start_date_str: str,
    end_date_str: str,
    filters: str,
    engine: Engine,
    limit: int = 20,
) -> pd.DataFrame:
    """
    Fetch top provinces by orders/revenue.
    
    Args:
        start_date_str: Period start
        end_date_str: Period end
        filters: SQL WHERE clause
        engine: SQLAlchemy Engine
        limit: Number of top provinces to return
        
    Returns:
        DataFrame with Province, Orders, and Revenue columns
    """
    try:
        query = load_query(config.QUERY_FILES["province"]).format(filters=filters)
        params = (start_date_str, end_date_str)
        df = fetch_data(query, engine, params=params)
        logger.info(f"Fetched province data: {len(df)} rows")
        return df.head(limit)
    except Exception as e:
        logger.error(f"Error fetching province data: {e}")
        return pd.DataFrame()


def get_revenue_by_brand_platform(
    start_date_str: str,
    end_date_str: str,
    filters: str,
    engine: Engine,
) -> pd.DataFrame:
    """
    Fetch revenue data broken down by Brand and Platform.
    
    Args:
        start_date_str: Period start (YYYY-MM-DD HH:MM:SS)
        end_date_str: Period end (YYYY-MM-DD HH:MM:SS)
        filters: SQL WHERE clause
        engine: SQLAlchemy Engine
        
    Returns:
        DataFrame with Brand, Platform, Revenue, Orders
    """
    try:
        query = load_query(config.QUERY_FILES["revenue_brand_platform"]).format(filters=filters)
        params = (start_date_str, end_date_str)
        df = fetch_data(query, engine, params=params)
        logger.info(f"Fetched revenue by brand/platform: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error fetching revenue by brand/platform: {e}")
        return pd.DataFrame()


def get_revenue_by_brand(
    start_date_str: str,
    end_date_str: str,
    filters: str,
    engine: Engine,
) -> pd.DataFrame:
    """
    Fetch revenue data by Brand.
    
    Args:
        start_date_str: Period start (YYYY-MM-DD HH:MM:SS)
        end_date_str: Period end (YYYY-MM-DD HH:MM:SS)
        filters: SQL WHERE clause
        engine: SQLAlchemy Engine
        
    Returns:
        DataFrame with Brand, Revenue, Orders, RevenuePercent
    """
    try:
        query = load_query(config.QUERY_FILES["revenue_by_brand"]).format(filters=filters)
        params = (start_date_str, end_date_str, start_date_str, end_date_str)
        df = fetch_data(query, engine, params=params)
        logger.info(f"Fetched revenue by brand: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error fetching revenue by brand: {e}")
        return pd.DataFrame()


def get_revenue_by_platform(
    start_date_str: str,
    end_date_str: str,
    filters: str,
    engine: Engine,
) -> pd.DataFrame:
    """
    Fetch revenue data by Platform.
    
    Args:
        start_date_str: Period start (YYYY-MM-DD HH:MM:SS)
        end_date_str: Period end (YYYY-MM-DD HH:MM:SS)
        filters: SQL WHERE clause
        engine: SQLAlchemy Engine
        
    Returns:
        DataFrame with Platform, Revenue, Orders, RevenuePercent
    """
    try:
        query = load_query(config.QUERY_FILES["revenue_by_platform"]).format(filters=filters)
        params = (start_date_str, end_date_str, start_date_str, end_date_str)
        df = fetch_data(query, engine, params=params)
        logger.info(f"Fetched revenue by platform: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error fetching revenue by platform: {e}")
        return pd.DataFrame()


def get_filter_options_dict(engine: Engine) -> Dict[str, List[str]]:
    """
    Load all filter options at startup.
    
    Args:
        engine: SQLAlchemy Engine
        
    Returns:
        Dictionary with brand, shop, platform, status options
    """
    return {
        "brand": load_filter_options(config.QUERY_FILES["brand"], "brand", engine),
        "shop": load_filter_options(config.QUERY_FILES["shop"], "ShopName", engine),
        "status": load_filter_options(config.QUERY_FILES["order_status"], "StatusName", engine),
        "platform": config.PLATFORMS,  # Static list
    }

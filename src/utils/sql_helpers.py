"""
SQL helper utilities.
Handles SQL filtering, escaping, and WHERE clause building.
"""

from typing import List, Dict, Optional
from src.logger import get_logger

logger = get_logger(__name__)


def escape_sql_string(value: str) -> str:
    """
    Escape single quotes in SQL string to prevent SQL errors.
    
    Args:
        value: String to escape
        
    Returns:
        Escaped string
    """
    if isinstance(value, str):
        return value.replace("'", "''")
    return value


def build_filters(
    brand: List[str],
    platform: List[str],
    shop: List[str],
    status: List[str],
) -> str:
    """
    Build SQL WHERE clause from selected filters.
    Used for Sales/Orders table queries.
    
    Args:
        brand: List of selected brands
        platform: List of selected platforms
        shop: List of selected shops
        status: List of selected order statuses
        
    Returns:
        WHERE clause string (e.g., "AND brand IN (...) AND platform IN (...)")
        Returns empty string if no filters selected
    """
    filters = []
    
    # Brand filter
    actual_brands = [b for b in brand if b != "Tất cả"]
    if actual_brands:
        brands_str = "', '".join([escape_sql_string(b) for b in actual_brands])
        filters.append(f"brand IN ('{brands_str}')")
    
    # Platform filter
    actual_platforms = [p for p in platform if p != "Tất cả"]
    if actual_platforms:
        platforms_str = "', '".join([escape_sql_string(p) for p in actual_platforms])
        filters.append(f"PlatformName IN ('{platforms_str}')")
    
    # Shop filter
    actual_shops = [s for s in shop if s != "Tất cả"]
    if actual_shops:
        shops_str = "', '".join([escape_sql_string(s) for s in actual_shops])
        filters.append(f"ShopName IN ('{shops_str}')")
    
    # Status filter
    actual_statuses = [st for st in status if st != "Tất cả"]
    if actual_statuses:
        statuses_str = "', '".join([escape_sql_string(st) for st in actual_statuses])
        filters.append(f"StatusName IN ('{statuses_str}')")
    
    if filters:
        where_clause = "AND " + " AND ".join(filters)
        logger.debug(f"Built filters: {where_clause}")
        return where_clause
    
    return ""


def build_inventory_filters(brand: List[str], shop: List[str]) -> str:
    """
    Build SQL WHERE clause for Inventory table queries.
    Inventory table only has Brand and Shop (no Platform or Status).
    
    Args:
        brand: List of selected brands
        shop: List of selected shops
        
    Returns:
        WHERE clause string
    """
    filters = []
    
    # Brand filter
    actual_brands = [b for b in brand if b != "Tất cả"]
    if actual_brands:
        brands_str = "', '".join([escape_sql_string(b) for b in actual_brands])
        filters.append(f"brand IN ('{brands_str}')")
    
    # Shop filter
    actual_shops = [s for s in shop if s != "Tất cả"]
    if actual_shops:
        shops_str = "', '".join([escape_sql_string(s) for s in actual_shops])
        filters.append(f"ShopName IN ('{shops_str}')")
    
    if filters:
        where_clause = "AND " + " AND ".join(filters)
        logger.debug(f"Built inventory filters: {where_clause}")
        return where_clause
    
    return ""

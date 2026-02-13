"""
Formatter utilities.
Format data for display (currency, numbers, etc.)
"""

from typing import Optional, Union
import pandas as pd


def format_currency(value: Optional[Union[int, float]]) -> str:
    """
    Format number as Vietnamese currency (VND).
    
    Args:
        value: Numeric value to format
        
    Returns:
        Formatted string with commas (e.g., "1,234,567")
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "0"
    return "{:,.0f}".format(value)


def format_number(value: Optional[Union[int, float]]) -> str:
    """
    Format number with commas for thousands separator.
    
    Args:
        value: Numeric value to format
        
    Returns:
        Formatted string (e.g., "1,234,567")
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "0"
    return "{:,.0f}".format(value)


def format_percentage(value: Optional[float], decimal_places: int = 1) -> str:
    """
    Format value as percentage.
    
    Args:
        value: Numeric value to format
        decimal_places: Number of decimal places (default: 1)
        
    Returns:
        Formatted percentage string
    """
    if value is None or pd.isna(value):
        return "0%"
    return f"{value:.{decimal_places}f}%"


def get_growth_arrow(growth_value: float) -> str:
    """
    Get arrow symbol based on growth value.
    
    Args:
        growth_value: Growth percentage
        
    Returns:
        Arrow symbol: "↑" for positive, "↓" for negative
    """
    return "↑" if growth_value >= 0 else "↓"

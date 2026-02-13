"""
Date/time helper utilities.
"""

from datetime import datetime, timedelta
from typing import Tuple


def get_previous_period(start_date: datetime, end_date: datetime) -> Tuple[datetime, datetime]:
    """
    Calculate the previous period based on selected duration.
    
    Args:
        start_date: Start date of current period
        end_date: End date of current period
        
    Returns:
        Tuple of (previous_start_date, previous_end_date)
        
    Example:
        If current period is 2024-02-10 to 2024-02-15 (6 days),
        returns 2024-02-04 to 2024-02-09
    """
    delta = end_date - start_date
    prev_end = start_date - timedelta(days=1)
    prev_start = prev_end - delta
    return prev_start, prev_end


def format_date_range(start_date: datetime, end_date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> Tuple[str, str]:
    """
    Format date range to SQL datetime strings.
    
    Args:
        start_date: Start datetime
        end_date: End datetime
        format_str: Format string (default: SQL datetime format)
        
    Returns:
        Tuple of (start_str, end_str)
    """
    # Start: beginning of day
    start_str = start_date.strftime("%Y-%m-%d 00:00:00")
    # End: end of day
    end_str = end_date.strftime("%Y-%m-%d 23:59:59")
    return start_str, end_str

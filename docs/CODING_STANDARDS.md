# OQR Dashboard - Coding Standards

## Overview
This document defines the coding standards and best practices for the OQR Dashboard project.

## Python Version
- **Target**: Python 3.8+
- **Development**: Use Python 3.10+

## Code Style

### PEP 8 Compliance
```python
# ✅ Good
def get_customer_data(customer_id: int, include_orders: bool = True) -> dict:
    """Fetch customer data with optional order history."""
    pass

# ❌ Bad
def getCustomerData(id,includeOrders=True):
    #fetch data
    pass
```

### Line Length
- **Maximum**: 100 characters (Streamlit-friendly)
- **Exception**: URLs, long strings (limit to reasonable breakpoints)

```python
# ✅ Good
query = (
    "SELECT * FROM orders "
    "WHERE status = %s AND date > %s"
)

# ❌ Bad
query = "SELECT * FROM orders WHERE status = %s AND date > %s AND brand = %s AND platform = %s AND ..."
```

## Naming Conventions

### Constants
```python
# ✅ Good - All caps with underscores
DB_HOST = "localhost"
CACHE_TTL_SECONDS = 600
DEFAULT_PAGE_SIZE = 50
MAX_CONNECTIONS = 10

# ❌ Bad
db_host = "localhost"
cacheTtl = 600
default_page_size = 50
```

### Variables & Functions
```python
# ✅ Good - Lowercase with underscores
start_date = datetime.now()
customer_name = "John Doe"

def fetch_customer_data(customer_id: int) -> dict:
    pass

# ❌ Bad
startDate = datetime.now()
customerName = "John Doe"

def FetchCustomerData(id):
    pass
```

### Classes
```python
# ✅ Good - PascalCase
class DataService:
    pass

class KPICalculator:
    pass

# ❌ Bad
class data_service:
    pass

class kpiCalculator:
    pass
```

### Private Functions/Methods
```python
# ✅ Good - Leading underscore
def _internal_helper(data: list) -> dict:
    """Internal helper not part of public API."""
    pass

class DataService:
    def _validate_input(self, value: str) -> bool:
        pass

# ❌ Bad
def internal_helper(data):
    pass
```

## Imports

### Order
```python
# 1. Future imports (if needed)
from __future__ import annotations

# 2. Standard library
import os
import sys
from datetime import datetime
from typing import Optional, List, Dict, Tuple

# 3. Third-party
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

# 4. Local/Application
import config
from src.db.connection import get_engine
from src.services.data_service import get_kpi_data
from ui.filters import render_filter_section
```

### Specific Rules
- ✅ Use absolute imports: `from src.services.data_service import ...`
- ❌ Avoid relative imports: `from .services.data_service import ...`
- ✅ Import specific names when possible: `from config import DB_HOST`
- ❌ Avoid wildcard imports: `from utils import *`
- ✅ Group and separate import sections with blank lines
- ❌ Don't mix import styles in same module

## Type Hints

### Function Signatures
```python
# ✅ Good - Always include type hints
def fetch_data(
    query: str,
    engine: Engine,
    params: Optional[Tuple[str, ...]] = None,
) -> pd.DataFrame:
    """Fetch data from database."""
    pass

# ❌ Bad - Missing type hints
def fetch_data(query, engine, params=None):
    pass
```

### Variable Annotations
```python
# ✅ Good
customer_count: int = 100
filter_options: Dict[str, List[str]] = {}
processed_data: Optional[pd.DataFrame] = None

# ❌ Bad
customer_count = 100
filter_options = {}
processed_data = None
```

### Common Types
```python
from typing import (
    Optional,      # Can be None
    Union,        # Multiple types
    List,         # List of items
    Dict,         # Dictionary
    Tuple,        # Fixed-size tuple
    Callable,     # Function
    Any,          # Anything
)

# Examples
def func(
    name: str,
    age: Optional[int] = None,
    items: List[str] = None,
    config: Dict[str, Any] = None,
    callback: Callable[[int], str] = None,
) -> Union[str, None]:
    pass
```

## Docstrings

### Google Style (Preferred)
```python
def fetch_kpi_data(
    start_date: str,
    end_date: str,
    filters: Dict[str, List[str]],
) -> pd.DataFrame:
    """Fetch KPI metrics for given period and filters.
    
    Retrieves revenue, orders, and AOV metrics from the database,
    including period-over-period growth calculations.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        filters: Dictionary with brand, platform, shop, status filters
        
    Returns:
        DataFrame with columns: Revenue, Orders, AOV, RevenueGrowth,
        OrdersGrowth, AovGrowth
        
    Raises:
        ValueError: If date format is invalid
        DatabaseError: If database query fails
        
    Example:
        >>> data = fetch_kpi_data("2024-01-01", "2024-01-31", {})
        >>> print(data["Revenue"].sum())
        1234567
    """
    pass
```

### Module Docstring
```python
"""
Data service module.

Handles all data fetching, transformation, and aggregation logic.
Provides high-level functions for dashboard data operations.

Example:
    >>> from src.services.data_service import get_kpi_data
    >>> kpi = get_kpi_data(start_str, end_str, filters, engine)
"""
```

### Class Docstring
```python
class KPICalculator:
    """Calculate KPI metrics from sales data.
    
    Attributes:
        engine (Engine): SQLAlchemy database engine
        cache_ttl (int): Cache time-to-live in seconds
    """
    
    def __init__(self, engine: Engine, cache_ttl: int = 600):
        """Initialize KPI calculator.
        
        Args:
            engine: SQLAlchemy Engine instance
            cache_ttl: Cache time-to-live (default: 600 seconds)
        """
        pass
```

## Error Handling

### Try-Except Pattern
```python
# ✅ Good - Specific exceptions, proper logging
try:
    df = fetch_data(query, engine)
except ValueError as e:
    logger.error(f"Invalid query format: {e}")
    st.error("Query validation failed")
except Exception as e:
    logger.exception("Unexpected error in fetch_data")
    st.error("Data fetch failed")

# ❌ Bad - Bare except, poor error info
try:
    df = fetch_data(query, engine)
except:
    print("Error!")
```

### Logging
```python
from src.logger import get_logger

logger = get_logger(__name__)

# ✅ Good - Appropriate log levels
logger.debug("Starting data fetch")
logger.info(f"Fetched {len(df)} rows")
logger.warning("Slow query detected: 5 seconds")
logger.error(f"Query failed: {error_msg}")
logger.exception("Unexpected error")  # Includes traceback

# ❌ Bad - Using print
print("Starting fetch")
print(f"Got {len(df)} rows")
```

## Code Organization

### Module Structure
```python
# Module docstring
"""
Module description.
"""

# Imports (organized by section)
from typing import Optional
import streamlit as st
import config
from src.logger import get_logger

# Logger setup
logger = get_logger(__name__)

# Constants (module-level)
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Main functions
def public_function():
    """Public API function."""
    pass

# Helper functions
def _private_helper():
    """Private helper function."""
    pass

# Classes
class MyClass:
    """Class docstring."""
    pass
```

### Function Size
- **Ideal**: < 50 lines
- **Maximum**: 100 lines
- **Guideline**: If > 100 lines, consider breaking into smaller functions

```python
# ✅ Good - Focused function
def validate_date_range(start: str, end: str) -> bool:
    """Validate date range format."""
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        return start_date <= end_date
    except ValueError:
        return False

# ❌ Bad - Too many responsibilities
def process_and_validate_and_fetch_and_transform_data(...):
    # 200 lines of mixed logic
    pass
```

## Streamlit-Specific

### Caching
```python
# ✅ Good - Use appropriate cache decorators
@st.cache_resource
def get_engine():
    """Cache database engine for lifetime."""
    return create_engine(...)

@st.cache_data(ttl=600)
def fetch_data(query: str, engine) -> pd.DataFrame:
    """Cache data for 10 minutes."""
    return pd.read_sql(query, engine)

# ❌ Bad - Over-caching or unnecessary dependencies
@st.cache_data
def get_user_input():
    return st.text_input("Name")  # User input should NOT be cached!
```

### UI Components
```python
# ✅ Good - Reusable components
def render_kpi_card(title: str, value: str, growth: float) -> None:
    """Render single KPI card."""
    st.markdown(...)

def render_filter_section() -> Dict[str, List[str]]:
    """Render all filters and return selections."""
    # Implementation
    pass

# ❌ Bad - Inline everything in main function
# Large chunks of UI code in app.py
```

## Configuration

### Use config.py for All Settings
```python
# ✅ Good
from config import DB_HOST, CACHE_TTL

# ❌ Bad
DB_HOST = "hardcoded_value"
CACHE_TTL = 600
```

## Comments & Documentation

### When to Comment
```python
# ✅ Good - Explains WHY, not WHAT
def calculate_aov(revenue: float, orders: int) -> float:
    """Average Order Value - core KPI for dashboard."""
    # Avoid division by zero edge case
    if orders == 0:
        return 0
    return revenue / orders

# ❌ Bad - Obvious comments
# Calculate AOV
aov = revenue / orders

# ❌ Bad - Misleading comments
# Return the value
return result
```

### Inline Comments
```python
# ✅ Good - Clarifies non-obvious logic
prev_end = start_date - timedelta(days=1)  # YoY period ends day before current start
prev_start = prev_end - delta  # Match period length

# ❌ Bad - States the obvious
x = x + 1  # Add one to x
```

## Testing

### Function Testability
```python
# ✅ Good - Pure function, easy to test
def format_currency(value: float) -> str:
    """Format number as currency string."""
    return f"${value:,.2f}"

# Test:
assert format_currency(1234.5) == "$1,234.50"

# ❌ Bad - Has side effects, hard to test
def display_currency(value: float):
    """Show currency on screen."""
    st.write(f"${value:,.2f}")  # Can't easily test
```

## Common Patterns

### Database Operations
```python
@st.cache_data(ttl=600)
def fetch_data(query: str, _engine: Engine, params: Optional[Tuple] = None) -> pd.DataFrame:
    """Fetch data with proper error handling."""
    try:
        df = pd.read_sql(query, _engine, params=params)
        logger.info(f"Fetched {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Query failed: {e}")
        return pd.DataFrame()
```

### UI State Management
```python
def checkbox_filter(label: str, options: List[str], key: str) -> List[str]:
    """Multi-select filter with session state."""
    if f"{key}_sel" not in st.session_state:
        st.session_state[f"{key}_sel"] = options
    
    # Render and return selection
    return st.session_state[f"{key}_sel"]
```

## Tools & Auto-formatting

### Recommended Tools
- **Linting**: `flake8` - Check code style
- **Formatting**: `black` - Auto-format code
- **Type Checking**: `mypy` - Static type validation

### Setup
```bash
pip install black flake8 mypy

# Format code
black src/ ui/ app.py

# Check style
flake8 src/ ui/ app.py --max-line-length=100

# Type check
mypy src/ ui/ --ignore-missing-imports
```

## Checklist for Code Review

- [ ] Type hints on all functions
- [ ] Docstrings present (Google style)
- [ ] Error handling with proper logging
- [ ] No hardcoded values (use config.py)
- [ ] No wildcard imports
- [ ] Functions < 100 lines
- [ ] Clear variable names (not a, b, x)
- [ ] PEP 8 compliant
- [ ] No commented-out code
- [ ] Appropriate cache decorators for Streamlit
- [ ] Specific exception handling (not bare except)
- [ ] Constants in UPPER_CASE
- [ ] Private functions prefixed with _

---

**Version**: 1.0  
**Last Updated**: February 2025

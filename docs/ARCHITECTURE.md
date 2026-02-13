# OQR Dashboard - Refactoring Documentation

## Overview
The OQR Dashboard has been refactored from a monolithic structure into a clean, modular architecture following Python best practices and PEP8 standards.

## Project Structure

```
x:\Streamlit\
├── app.py                          # Main entry point (thin layer)
├── config.py                       # Centralized configuration
├── requirements.txt                # Project dependencies
├── .env.example                    # Environment variables template
├── README.md                       # Project README
│
├── src/                            # Source code package
│   ├── __init__.py
│   ├── logger.py                   # Logging configuration
│   ├── db/
│   │   ├── __init__.py
│   │   └── connection.py           # Database connection pooling
│   ├── services/
│   │   ├── __init__.py
│   │   └── data_service.py         # Data fetching & transformations
│   └── utils/
│       ├── __init__.py
│       ├── formatters.py           # Display formatting (currency, numbers)
│       ├── sql_helpers.py          # SQL building & escaping
│       ├── query_manager.py        # SQL file loading
│       └── date_helpers.py         # Date operations
│
├── ui/                             # UI components
│   ├── __init__.py
│   ├── styles.py                   # CSS & styling
│   ├── filters.py                  # Filter UI components
│   ├── kpi_cards.py                # KPI card rendering
│   ├── charts.py                   # Plotly charts
│   └── data_tables.py              # Table rendering
│
├── query/                          # SQL query files (unchanged)
│   ├── GET_BRAND.sql
│   ├── GET_SHOP.sql
│   └── ...
│
├── docs/                           # Documentation
│   └── ARCHITECTURE.md             # This file
│
├── app_old.py                      # Backup of old monolithic app
├── db_config.py                    # (Legacy - can be removed)
├── utils.py                        # (Legacy - functionality moved to src/)
└── test_connection.py              # (Legacy - can be removed)
```

## Key Changes & Benefits

### 1. **Centralized Configuration (config.py)**
- Database settings
- UI constants
- Cache TTL settings
- Query file mappings
- Error messages
- **Benefit**: Single source of truth, easy to manage settings

### 2. **Database Layer (src/db/connection.py)**
- Connection pooling with SQLAlchemy
- Proper error handling
- Resource cleanup
- Caching with `@st.cache_resource`
- **Benefit**: Reliable, efficient database connections

### 3. **Data Service Layer (src/services/data_service.py)**
- Separated data fetching logic
- Transformation & aggregation
- Caching with `@st.cache_data`
- Specific functions for each query type (KPI, trend, status, province)
- **Benefit**: Reusable, testable, maintainable data operations

### 4. **Utilities (src/utils/)**
- **formatters.py**: Number/currency formatting, growth arrows
- **sql_helpers.py**: Filter building, SQL escaping
- **query_manager.py**: Load queries from files
- **date_helpers.py**: Date calculations, range formatting
- **Benefit**: Modular, single-purpose functions

### 5. **UI Components (ui/)**
- **styles.py**: Centralized CSS
- **filters.py**: Filter popover components (reusable)
- **kpi_cards.py**: KPI card rendering
- **charts.py**: Plotly chart rendering
- **data_tables.py**: Table rendering with styling
- **Benefit**: Modular, reusable UI components

### 6. **Logging (src/logger.py)**
- Centralized logging configuration
- Console + optional file logging
- Module-specific loggers
- **Benefit**: Better debugging, production monitoring

### 7. **Thin Entry Point (app.py)**
- Only orchestration logic
- Imports & calls components
- ~60 lines vs. 260 lines
- **Benefit**: Clear, maintainable main flow

## Coding Standards

### Naming Conventions
```python
# Classes: PascalCase
class DataService:
    pass

# Functions: snake_case
def get_kpi_data(start_date, end_date):
    pass

# Constants: UPPER_CASE
DB_HOST = "localhost"

# Private: leading underscore
def _internal_helper():
    pass
```

### Imports Order
```python
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party
import streamlit as st
import pandas as pd

# 3. Local
import config
from src.services.data_service import get_kpi_data
from ui.filters import render_filter_section
```

### Docstrings (Google Style)
```python
def fetch_data(query: str, engine: Engine, params: Optional[Tuple] = None) -> pd.DataFrame:
    """Fetch data from database using SQL query.
    
    Args:
        query: SQL query string
        engine: SQLAlchemy Engine instance
        params: Query parameters tuple (optional)
        
    Returns:
        DataFrame with query results
        
    Raises:
        Exception: If query execution fails
    """
```

### Error Handling
```python
try:
    data = fetch_data(query, engine)
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    st.error("Input validation failed")
except Exception as e:
    logger.exception("Unexpected error in fetch_data")
    st.error("Operation failed")
```

## Migration Guide

### For Developers
1. Use `config.py` for all constants - **never hardcode**
2. Import from specific modules: `from src.services.data_service import get_kpi_data`
3. Use `get_logger(__name__)` in each module
4. Follow naming conventions (see above)
5. Add docstrings to all functions
6. Use type hints: `def func(x: int) -> str:`

### Old vs. New

**Old Code:**
```python
from utils import load_query, format_currency, fetch_data
# load_query returns query
# format_currency, format_number mixed in same module
# fetch_data with no error handling
```

**New Code:**
```python
from src.utils.query_manager import load_query
from src.utils.formatters import format_currency
from src.services.data_service import fetch_data
# Clear purpose of each module
# Proper error handling & logging
```

## Performance Considerations

### Caching
- **Data queries**: `@st.cache_data(ttl=600)` - 10 minutes
- **Filter options**: `@st.cache_data(ttl=3600)` - 1 hour
- **DB connection**: `@st.cache_resource` - lifetime

### Database
- Connection pooling: 10 connections, max 20 overflow
- Pool recycle: 3600 seconds
- Timeout: 30 seconds

### Optimization Tips
1. Adjust cache TTL in `config.py` based on data update frequency
2. Use `LIMIT` in SQL queries for large result sets
3. Index frequently filtered columns in database
4. Monitor logs for slow queries

## Testing

### Running the App
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

### Manual Testing Checklist
- [ ] Date filter works correctly
- [ ] Brand/Platform/Shop/Status filters update properly
- [ ] KPI metrics display and calculate growth correctly
- [ ] Hourly trend chart renders without errors
- [ ] Status and Province tables show data with totals
- [ ] No duplicate database connections
- [ ] Logs appear in console (if enabled)

### Automated Testing (Future)
```bash
pip install pytest pytest-cov
pytest tests/
```

## Logging

Logs are configured in `src/logger.py`. To enable file logging:

1. Set `LOG_FILE` in environment or `.env`:
   ```bash
   LOG_FILE=logs/dashboard.log
   ```

2. Adjust log level:
   ```bash
   LOG_LEVEL=DEBUG  # For development
   LOG_LEVEL=INFO   # For production
   ```

3. View logs:
   ```bash
   tail -f logs/dashboard.log  # Linux/Mac
   type logs\dashboard.log     # Windows
   ```

## Future Enhancements

1. **Multi-page Dashboard**: Create `pages/` directory with separate modules
2. **Caching**: Add Redis caching for distributed deployments
3. **API Layer**: FastAPI backend for data queries
4. **Testing**: Unit tests for services, integration tests for database
5. **CI/CD**: GitHub Actions for automated testing & deployment
6. **Monitoring**: Prometheus metrics, alerting

## File Removal Notes

The following old files can be safely removed after verifying the new structure works:
- `app_old.py` - Backup of old app
- `db_config.py` - Functionality moved to `src/db/connection.py`
- `utils.py` - Functionality split across `src/utils/` and `src/services/`
- `test_connection.py` - Testing moved to proper test structure

## Support & Questions

For issues or questions:
1. Check the logs: `LOG_LEVEL=DEBUG streamlit run app.py`
2. Review relevant module docstrings
3. Check `config.py` for settings
4. Review error messages in Streamlit UI

## Version History

### v2.0 (Refactored - Current)
- Modular architecture
- Centralized configuration
- Proper logging
- PEP8 compliant
- Better error handling

### v1.0 (Legacy)
- Monolithic app.py
- Hardcoded constants
- Limited error handling
- All logic in one file

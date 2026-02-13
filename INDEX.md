# 📑 OQR Dashboard - File Index & Quick Reference

## 🎯 Start Here

**New to project?** Start with these files in order:

1. [README.md](README.md) - Overview & quick start (5 min)
2. [docs/SETUP.md](docs/SETUP.md) - Installation guide (10 min)
3. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - How it works (20 min)
4. [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md) - Code guidelines (15 min)

---

## 📁 File Structure & Purpose

### 🚀 Application Entry Point
```
app.py                    # Main application - thin orchestration layer (~60 lines)
config.py                 # Centralized configuration - ALL constants go here
```

### 🗄️ Database Layer
```
src/db/
├── __init__.py
└── connection.py         # SQLAlchemy engine, connection pooling, resource management
```

### 📊 Business Logic
```
src/services/
├── __init__.py
└── data_service.py       # Data fetching, transformation, caching
                          # Functions: get_kpi_data, get_trend_data, get_status_summary, etc.
```

### 🛠️ Utility Functions
```
src/utils/
├── __init__.py
├── formatters.py         # Format data: format_currency, format_number, get_growth_arrow
├── sql_helpers.py        # SQL building: build_filters, escape_sql_string
├── query_manager.py      # Load SQL: load_query, get_query_by_key
└── date_helpers.py       # Date operations: get_previous_period, format_date_range
```

### 🪵 Logging
```
src/logger.py             # Centralized logging setup, get_logger function
```

### 🎨 User Interface
```
ui/
├── __init__.py
├── styles.py             # CSS/HTML styling, inject_styles function
├── filters.py            # Filter components: checkbox_filter, render_filter_section
├── kpi_cards.py          # KPI cards: render_kpi_card, render_kpi_section
├── charts.py             # Charts: render_hourly_trend_chart
└── data_tables.py        # Tables: render_status_table, render_province_table
```

### 📚 Documentation
```
docs/
├── ARCHITECTURE.md       # System design, patterns, best practices
├── SETUP.md              # Installation, deployment, troubleshooting
├── CODING_STANDARDS.md   # Code style, naming, conventions
└── MIGRATION_COMPLETED.md # This refactoring summary
```

### 📝 Configuration Files
```
requirements.txt          # Python dependencies (pip install -r requirements.txt)
.env.example             # Environment variables template (copy to .env)
.gitignore               # Git ignore patterns (if using version control)
```

### 🗂️ Data Files
```
query/                    # SQL query files
├── GET_BRAND.sql
├── GET_SHOP.sql
├── GET_PLATFORM.sql
├── GET_STATUS.sql
├── GET_ORDER_REVENUE_AOV.sql
├── get_Hourly_Trend.sql
├── GET_ORDER_STATUS.sql
├── GET_REVENUE_ORDER_PROVINCE.sql
└── ...

__pycache__/             # Python cache (ignore)
```

### 📦 Legacy Files (Can Remove)
```
app_old.py               # Backup of original monolithic app
db_config.py            # Old database config (moved to src/db/connection.py)
utils.py                # Old utilities (split into src/utils/*)
test_connection.py      # Old test script (can be removed)
```

---

## 🔍 Quick Lookup

### "I need to..."

#### Change database settings
→ Edit `config.py` (DB_HOST, DB_USER, etc.)

#### Add new UI filter
1. Create SQL query in `query/`
2. Add function in `src/services/data_service.py`
3. Add component in `ui/filters.py`
4. Update `app.py` main()

#### Fix date formatting
→ See `src/utils/date_helpers.py`

#### Change KPI calculations
→ Update SQL in `query/GET_ORDER_REVENUE_AOV.sql` or logic in `src/services/data_service.py`

#### Add new chart
1. Create function in `ui/charts.py`
2. Call in `app.py` after fetching data

#### Format currency/numbers
→ Use `src/utils/formatters.py` functions

#### Build SQL filters
→ Use `src/utils/sql_helpers.py::build_filters()`

#### Debug data fetching
1. Set `LOG_LEVEL=DEBUG` in `.env`
2. Check logs: `tail -f logs/dashboard.log`
3. Add logging: `logger.debug(f"Message: {value}")`

#### Check caching behavior
→ Review `@st.cache_data(ttl=...)` and `@st.cache_resource` in code

#### Handle database errors
→ See `src/db/connection.py` error handling

#### Write new utility function
→ Follow pattern in `src/utils/formatters.py` (docstring, type hints, error handling)

---

## 📊 Module Dependencies

```
app.py
├── config                                  # Settings
├── src.db.connection.get_engine           # DB engine
├── src.logger.get_logger                  # Logging
├── src.services.data_service              # All data functions
│   ├── src.utils.query_manager.load_query
│   ├── src.utils.sql_helpers.build_filters
│   └── src.db.connection (implied)
├── src.utils.sql_helpers.build_filters
├── src.utils.date_helpers.get_previous_period
├── ui.styles.inject_styles                # CSS
├── ui.filters.render_filter_section       # Filters
├── ui.kpi_cards.render_kpi_section        # KPI cards
├── ui.charts.render_hourly_trend_chart    # Chart
└── ui.data_tables.render_*_table          # Tables
```

---

## 🎓 Code Examples

### Example 1: Add New KPI Metric

**Step 1**: Update SQL in `query/GET_ORDER_REVENUE_AOV.sql`
```sql
SELECT 
    Revenue,
    Orders,
    AOV,
    RevenueGrowth,
    NewMetric  -- ← Add here
FROM ...
```

**Step 2**: Update UI in `ui/kpi_cards.py`
```python
def render_kpi_section(kpi_data):
    # ... existing code ...
    with k_cols[4]:  # Add 5th column if needed
        st.markdown(
            render_kpi_card(
                "New Metric",
                format_number(row.get("NewMetric", 0)),
                row.get("NewMetricGrowth", 0),
                config.CARD_STYLES["blue"],
            ),
            unsafe_allow_html=True,
        )
```

### Example 2: Add Logging

```python
from src.logger import get_logger

logger = get_logger(__name__)

def my_function():
    logger.debug("Starting operation")
    logger.info(f"Processed {count} items")
    logger.error(f"Error occurred: {error}")
```

### Example 3: Use Config

```python
# ✅ Correct
from config import DB_HOST, CACHE_TTL
engine = create_engine(DB_HOST)

# ❌ Wrong
DB_HOST = "192.168.1.119"  # Hardcoded!
```

---

## 📈 Import Guide

### For New Files

**Always follow this import order:**
```python
# 1. Standard library
from datetime import datetime
from typing import Optional

# 2. Third-party
import streamlit as st
import pandas as pd

# 3. Local
import config
from src.db.connection import get_engine
from ui.filters import render_filter_section
```

### Common Imports by Use Case

**Data fetching:**
```python
from src.services.data_service import get_kpi_data, get_trend_data, fetch_data
```

**Formatting:**
```python
from src.utils.formatters import format_currency, format_number, get_growth_arrow
```

**SQL operations:**
```python
from src.utils.sql_helpers import build_filters, escape_sql_string
from src.utils.query_manager import load_query, get_query_by_key
```

**UI components:**
```python
from ui.filters import checkbox_filter, render_filter_section
from ui.kpi_cards import render_kpi_section
from ui.charts import render_hourly_trend_chart
from ui.data_tables import render_status_table
```

**Database:**
```python
from src.db.connection import get_engine
```

**Logging:**
```python
from src.logger import get_logger
logger = get_logger(__name__)
```

---

## 🧪 Testing Quick Reference

### Test imports work
```bash
python -c "from app import main; print('OK')"
```

### Test database connection
```bash
python -c "from src.db.connection import get_engine; engine = get_engine(); print('Connected' if engine else 'Failed')"
```

### Run app
```bash
streamlit run app.py
```

### Debug mode
```bash
LOG_LEVEL=DEBUG streamlit run app.py
```

---

## 🚀 Deployment Quick Links

- **Local development**: See [docs/SETUP.md#initial-setup](docs/SETUP.md)
- **Production deployment**: See [docs/SETUP.md#production-deployment](docs/SETUP.md)
- **Docker deployment**: See [docs/SETUP.md#docker-deployment](docs/SETUP.md)
- **Streamlit Cloud**: See [docs/SETUP.md#streamlit-cloud](docs/SETUP.md)

---

## 📊 Performance Tips

1. **Slow queries?** → Optimize SQL, add indexes, reduce date range
2. **Memory leak?** → Check for infinite loops, clear cache: `streamlit cache clear`
3. **Slow UI?** → Increase CACHE_TTL in config.py
4. **DB connection errors?** → Check credentials in .env, verify MySQL running

---

## 🐛 Debugging Guide

| Issue | Where to look |
|-------|---------------|
| Import error | Check __init__.py files exist in all packages |
| Database connection failed | Check .env, verify MySQL running |
| Data not showing | Check SQL queries, verify date range, check filters |
| Cache stale | Run `streamlit cache clear` |
| Slow performance | Check logs for slow queries, increase cache TTL |
| UI component broken | Check ui/*.py for the component |
| Data formatting wrong | Check src/utils/formatters.py |

---

## 📞 Getting Help

1. **Check logs**: `LOG_LEVEL=DEBUG streamlit run app.py`
2. **Read relevant docs**: SETUP.md, ARCHITECTURE.md, CODING_STANDARDS.md
3. **Review docstrings**: Most functions have detailed docstrings
4. **Check error messages**: Streamlit shows clear error messages

---

## ✅ Before You Commit Code

- [ ] Followed naming conventions
- [ ] Added type hints to all functions
- [ ] Added docstrings
- [ ] No hardcoded values (use config.py)
- [ ] Proper error handling with logging
- [ ] Code < 100 lines per function
- [ ] Tested locally: `streamlit run app.py`
- [ ] No import errors
- [ ] Reviewed docs/CODING_STANDARDS.md

---

## 🔗 Important Links

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview |
| [docs/SETUP.md](docs/SETUP.md) | How to set up locally |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical design |
| [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md) | Code style guide |
| [config.py](config.py) | All settings |
| [app.py](app.py) | Main entry point |

---

**Last Updated**: February 2025  
**Version**: 2.0 (Refactored)

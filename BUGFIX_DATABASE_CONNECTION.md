# 🔧 Fix Database Connection Error

## Error Fixed ✅

**Error Message:**
```
Kết nối database thất bại! Error: Not an executable object: 'SELECT 1'
```

**Root Cause:**
SQLAlchemy 2.0+ requires SQL strings to be wrapped in `text()` object when using `engine.connect()`.

**Solution Applied:**
Updated `src/db/connection.py` to import and use `text()` from sqlalchemy:

```python
# Before (Incorrect)
from sqlalchemy import create_engine, Engine, event
with engine.connect() as conn:
    conn.execute("SELECT 1")  # ❌ String not wrapped

# After (Correct)
from sqlalchemy import create_engine, Engine, event, text
with engine.connect() as conn:
    conn.execute(text("SELECT 1"))  # ✅ String wrapped in text()
```

---

## Verification ✅

Database connection has been tested successfully:

```bash
✓ Connected: Engine(mysql+pymysql://root:***@192.168.1.119:3306/omisell_db?charset=utf8mb4)
```

---

## Related Changes

The following file was updated:
- **src/db/connection.py** - Added `text` import, wrapped SQL in `text()`

No other changes needed. The app should now work correctly.

---

## Next Steps

1. Run the app:
   ```bash
   streamlit run app.py
   ```

2. Access browser:
   ```
   http://localhost:8501
   ```

3. Test filters and data display

---

## SQLAlchemy 2.0 Migration Notes

If you encounter similar errors with SQL strings:

**Pattern 1: Raw SQL with engine.connect()**
```python
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM table"))
```

**Pattern 2: Parameterized queries**
```python
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT * FROM orders WHERE id = :id"),
        {"id": 123}
    )
```

**Pattern 3: With pandas (already works)**
```python
import pandas as pd
from sqlalchemy import text
df = pd.read_sql(text("SELECT * FROM orders"), engine)
```

---

**Status:** ✅ FIXED  
**Date:** February 13, 2026  
**Tested:** OK

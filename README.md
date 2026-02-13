# OQR Dashboard

B2C Revenue & Orders Analytics Dashboard - Streamlit Application

## Quick Start

### Prerequisites
- Python 3.8+
- MySQL/MariaDB database
- pip package manager

### Installation

1. **Clone/Download Project**
   ```bash
   cd x:\Streamlit
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Copy template
   cp .env.example .env
   
   # Edit .env with your database credentials
   # DB_HOST=your_host
   # DB_USER=your_user
   # DB_PASSWORD=your_password
   # DB_NAME=your_database
   ```

5. **Run Application**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## Features

✨ **Key Features**
- 📊 Real-time revenue and order metrics (KPI cards)
- 📈 Hourly trend analysis with dual-axis charts
- 🔍 Multi-filter dashboard (Brand, Platform, Shop, Status, Date)
- 📱 Responsive layout (wide layout, optimized for desktop)
- ⚡ Fast data loading with caching (10-60 min)
- 🎨 Professional UI with custom styling
- 📋 Detailed tables (Order Status, Province Analytics)

## Project Structure

```
OQR Dashboard/
├── app.py                      # Main application entry point
├── config.py                   # Configuration & constants
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── src/                       # Source code
│   ├── db/                   # Database layer
│   ├── services/             # Business logic (data fetching)
│   ├── utils/                # Utility functions
│   └── logger.py             # Logging configuration
├── ui/                        # UI components
│   ├── filters.py            # Filter components
│   ├── kpi_cards.py          # KPI card display
│   ├── charts.py             # Chart rendering
│   └── data_tables.py        # Table components
├── query/                     # SQL query files
├── docs/                      # Documentation
└── __pycache__/              # (Ignore)
```

## Dashboard Sections

### 1. **Filters** (Top Section)
- **Date Range**: Select period for analysis
- **Brand**: Filter by brand (multi-select)
- **Platform**: Filter by e-commerce platform (Haravan, Lazada, etc.)
- **Shop**: Filter by shop name
- **Status**: Filter by order status

### 2. **KPI Cards** (4 Metrics)
- **Doanh Số (Revenue)**: Total revenue with growth %
- **Đơn Hàng (Orders)**: Total orders with growth %
- **AOV**: Average order value with growth %
- **Tăng trưởng (Growth)**: Period-over-period revenue growth

### 3. **Hourly Trend Chart**
- Dual-axis chart: Revenue (left) and Orders (right)
- X-axis: Hour of day (0-23)
- Interactive: Hover for details, zoom, pan

### 4. **Status Summary Table**
- Order count by status
- Color-coded gradient (blue = higher)
- Grand total at bottom

### 5. **Province Analytics Table**
- Top 20 provinces by orders/revenue
- Color-coded ordering
- Grand total aggregation

## Configuration

### Database Settings (config.py)
```python
DB_HOST = "192.168.1.119"      # Database host
DB_PORT = 3306                  # MySQL port
DB_USER = "root"               # Database user
DB_PASSWORD = "password"        # Database password
DB_NAME = "omisell_db"         # Database name
```

### Caching
```python
CACHE_TTL_DATA = 600           # Data cache: 10 minutes
CACHE_TTL_OPTIONS = 3600       # Options cache: 1 hour
```

### UI Customization
Edit `config.py`:
- `PLATFORMS`: Add/remove e-commerce platforms
- `CARD_STYLES`: Modify KPI card colors
- `CHART_HEIGHT`: Adjust chart heights
- `CHART_COLORS`: Change chart line colors

## Usage

### Basic Workflow
1. **Select Date Range**: Pick start and end date
2. **Apply Filters**: Choose Brand, Platform, Shop, Status
3. **View Results**: 
   - KPI cards update with filtered data
   - Charts and tables adjust automatically
   - Comparisons show vs. previous period

### Tips
- ✅ Use "Chọn tất cả" (Select All) to include everything
- ✅ Use "Bỏ hết" (Deselect All) to clear selection
- ✅ Hold Shift to select date ranges
- ✅ Hover over charts for detailed values
- ✅ Click chart elements to zoom/filter

## Development

### Code Structure
- **Single Responsibility**: Each module has one purpose
- **DRY (Don't Repeat)**: Common logic in utilities
- **SOLID Principles**: Separation of concerns
- **Type Hints**: For better IDE support and documentation
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: Centralized logging for debugging

### Adding New Filters
1. Add SQL query to `query/` folder
2. Add to `config.QUERY_FILES` mapping
3. Import in `src/services/data_service.py`
4. Add to filter section in `ui/filters.py`

### Adding New KPI Metrics
1. Update SQL query in `query/GET_ORDER_REVENUE_AOV.sql`
2. Add new column rendering in `ui/kpi_cards.py`
3. Update `config.KPI_TITLES` with new title

### Adding New Charts
1. Create function in `ui/charts.py`
2. Fetch data in `src/services/data_service.py`
3. Call from `app.py` main function

## Troubleshooting

### Database Connection Failed
- ✅ Check credentials in `.env` file
- ✅ Verify database server is running
- ✅ Test MySQL connection: `mysql -h host -u user -p database`
- ✅ Check network connectivity

### No Data Displayed
- ✅ Verify date range is correct
- ✅ Check SQL query files exist in `query/` folder
- ✅ Ensure filter selections are applied
- ✅ Check database has data for selected period

### Slow Performance
- ✅ Increase cache TTL in `config.py`
- ✅ Optimize SQL queries
- ✅ Add indexes to frequently filtered columns
- ✅ Reduce date range selection

### Import Errors
- ✅ Ensure all files are in correct folders
- ✅ Check `__init__.py` files exist in packages
- ✅ Verify Python path includes project root
- ✅ Run: `pip install -r requirements.txt`

### Logging & Debugging
```bash
# Enable debug logging
LOG_LEVEL=DEBUG streamlit run app.py

# View Streamlit logs
streamlit logs

# Check app cache
streamlit cache clear
```

## Database Schema

The dashboard expects these tables:
- `sales` or `orders`: Main orders table with Revenue, Orders, Platform, Brand, Shop, Status, DateTime
- Related tables for brands, shops, statuses

See `query/*.sql` files for expected column names.

## Performance Notes

### Caching
- Filter options cached for 1 hour (reduces DB queries)
- Query results cached for 10 minutes
- Database connections pooled (max 10 simultaneous)

### Optimization
- Queries should include date range filters
- Use indexes on: Brand, Platform, Shop, Status, DateTime
- Consider partitioning large tables by date

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Production (Streamlit Cloud)
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Set environment variables in secrets
4. Deploy

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.31.1 | Web framework |
| pandas | 2.1.4 | Data processing |
| sqlalchemy | 2.0.23 | ORM & database |
| pymysql | 1.1.0 | MySQL driver |
| plotly | 5.18.0 | Charts |

See `requirements.txt` for complete list.

## License

Internal use only

## Support

For issues or questions:
1. Check logs: `LOG_LEVEL=DEBUG streamlit run app.py`
2. Review `docs/ARCHITECTURE.md` for technical details
3. Check error messages in Streamlit UI
4. Review relevant module docstrings

---

**Last Updated**: February 2025  
**Version**: 2.0 (Refactored)

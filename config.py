"""
Configuration module for OQR Dashboard.
Centralized settings for database, UI, cache, and application constants.
"""

import os
from typing import Optional

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DB_HOST: str = os.getenv("DB_HOST", "192.168.1.119")
DB_PORT: int = int(os.getenv("DB_PORT", 3306))
DB_USER: str = os.getenv("DB_USER", "root")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "Oqr@18009413")
DB_NAME: str = os.getenv("DB_NAME", "omisell_db")
DB_CHARSET: str = "utf8mb4"

# Connection pooling
DB_POOL_SIZE: int = 10
DB_MAX_OVERFLOW: int = 20
DB_POOL_TIMEOUT: int = 30
DB_POOL_RECYCLE: int = 3600

# ============================================================================
# CACHE CONFIGURATION
# ============================================================================
CACHE_TTL_DATA: int = 600  # 10 minutes for data queries
CACHE_TTL_OPTIONS: int = 3600  # 1 hour for options (brand, shop, etc.)

# ============================================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================================
PAGE_CONFIG = {
    "page_title": "OQR Dashboard",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}

# ============================================================================
# UI CONSTANTS
# ============================================================================

# SQL Query Files Mapping
QUERY_FILES = {
    "kpi": "GET_ORDER_REVENUE_AOV.sql",
    "trend": "get_Hourly_Trend.sql",
    "status": "GET_ORDER_STATUS.sql",
    "province": "GET_REVENUE_ORDER_PROVINCE.sql",
    "brand": "GET_BRAND.sql",
    "shop": "GET_SHOP.sql",
    "platform": "GET_PLATFORM.sql",
    "order_status": "GET_STATUS.sql",
    "revenue_brand_platform": "GET_REVENUE_BRAND_PLATFORM.sql",
    "revenue_by_brand": "GET_REVENUE_BY_BRAND.sql",
    "revenue_by_platform": "GET_REVENUE_BY_PLATFORM.sql",
}

# Platform List (Static)
PLATFORMS: list[str] = ["Haravan", "Lazada", "Shopee", "Shopify", "Tiktok Shop"]

# Date Format
DATE_FORMAT: str = "DD/MM/YYYY"
SQL_DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT: str = "%Y-%m-%d"

# ============================================================================
# DASHBOARD TITLE & DESCRIPTIONS
# ============================================================================
DASHBOARD_TITLE: str = "📊 B2C Revenue & Orders Dashboard"
DASHBOARD_SUBTITLE: str = "📊 Phân tích chi tiết"

# KPI Card Titles
KPI_TITLES = {
    "revenue": "Doanh Số",
    "orders": "Đơn Hàng",
    "aov": "AOV",
    "growth": "Tăng trưởng",
}

# Table Titles
TABLE_TITLES = {
    "status": "Trạng Thái Đơn Hàng",
    "province": "Top Đơn Hàng Theo Tỉnh Thành",
}

# Filter Names & Keys
FILTERS = {
    "date": {"label": "Thời gian", "key": "date"},
    "brand": {"label": "Brand", "key": "br"},
    "platform": {"label": "Nền tảng", "key": "pl"},
    "shop": {"label": "ShopName", "key": "sh"},
    "status": {"label": "Trạng thái", "key": "st"},
}

# Chart Configuration
CHART_HEIGHT: int = 400
CHART_COLORS = {
    "revenue": "#ff7f0e",
    "orders": "#1f77b4",
    "primary": "#1e3a8a",
    "secondary": "#3b82f6",
}

# KPI Card Styles
CARD_STYLES = {
    "white": "card-white",
    "blue": "card-blue",
    "red": "card-red",
    "purple": "card-purple",
}

# ============================================================================
# SIDEBAR & NAVIGATION
# ============================================================================
SIDEBAR_MENU: list[dict] = [
    {"key": "overview", "label": "Overview", "icon": "📊"},
    {"key": "custom_report", "label": "Custom Report", "icon": "📋"},
    {"key": "shopee_fee", "label": "Shopee Fee", "icon": "🛍️"},
    {"key": "tiktok_fee", "label": "TikTok Shop Fee", "icon": "🎵"},
    {"key": "b2b_revenue", "label": "[B2B] Revenue & Orders", "icon": "🏢"},
    {"key": "accounting_check", "label": "Kế toán check", "icon": "🧮"},
    {"key": "fulfillment", "label": "Fulfillment", "icon": "📦"},
]

# Lazy import to avoid circular imports
SIDEBAR_MENU_MAP: dict = {}

def _init_menu_map():
    """Initialize sidebar menu map (lazy loading to avoid circular imports)."""
    from pages.overview import render_overview
    from pages.custom_report import render_custom_report
    from pages.shopee_fee import render_shopee_fee
    from pages.tiktok_fee import render_tiktok_fee
    from pages.b2b_revenue import render_b2b_revenue
    from pages.accounting_check import render_accounting_check
    from pages.fulfillment import render_fulfillment
    
    return {
        "overview": render_overview,
        "custom_report": render_custom_report,
        "shopee_fee": render_shopee_fee,
        "tiktok_fee": render_tiktok_fee,
        "b2b_revenue": render_b2b_revenue,
        "accounting_check": render_accounting_check,
        "fulfillment": render_fulfillment,
    }

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE: Optional[str] = os.getenv("LOG_FILE", None)  # None = console only

# ============================================================================
# DATE RANGE DEFAULTS
# ============================================================================
# Default lookback period (days)
DEFAULT_LOOKBACK_DAYS: int = 0  # Same day by default
MIN_DATE_STR: str = "2020-01-01"
MAX_DATE_STR: str = "2030-12-31"

# ============================================================================
# ERROR MESSAGES
# ============================================================================
ERROR_MESSAGES = {
    "db_connection": "Kết nối database thất bại!",
    "query_not_found": "Query file not found: {filename}",
    "data_fetch_failed": "Data fetch failed",
    "invalid_input": "Input validation failed",
}

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================
SUCCESS_MESSAGES = {
    "db_connected": "Database connected successfully",
}

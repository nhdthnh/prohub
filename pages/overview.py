"""
Overview page - Main B2C Revenue & Orders Dashboard
"""

import streamlit as st
from datetime import datetime

import config
from src.db.connection import get_engine
from src.logger import get_logger
from src.services.data_service import (
    get_filter_options_dict,
    get_kpi_data,
    get_trend_data,
    get_status_summary,
    get_province_data,
)
from src.utils.sql_helpers import build_filters
from src.utils.date_helpers import get_previous_period
from ui.filters import render_filter_section
from ui.kpi_cards import render_kpi_section
from ui.charts import render_hourly_trend_chart
from ui.data_tables import render_status_table, render_province_table

logger = get_logger(__name__)


def render_overview() -> None:
    """Render Overview page with main dashboard."""
    st.title("📊 B2C Revenue & Orders Dashboard")
    
    # Initialize database connection
    engine = get_engine()
    if not engine:
        st.stop()
    
    # Load filter options
    filter_opts = get_filter_options_dict(engine)
    
    # Prepare shop options with counts
    shop_with_counts = {shop: 0 for shop in filter_opts["shop"]}
    
    # Render filter section
    filters = render_filter_section(
        engine,
        brand_options=filter_opts["brand"],
        platform_options=filter_opts["platform"],
        shop_options=shop_with_counts,
        status_options=filter_opts["status"],
    )
    
    # Extract filters and dates
    start_date, end_date = filters["date_range"]
    start_str, end_str = filters["date_str"]
    
    # Calculate previous period for comparison
    p_start, p_end = get_previous_period(start_date, end_date)
    p_start_str = p_start.strftime("%Y-%m-%d 00:00:00")
    p_end_str = p_end.strftime("%Y-%m-%d 23:59:59")
    
    # Build SQL filters
    filter_sql = build_filters(
        filters["brand"],
        filters["platform"],
        filters["shop"],
        filters["status"],
    )
    
    # --- FETCH KPI DATA ---
    kpi_df = get_kpi_data(
        start_str, end_str,
        p_start_str, p_end_str,
        filter_sql,
        engine,
    )
    
    # --- RENDER KPI SECTION ---
    render_kpi_section(kpi_df)
    
    # --- RENDER 3 CHARTS IN ONE ROW ---
    st.divider()
    st.subheader(config.DASHBOARD_SUBTITLE)
    
    # Fetch data for all 3 visualizations
    trend_df = get_trend_data(start_str, end_str, filter_sql, engine)
    status_df = get_status_summary(start_str, end_str, filter_sql, engine)
    province_df = get_province_data(start_str, end_str, filter_sql, engine)
    
    # Create 3 equal columns
    col1, col2, col3 = st.columns(3)
    
    # Trend chart (left)
    with col1:
        render_hourly_trend_chart(trend_df)
    
    # Status table (middle)
    with col2:
        render_status_table(status_df)
    
    # Province table (right)
    with col3:
        render_province_table(province_df)
    
    logger.info("Overview page rendered successfully")

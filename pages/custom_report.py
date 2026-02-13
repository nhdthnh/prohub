"""
Custom Report page - Brand and Platform Analysis
"""

import streamlit as st
from datetime import datetime

import config
from src.db.connection import get_engine
from src.logger import get_logger
from src.services.data_service import (
    get_filter_options_dict,
    get_revenue_by_brand_platform,
    get_revenue_by_brand,
    get_revenue_by_platform,
)
from src.utils.sql_helpers import build_filters
from src.utils.date_helpers import get_previous_period
from ui.filters import render_filter_section
from ui.charts import render_stacked_bar_chart, render_pie_chart
from ui.data_tables import render_status_table

logger = get_logger(__name__)


def render_custom_report() -> None:
    """Render Custom Report page with Brand and Platform analysis."""
    st.title("📋 Custom Report - Brand & Platform Analysis")
    
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
    
    # Build SQL filters
    filter_sql = build_filters(
        filters["brand"],
        filters["platform"],
        filters["shop"],
        filters["status"],
    )
    
    # --- SECTION 1: REVENUE BY BRAND & PLATFORM ---
    st.divider()
    st.subheader("🏢 Doanh Số Theo Brand Và Nền Tảng")
    
    col1, col2 = st.columns([1.5, 1])
    
    # Stacked bar chart
    with col1:
        brand_platform_df = get_revenue_by_brand_platform(
            start_str, end_str, filter_sql, engine
        )
        if not brand_platform_df.empty:
            render_stacked_bar_chart(
                brand_platform_df,
                category_col="brand",
                platform_col="PlatformName"
            )
        else:
            st.info("Không có dữ liệu")
    
    # Revenue by Brand table
    with col2:
        brand_data = get_revenue_by_brand(start_str, end_str, filter_sql, engine)
        if not brand_data.empty:
            st.markdown("#### Tỷ Trọng Doanh Số Theo Brand")
            display_data = brand_data[["Brand", "Revenue", "Orders", "RevenuePercent"]].copy()
            display_data.columns = ["Brand", "Doanh Số", "Đơn Hàng", "% Doanh Số"]
            display_data["Doanh Số"] = display_data["Doanh Số"].apply(lambda x: f"{x:,.0f}")
            
            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True,
                height=320,
            )
            
            total_revenue = brand_data["Revenue"].sum()
            st.markdown(f"**Grand total: {total_revenue:,.0f}**")
        else:
            st.info("Không có dữ liệu")
    
    # --- SECTION 2: BRAND & PLATFORM PROPORTIONS ---
    st.divider()
    st.subheader("📊 Tỷ Trọng Doanh Số")
    
    col1, col2 = st.columns(2)
    
    # Pie chart - Brand
    with col1:
        st.markdown("#### Theo Brand")
        brand_data = get_revenue_by_brand(start_str, end_str, filter_sql, engine)
        if not brand_data.empty:
            render_pie_chart(brand_data, label_col="Brand", value_col="Revenue")
        else:
            st.info("Không có dữ liệu")
    
    # Pie chart - Platform
    with col2:
        st.markdown("#### Theo Nền Tảng")
        platform_data = get_revenue_by_platform(start_str, end_str, filter_sql, engine)
        if not platform_data.empty:
            render_pie_chart(platform_data, label_col="PlatformName", value_col="Revenue")
        else:
            st.info("Không có dữ liệu")
    
    # --- SECTION 3: DETAILED TABLES ---
    st.divider()
    st.subheader("📋 Chi Tiết Theo Nền Tảng")
    
    col1, col2 = st.columns(2)
    
    # Brand table
    with col1:
        brand_data = get_revenue_by_brand(start_str, end_str, filter_sql, engine)
        if not brand_data.empty:
            st.markdown("#### Doanh Số Theo Brand")
            display_data = brand_data[["Brand", "Revenue", "Orders", "RevenuePercent"]].copy()
            display_data.columns = ["Brand", "Doanh Số", "Đơn Hàng", "% Δ"]
            display_data["Doanh Số"] = display_data["Doanh Số"].apply(lambda x: f"{x:,.0f}")
            
            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True,
                height=320,
            )
            
            total = brand_data["Revenue"].sum()
            st.markdown(f"**Grand total: {total:,.0f}**")
        else:
            st.info("Không có dữ liệu")
    
    # Platform table
    with col2:
        platform_data = get_revenue_by_platform(start_str, end_str, filter_sql, engine)
        if not platform_data.empty:
            st.markdown("#### Doanh Số Theo Nền Tảng")
            display_data = platform_data[["PlatformName", "Revenue", "Orders", "RevenuePercent"]].copy()
            display_data.columns = ["Platform", "Doanh Số", "Đơn Hàng", "% Δ"]
            display_data["Doanh Số"] = display_data["Doanh Số"].apply(lambda x: f"{x:,.0f}")
            
            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True,
                height=320,
            )
            
            total = platform_data["Revenue"].sum()
            st.markdown(f"**Grand total: {total:,.0f}**")
        else:
            st.info("Không có dữ liệu")
    
    logger.info("Custom Report page rendered successfully")

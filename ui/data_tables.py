"""
Data table UI components.
"""

from typing import Optional
import streamlit as st
import pandas as pd

import config
from src.utils.formatters import format_number
from src.logger import get_logger

logger = get_logger(__name__)


def render_status_table(status_data: pd.DataFrame) -> None:
    """
    Render order status summary table.
    
    Args:
        status_data: DataFrame with Status and Orders columns
    """
    st.markdown(f"#### {config.TABLE_TITLES['status']}")
    
    if status_data.empty:
        st.info("Không có dữ liệu trạng thái")
        return
    
    try:
        # Style and display dataframe with fixed height
        st.dataframe(
            status_data.style.background_gradient(
                cmap="Blues",
                subset=["Orders"] if "Orders" in status_data.columns else [],
            ),
            use_container_width=True,
            hide_index=True,
            height=320,
        )
        
        # Display total
        total = status_data["Orders"].sum() if "Orders" in status_data.columns else 0
        st.markdown(f"**Grand total: {format_number(total)}**")
        logger.info(f"Status table rendered: {len(status_data)} rows, total={total}")
    
    except Exception as e:
        logger.error(f"Error rendering status table: {e}")
        st.error(f"Status Table Error: {e}")


def render_province_table(province_data: pd.DataFrame) -> None:
    """
    Render top provinces table by orders/revenue.
    
    Args:
        province_data: DataFrame with Province, Orders, Revenue columns
    """
    st.markdown(f"#### {config.TABLE_TITLES['province']}")
    
    if province_data.empty:
        st.info("Không có dữ liệu tỉnh thành")
        return
    
    try:
        # Style and display dataframe with fixed height
        st.dataframe(
            province_data.style.background_gradient(
                cmap="Blues",
                subset=["Orders"] if "Orders" in province_data.columns else [],
            ),
            use_container_width=True,
            hide_index=True,
            height=320,
        )
        
        # Display total
        total = province_data["Orders"].sum() if "Orders" in province_data.columns else 0
        st.markdown(f"**Grand total: {format_number(total)}**")
        logger.info(f"Province table rendered: {len(province_data)} rows, total={total}")
    
    except Exception as e:
        logger.error(f"Error rendering province table: {e}")
        st.error(f"Province Table Error: {e}")

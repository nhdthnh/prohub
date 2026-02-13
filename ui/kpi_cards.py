"""
KPI card UI components.
"""

from typing import Optional, Dict
import streamlit as st

import config
from src.utils.formatters import format_currency, format_number, get_growth_arrow
from src.logger import get_logger

logger = get_logger(__name__)


def render_kpi_card(
    title: str,
    value: str,
    growth: float,
    style: str = "card-white",
) -> str:
    """
    Generate HTML for KPI metric card.
    
    Args:
        title: Card title
        value: Formatted value to display
        growth: Growth percentage
        style: CSS class name (card-white, card-blue, card-red, card-purple)
        
    Returns:
        HTML string for the card
    """
    arrow = get_growth_arrow(growth)
    html = f"""<div class="metric-card {style}">
<div style="font-size:14px; opacity:0.9">{title}</div>
<div style="font-size:26px; font-weight:bold; margin: 8px 0;">{value}</div>
<div style="font-size:13px">{arrow} {abs(growth):.1f}% so với kỳ trước</div>
</div>"""
    return html


def render_kpi_section(kpi_data) -> None:
    """
    Render KPI metrics section with 4 cards.
    
    Args:
        kpi_data: DataFrame with KPI metrics
    """
    st.write("")
    k_cols = st.columns(4)
    
    if kpi_data.empty:
        st.warning("Không có dữ liệu KPI")
        return
    
    try:
        row = kpi_data.iloc[0]
        logger.info(f"KPI row data: Revenue={row.get('Revenue')}, Orders={row.get('Orders')}, AOV={row.get('AOV')}")
        
        with k_cols[0]:
            revenue_val = row.get("Revenue", 0)
            revenue_growth = row.get("RevenueGrowth", 0)
            logger.info(f"Rendering Revenue card: value={revenue_val}, growth={revenue_growth}")
            
            st.markdown(
                render_kpi_card(
                    config.KPI_TITLES["revenue"],
                    format_currency(revenue_val),
                    revenue_growth,
                    config.CARD_STYLES["white"],
                ),
                unsafe_allow_html=True,
            )
        
        with k_cols[1]:
            orders_val = row.get("Orders", 0)
            orders_growth = row.get("OrdersGrowth", 0)
            logger.info(f"Rendering Orders card: value={orders_val}, growth={orders_growth}")
            
            st.markdown(
                render_kpi_card(
                    config.KPI_TITLES["orders"],
                    format_number(orders_val),
                    orders_growth,
                    config.CARD_STYLES["blue"],
                ),
                unsafe_allow_html=True,
            )
        
        with k_cols[2]:
            aov_val = row.get("AOV", 0)
            aov_growth = row.get("AovGrowth", 0)
            logger.info(f"Rendering AOV card: value={aov_val}, growth={aov_growth}")
            
            st.markdown(
                render_kpi_card(
                    config.KPI_TITLES["aov"],
                    format_currency(aov_val),
                    aov_growth,
                    config.CARD_STYLES["red"],
                ),
                unsafe_allow_html=True,
            )
        
        with k_cols[3]:
            revenue_growth = row.get("RevenueGrowth", 0)
            logger.info(f"Rendering Growth card: value={revenue_growth}")
            
            st.markdown(
                render_kpi_card(
                    config.KPI_TITLES["growth"],
                    f"{revenue_growth:.1f}%",
                    revenue_growth,
                    config.CARD_STYLES["purple"],
                ),
                unsafe_allow_html=True,
            )
        
        logger.info("✓ KPI section rendered successfully")
    
    except Exception as e:
        logger.error(f"✗ Error rendering KPI section: {str(e)}", exc_info=True)
        st.error(f"Error rendering KPI metrics: {str(e)}")

"""
Chart UI components.
Handles Plotly chart rendering.
"""

from typing import Optional
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

import config
from src.logger import get_logger

logger = get_logger(__name__)


def render_hourly_trend_chart(trend_data: pd.DataFrame) -> None:
    """
    Render dual-axis line chart for hourly revenue and orders trend.
    
    Args:
        trend_data: DataFrame with HOURNUM, Revenue, Orders columns
    """
    if trend_data.empty:
        st.info("Chưa có dữ liệu biểu đồ cho khoảng thời gian này.")
        return
    
    try:
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Revenue line (left axis)
        fig.add_trace(
            go.Scatter(
                x=trend_data["HOURNUM"],
                y=trend_data["Revenue"],
                name="Doanh Số",
                line=dict(color=config.CHART_COLORS["revenue"]),
            ),
            secondary_y=False,
        )
        
        # Orders line (right axis)
        fig.add_trace(
            go.Scatter(
                x=trend_data["HOURNUM"],
                y=trend_data["Orders"],
                name="Đơn Hàng",
                line=dict(color=config.CHART_COLORS["orders"]),
            ),
            secondary_y=True,
        )
        
        # Update layout
        fig.update_layout(
            title_text="",
            hovermode="x unified",
            xaxis_title="Giờ (0-23)",
            height=config.CHART_HEIGHT,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        
        # Set y-axes titles
        fig.update_yaxes(title_text="Doanh Số", secondary_y=False)
        fig.update_yaxes(title_text="Đơn Hàng", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        logger.info("Hourly trend chart rendered successfully")
    
    except Exception as e:
        logger.error(f"Error rendering hourly trend chart: {e}")
        st.error(f"Trend Chart Error: {e}")


def render_stacked_bar_chart(data: pd.DataFrame, category_col: str, platform_col: str = None) -> None:
    """
    Render stacked bar chart for revenue by brand and platform.
    
    Args:
        data: DataFrame with category, platform, and Revenue columns
        category_col: Column name for categories (e.g., 'brand')
        platform_col: Column name for stacking (e.g., 'PlatformName')
    """
    if data.empty:
        st.info("Chưa có dữ liệu biểu đồ cho khoảng thời gian này.")
        return
    
    try:
        # Create figure
        fig = go.Figure()
        
        # Get unique platforms for colors
        platforms = data[platform_col].unique() if platform_col else []
        colors = ["#1e3a8a", "#ef4444", "#f97316", "#22c55e", "#8b5cf6"]
        
        # Add trace for each platform
        for i, platform in enumerate(platforms):
            platform_data = data[data[platform_col] == platform]
            color = colors[i % len(colors)]
            
            fig.add_trace(
                go.Bar(
                    x=platform_data[category_col],
                    y=platform_data["Revenue"],
                    name=platform,
                    marker=dict(color=color),
                )
            )
        
        # Update layout
        fig.update_layout(
            barmode="stack",
            title_text="",
            hovermode="x unified",
            xaxis_title=category_col.capitalize(),
            yaxis_title="Doanh Số",
            height=config.CHART_HEIGHT,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        logger.info(f"Stacked bar chart rendered for {category_col}")
    
    except Exception as e:
        logger.error(f"Error rendering stacked bar chart: {e}")
        st.error(f"Bar Chart Error: {e}")


def render_pie_chart(data: pd.DataFrame, label_col: str, value_col: str = "Revenue") -> None:
    """
    Render pie chart for revenue proportion.
    
    Args:
        data: DataFrame with label and value columns
        label_col: Column name for labels
        value_col: Column name for values (default: Revenue)
    """
    if data.empty:
        st.info("Chưa có dữ liệu biểu đồ cho khoảng thời gian này.")
        return
    
    try:
        # Create figure
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=data[label_col],
                    values=data[value_col],
                    hovertemplate="<b>%{label}</b><br>%{value:,.0f} (%{percent})<extra></extra>",
                )
            ]
        )
        
        # Update layout
        fig.update_layout(
            title_text="",
            height=config.CHART_HEIGHT,
            margin=dict(l=20, r=20, t=30, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        logger.info(f"Pie chart rendered for {label_col}")
    
    except Exception as e:
        logger.error(f"Error rendering pie chart: {e}")
        st.error(f"Pie Chart Error: {e}")


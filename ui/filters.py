"""
Filter UI components.
Handles filter popover dialogs for date, brand, platform, shop, status.
"""

from typing import List, Dict, Optional, Union
import streamlit as st
from datetime import datetime

import config
from src.logger import get_logger

logger = get_logger(__name__)


def checkbox_filter(
    label: str,
    options: Union[List[str], Dict[str, Optional[int]]],
    key_prefix: str,
) -> List[str]:
    """
    Render multi-select filter with checkbox popover.
    Includes 'Select All' / 'Deselect All' buttons.
    
    Args:
        label: Filter label displayed on button
        options: List of options or Dict with counts
        key_prefix: Unique key prefix for session state
        
    Returns:
        List of selected options
        
    Example:
        selected = checkbox_filter("Brand", ["Apple", "Samsung"], "br")
    """
    # Convert list to dict if needed
    if isinstance(options, list):
        options = {opt: None for opt in options}
    
    all_keys = list(options.keys())
    
    # Initialize session state
    if f"{key_prefix}_sel" not in st.session_state:
        st.session_state[f"{key_prefix}_sel"] = all_keys
    
    current_sel = st.session_state[f"{key_prefix}_sel"]
    
    # Compute button label based on selection
    if len(current_sel) == len(all_keys) and len(all_keys) > 0:
        btn_label = f"{label}: Tất cả"
    elif len(current_sel) == 0:
        btn_label = f"{label}: Chưa chọn"
    else:
        btn_label = f"{label}: Đã chọn {len(current_sel)} mục"
    
    # Popover content
    with st.popover(btn_label, use_container_width=True):
        st.markdown(f"**{label}**")
        
        # Select All / Deselect All buttons
        col1, col2 = st.columns(2)
        if col1.button(
            "Chọn tất cả",
            key=f"all_{key_prefix}",
            use_container_width=True,
        ):
            st.session_state[f"{key_prefix}_sel"] = all_keys
            st.rerun()
        
        if col2.button(
            "Bỏ hết",
            key=f"none_{key_prefix}",
            use_container_width=True,
        ):
            st.session_state[f"{key_prefix}_sel"] = []
            st.rerun()
        
        st.divider()
        
        # Checkbox list
        new_sel = []
        for name, count in options.items():
            col_text, col_count = st.columns([4, 1])
            
            # Checkbox
            is_checked = name in current_sel
            if col_text.checkbox(
                name,
                value=is_checked,
                key=f"cb_{key_prefix}_{name}",
            ):
                new_sel.append(name)
            
            # Display count (if available)
            if count is not None:
                col_count.markdown(
                    f"<p style='text-align:right; margin:0; color:gray;'>{count}</p>",
                    unsafe_allow_html=True,
                )
        
        # Update state and rerun if selection changed
        if set(new_sel) != set(current_sel):
            st.session_state[f"{key_prefix}_sel"] = new_sel
            st.rerun()
    
    return st.session_state[f"{key_prefix}_sel"]


def render_filter_section(
    engine,
    brand_options: List[str],
    platform_options: List[str],
    shop_options: Dict[str, int],
    status_options: List[str],
) -> Dict[str, List[str]]:
    """
    Render complete filter section with all filters.
    
    Args:
        engine: SQLAlchemy Engine (for data loading)
        brand_options: List of brands
        platform_options: List of platforms
        shop_options: Dict of shops with counts
        status_options: List of statuses
        
    Returns:
        Dictionary with selected values:
        {
            "date_range": (start_date, end_date),
            "date_str": (start_str, end_str),
            "brand": [...],
            "platform": [...],
            "shop": [...],
            "status": [...],
        }
    """
    filters = {}
    
    with st.container(border=True):
        f_c1, f_c2, f_c3, f_c4, f_c5 = st.columns([1.5, 1, 1, 1, 1])
        
        # Date picker
        with f_c1:
            date_range = st.date_input(
                "Thời gian",
                value=(datetime.now(), datetime.now()),
                format=config.DATE_FORMAT,
                label_visibility="collapsed",
            )
            
            if not (isinstance(date_range, tuple) and len(date_range) == 2):
                st.stop()
            
            start_date, end_date = date_range
            start_str = start_date.strftime(config.SQL_DATETIME_FORMAT.replace(" 00:00:00", " 00:00:00"))
            end_str = end_date.strftime(config.SQL_DATETIME_FORMAT.replace(" 23:59:59", " 23:59:59"))
            start_str = start_date.strftime("%Y-%m-%d 00:00:00")
            end_str = end_date.strftime("%Y-%m-%d 23:59:59")
            
            filters["date_range"] = (start_date, end_date)
            filters["date_str"] = (start_str, end_str)
        
        # Brand filter
        with f_c2:
            filters["brand"] = checkbox_filter(
                config.FILTERS["brand"]["label"],
                brand_options,
                config.FILTERS["brand"]["key"],
            )
        
        # Platform filter
        with f_c3:
            filters["platform"] = checkbox_filter(
                config.FILTERS["platform"]["label"],
                platform_options,
                config.FILTERS["platform"]["key"],
            )
        
        # Shop filter
        with f_c4:
            filters["shop"] = checkbox_filter(
                config.FILTERS["shop"]["label"],
                shop_options,
                config.FILTERS["shop"]["key"],
            )
        
        # Status filter
        with f_c5:
            filters["status"] = checkbox_filter(
                config.FILTERS["status"]["label"],
                status_options,
                config.FILTERS["status"]["key"],
            )
    
    logger.info(f"Filters applied: Brand={len(filters.get('brand', []))}, "
                f"Platform={len(filters.get('platform', []))}, "
                f"Shop={len(filters.get('shop', []))}, "
                f"Status={len(filters.get('status', []))}")
    
    return filters

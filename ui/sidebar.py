"""
Sidebar UI component.
Handles navigation menu and sidebar configuration.
"""

import streamlit as st
from typing import Dict, List, Optional
import config
from src.logger import get_logger

logger = get_logger(__name__)


def render_sidebar() -> Optional[str]:
    """
    Render sidebar with navigation menu.
    
    Returns:
        Selected menu item key or None
    """
    with st.sidebar:
        # Logo/Title
        st.markdown("### 📊 [B2C] Revenue & Orders")
        st.divider()
        
        # Navigation menu
        selected_menu = render_navigation_menu()
        
        st.divider()
        
        # Footer info
        st.markdown(
            "<small>v2.0 | Refactored Dashboard</small>",
            unsafe_allow_html=True
        )
        
        return selected_menu


def render_navigation_menu() -> Optional[str]:
    """
    Render navigation menu items using radio buttons.
    
    Returns:
        Selected menu key
    """
    menu_items = config.SIDEBAR_MENU
    menu_keys = [item["key"] for item in menu_items]
    menu_labels = [f"{item['icon']} {item['label']}" for item in menu_items]
    
    # Use radio for menu selection
    selected_index = st.radio(
        "Navigation",
        options=range(len(menu_keys)),
        format_func=lambda i: menu_labels[i],
        label_visibility="collapsed",
    )
    
    return menu_keys[selected_index]


def render_page_content(selected_menu: str) -> None:
    """
    Render content based on selected menu item.
    
    Args:
        selected_menu: Selected menu key
    """
    menu_map = config.SIDEBAR_MENU_MAP
    
    if selected_menu in menu_map:
        page_func = menu_map[selected_menu]
        page_func()
    else:
        st.error(f"Page not found: {selected_menu}")
        logger.warning(f"Unknown menu selection: {selected_menu}")

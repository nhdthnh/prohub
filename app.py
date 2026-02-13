"""
OQR Dashboard - Main Application
B2C Revenue & Orders Analytics Dashboard
"""

import streamlit as st

import config
from src.logger import get_logger
from ui.styles import inject_styles
from ui.sidebar import render_sidebar, render_page_content

logger = get_logger(__name__)


def initialize_app() -> None:
    """Initialize Streamlit page configuration."""
    st.set_page_config(**config.PAGE_CONFIG)
    inject_styles()
    
    # Initialize menu map on first run
    if not config.SIDEBAR_MENU_MAP:
        config.SIDEBAR_MENU_MAP.update(config._init_menu_map())
    
    logger.info("App initialized")


def main() -> None:
    """Main application flow."""
    initialize_app()
    
    # Render sidebar and get selected menu
    selected_menu = render_sidebar()
    
    # Render page content based on selection
    if selected_menu:
        render_page_content(selected_menu)


if __name__ == "__main__":
    main()

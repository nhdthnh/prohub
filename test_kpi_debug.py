"""Debug script to test render_kpi_section directly"""
import os
import sys

# Set up environment for Streamlit
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

import streamlit as st
import pandas as pd

# Import after setting environment
import config
from src.db.connection import get_engine
from src.services.data_service import get_kpi_data
from ui.styles import inject_styles
from ui.kpi_cards import render_kpi_section

# Inject styles
inject_styles()

st.title("🔍 Debug KPI Rendering")

# Get test data
engine = get_engine()
if engine:
    kpi_df = get_kpi_data(
        '2026-02-13 00:00:00', '2026-02-13 23:59:59',
        '2026-02-12 00:00:00', '2026-02-12 23:59:59',
        '', engine
    )
    
    st.write(f"KPI DataFrame shape: {kpi_df.shape}")
    st.write(f"KPI DataFrame columns: {kpi_df.columns.tolist()}")
    st.write(f"KPI DataFrame empty: {kpi_df.empty}")
    st.write("First row:")
    st.write(kpi_df.iloc[0] if not kpi_df.empty else "No data")
    
    st.write("\n---\n")
    st.write("### Attempting to render KPI section:")
    
    try:
        render_kpi_section(kpi_df)
        st.success("✓ KPI section rendered successfully!")
    except Exception as e:
        st.error(f"✗ Error rendering KPI section: {e}")
        import traceback
        st.code(traceback.format_exc())
else:
    st.error("Could not connect to database")

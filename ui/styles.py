"""
Custom CSS styles for dashboard.
"""

DASHBOARD_CSS = """
<style>
    /* Card Metric */
    .metric-card {
        border-radius: 12px; 
        padding: 20px; 
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex; 
        flex-direction: column; 
        height: 130px;
    }
    
    .card-white { 
        background: white; 
        color: #333; 
        border: 1px solid #eee; 
    }
    
    .card-blue { 
        background: linear-gradient(135deg, #1e3a8a, #3b82f6); 
    }
    
    .card-red { 
        background: linear-gradient(135deg, #991b1b, #ef4444); 
    }
    
    .card-purple { 
        background: linear-gradient(135deg, #581c87, #a855f7); 
    }
    
    /* Popover Button Styling */
    div[data-testid="stPopover"] > button {
        width: 100% !important;
        border-radius: 4px !important;
        text-align: left !important;
        background-color: white !important;
        border: 1px solid #d1d5db !important;
        color: #333 !important;
        height: 42px;
    }
    
    /* Filter Item Styling */
    .filter-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    
    .count-label {
        color: #6b7280;
        font-size: 0.85em;
    }
</style>
"""


def inject_styles():
    """
    Inject custom CSS into Streamlit app.
    """
    import streamlit as st
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

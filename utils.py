import os
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_data(query, _engine, params=None):
    """
    Executes a SQL query and returns a pandas DataFrame.
    Cached to improve performance. 
    Prefix _engine with underscore to prevent Streamlit from hashing it (it's not hashable).
    """
    try:
        return pd.read_sql(query, _engine, params=params)
    except Exception as e:
        # print(f"Error fetching data: {e}") 
        return pd.DataFrame() # Return empty DF on error to avoid crashing


def load_query(query_name):
    """
    Loads a SQL query from the 'query' directory.
    """
    file_path = os.path.join("query", query_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Query file not found: {query_name}")
        return ""

def format_currency(value):
    """
    Formats a number as currency (VND style).
    """
    if value is None:
        return "0"
    return "{:,.0f}".format(value)

def format_number(value):
    """
    Formats a number with commas.
    """
    if value is None:
        return "0"
    return "{:,.0f}".format(value)

def escape_sql_string(value):
    """
    Escapes single quotes in a string to prevent SQL errors.
    """
    if isinstance(value, str):
        return value.replace("'", "''")
    return value

def build_filters(brand, platform, shop, status):
    """
    Constructs the SQL WHERE clause based on selected filters for Sales (omisell_catalogue).
    """
    filters = []
    
    # Process Brand
    actual_brands = [b for b in brand if b != "Tất cả"]
    if actual_brands:
        brands_str = "', '".join([escape_sql_string(b) for b in actual_brands])
        filters.append(f"brand IN ('{brands_str}')")
        
    # Process Platform
    actual_platforms = [p for p in platform if p != "Tất cả"]
    if actual_platforms:
        platforms_str = "', '".join([escape_sql_string(p) for p in actual_platforms])
        filters.append(f"PlatformName IN ('{platforms_str}')")
        
    # Process Shop
    actual_shops = [s for s in shop if s != "Tất cả"]
    if actual_shops:
        shops_str = "', '".join([escape_sql_string(s) for s in actual_shops])
        filters.append(f"ShopName IN ('{shops_str}')")
        
    # Process Status
    actual_statuses = [st for st in status if st != "Tất cả"]
    if actual_statuses:
        statuses_str = "', '".join([escape_sql_string(st) for st in actual_statuses])
        filters.append(f"StatusName IN ('{statuses_str}')")
        
    if filters:
        return "AND " + " AND ".join(filters)
    return ""

def build_inventory_filters(brand, shop):
    """
    Constructs the SQL WHERE clause for Inventory (omisell_inventory).
    Inventory table likely only has Brand and Shop, not Order Status or Platform.
    """
    filters = []
    
    # Process Brand
    actual_brands = [b for b in brand if b != "Tất cả"]
    if actual_brands:
        brands_str = "', '".join([escape_sql_string(b) for b in actual_brands])
        filters.append(f"brand IN ('{brands_str}')")
        
    # Process Shop
    actual_shops = [s for s in shop if s != "Tất cả"]
    if actual_shops:
        shops_str = "', '".join([escape_sql_string(s) for s in actual_shops])
        filters.append(f"ShopName IN ('{shops_str}')")
        
    if filters:
        return "AND " + " AND ".join(filters)
    return ""

def get_previous_period(start_date, end_date):
    """
    Calculates the previous period based on the selected duration.
    """
    delta = end_date - start_date
    prev_end = start_date - timedelta(days=1)
    prev_start = prev_end - delta
    return prev_start, prev_end

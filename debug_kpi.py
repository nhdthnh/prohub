import pandas as pd
import config
from ui.kpi_cards import render_kpi_section
from src.utils.formatters import format_currency, format_number

# Simulate the KPI data returned from database
kpi_data = pd.DataFrame({
    'Revenue': [1.470842e+08],
    'Orders': [415],
    'Quantity': [0],
    'AOV': [354179.5],
    'RevenueGrowth': [-50.0],
    'OrdersGrowth': [-49.8186],
    'QuantityGrowth': [0],
    'AovGrowth': [-0.646398]
})

print("DataFrame:")
print(kpi_data)
print("\nColumns:", kpi_data.columns.tolist())
print("\nFirst row:")
row = kpi_data.iloc[0]
print(row)

# Try to access what render_kpi_section does
print("\nTesting render_kpi_section logic:")
print(f"Revenue: {row.get('Revenue', 0)}")
print(f"Orders: {row.get('Orders', 0)}")
print(f"AOV: {row.get('AOV', 0)}")
print(f"RevenueGrowth: {row.get('RevenueGrowth', 0)}")
print(f"OrdersGrowth: {row.get('OrdersGrowth', 0)}")
print(f"AovGrowth: {row.get('AovGrowth', 0)}")

print("\nFormatting test:")
print(f"Formatted Revenue: {format_currency(row.get('Revenue', 0))}")
print(f"Formatted Orders: {format_number(row.get('Orders', 0))}")
print(f"Formatted AOV: {format_currency(row.get('AOV', 0))}")

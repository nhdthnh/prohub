# routes/b2c.py
from flask import Blueprint, render_template, request
from datetime import datetime
from dependencies import qm  # Import qm từ file chung

# Tạo Blueprint tên là 'b2c'
b2c_bp = Blueprint('b2c', __name__)

def _process_chart_data(raw_trend):
    """Hàm phụ trợ: Xử lý dữ liệu biểu đồ để code chính gọn hơn"""
    hours = list(range(24))
    data_revenue = [0] * 24 
    data_orders = [0] * 24

    for row in raw_trend:
        raw_hour = row['HOURNUM']
        idx = raw_hour.hour if hasattr(raw_hour, 'hour') else int(raw_hour)
        if 0 <= idx < 24:
            data_revenue[idx] = float(row['Revenue'] or 0)
            data_orders[idx] = int(row['Orders'] or 0)
            
    labels_hours = [f"{h}:00" for h in hours]
    return labels_hours, data_revenue, data_orders

@b2c_bp.route('/')  # Đường dẫn gốc cho trang này
def dashboard():
    # 1. Xử lý ngày tháng
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if not start_date or not end_date:
        today_str = datetime.now().strftime('%Y-%m-%d')
        start_date = end_date = today_str

    # 2. Lấy Filters từ URL
    selected_filters = {
        'shops': request.args.getlist('shops'),
        'platforms': request.args.getlist('platforms'),
        'statuses': request.args.getlist('statuses'),
        'brands': request.args.getlist('brands')
    }

    # 3. Gọi các hàm lấy dữ liệu từ QueryManager (qm)
    kpi_data = qm.get_kpi_growth(start_date, end_date, filter_dict=selected_filters)
    filters = qm.get_filters(start_date, end_date)
    raw_trend = qm.get_hourly_trend(start_date, end_date, filter_dict=selected_filters)
    raw_status = qm.get_order_status(start_date, end_date, filter_dict=selected_filters)
    raw_province = qm.get_province_data(start_date, end_date, filter_dict=selected_filters)
    raw_brand_platform = qm.get_revenue_by_brand_platform(start_date, end_date, filter_dict=selected_filters)

    # 4. Xử lý dữ liệu biểu đồ (Gọi hàm phụ trợ đã tách ở trên)
    chart_labels, chart_revenue, chart_orders = _process_chart_data(raw_trend)

    # 5. Xử lý biểu đồ tròn
    pie_labels = [row['StatusName'] or 'Unknown' for row in raw_status]
    pie_data = [row['Orders'] for row in raw_status]

    return render_template('index.html', 
                           header_title="[B2C] Revenue & Orders Dashboard",
                           filters=filters,
                           kpi=kpi_data,
                           chart_labels=chart_labels,
                           chart_revenue=chart_revenue,
                           chart_orders=chart_orders,
                           pie_labels=pie_labels, 
                           pie_data=pie_data,
                           raw_status=raw_status,
                           raw_province=raw_province,
                           raw_brand_platform = raw_brand_platform)
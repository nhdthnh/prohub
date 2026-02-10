from flask import Blueprint, render_template, request
from datetime import datetime
from dependencies import qm  # Import QueryManager
from services.b2c_service import b2c_service

# Tùy vào setup của bạn, dòng này có thể là app.route hoặc bp.route
# Theo ngữ cảnh, mình dùng Blueprint:
b2c_bp = Blueprint('b2c', __name__)

@b2c_bp.route('/') 
def dashboard():
    # 1. Xử lý ngày tháng
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if not start_date or not end_date:
        today_str = datetime.now().strftime('%Y-%m-%d')
        start_date = end_date = today_str

    # 2. Lấy Filters
    selected_filters = {
        'shops': request.args.getlist('shops'),
        'platforms': request.args.getlist('platforms'),
        'statuses': request.args.getlist('statuses'),
        'brands': request.args.getlist('brands')
    }

    # 3. GỌI DATABASE (Lấy dữ liệu thô)
    filters_options = qm.get_filters(start_date, end_date)
    kpi_data = qm.get_kpi_growth(start_date, end_date, filter_dict=selected_filters)
    
    # Dữ liệu biểu đồ
    raw_trend = qm.get_hourly_trend(start_date, end_date, filter_dict=selected_filters)
    raw_status = qm.get_order_status(start_date, end_date, filter_dict=selected_filters)
    raw_province = qm.get_province_data(start_date, end_date, filter_dict=selected_filters)
    
    # [QUAN TRỌNG] Lấy dữ liệu cho Stacked Bar Chart (bị thiếu trước đó)
    raw_brand_platform = qm.get_revenue_by_brand_platform(start_date, end_date, filter_dict=selected_filters)
    
    # Dữ liệu cho Brand Performance Table
    raw_brand_perf = qm.get_brand_performance(start_date, end_date, filter_dict=selected_filters)

    # 4. GỌI SERVICE (Xử lý logic)
    brand_tbl, brand_tot, brand_max, brand_pie = b2c_service.process_brand_performance(raw_brand_perf)
    chart_lbl, chart_rev, chart_ord = b2c_service.process_chart_data(raw_trend)

    # 5. RENDER TEMPLATE (Truyền đầy đủ biến)
    return render_template(
        'index.html', 
        header_title="[B2C] Revenue & Orders Dashboard",
        
        # Context cơ bản
        filters=filters_options,
        start_date=start_date,
        end_date=end_date,
        
        # Data biểu đồ
        kpi=kpi_data,
        chart_labels=chart_lbl,
        chart_revenue=chart_rev,
        chart_orders=chart_ord,
        
        # Raw Data cho JS
        raw_status=raw_status,
        raw_province=raw_province,
        
        # [SỬA LỖI] Truyền biến này để tránh lỗi 'Undefined'
        raw_brand_platform=raw_brand_platform, 

        # Data cho Component Brand
        brand_table=brand_tbl,
        brand_total=brand_tot,
        max_vals=brand_max,
        brand_pie_data=brand_pie
    )
# app.py
from flask import Flask, render_template, request
from database.db import Database
from database.queries import QueryManager
from datetime import datetime

app = Flask(__name__)

# Khởi tạo DB và QueryManager
db = Database()
qm = QueryManager(db)

@app.route('/')
def dashboard():
    # 1. Lấy tham số ngày từ URL
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    # Nếu chưa có, mặc định lấy hôm nay
    if not start_date or not end_date:
        today_str = datetime.now().strftime('%Y-%m-%d')
        start_date = today_str
        end_date = today_str

    # 2. Lấy dữ liệu KPI Tổng hợp (Bao gồm Revenue, Orders, Qty, AOV và % Growth)
    # Chỉ gọi 1 hàm này thay vì 4 hàm lẻ để tối ưu tốc độ
    kpi_data = qm.get_kpi_growth(start_date, end_date)

    # 3. Lấy dữ liệu Filter và các Biểu đồ khác
    filters = qm.get_filters()
    raw_trend = qm.get_hourly_trend(start_date, end_date)
    raw_status = qm.get_order_status(start_date, end_date)
    raw_province = qm.get_province_data(start_date, end_date)

    # 4. Xử lý dữ liệu biểu đồ Line (Hourly Trend)
    hours = list(range(24))
    data_revenue = [0] * 24 
    data_orders = [0] * 24

    for row in raw_trend:
        raw_hour = row['HOURNUM']
        # Xử lý an toàn: Nếu SQL trả về datetime thì lấy .hour, nếu int thì giữ nguyên
        idx = raw_hour.hour if hasattr(raw_hour, 'hour') else int(raw_hour)
        
        if 0 <= idx < 24:
            data_revenue[idx] = float(row['Revenue'] or 0)
            data_orders[idx] = int(row['Orders'] or 0)
    
    labels_hours = [f"{h}:00" for h in hours]

    # 5. Xử lý dữ liệu biểu đồ Pie (Order Status)
    pie_labels = [row['StatusName'] or 'Unknown' for row in raw_status]
    pie_data = [row['Orders'] for row in raw_status]

    # 6. Render ra HTML
    return render_template('index.html', 
                           header_title="[B2C] Revenue & Orders Dashboard",
                           
                           # Dữ liệu bộ lọc
                           filters=filters, 
                           
                           # Dữ liệu KPI (Truyền nguyên cục dictionary kpi_data)
                           kpi=kpi_data, 
                           
                           # Dữ liệu biểu đồ Line
                           chart_labels=labels_hours,
                           chart_revenue=data_revenue,
                           chart_orders=data_orders,
                           
                           # Dữ liệu biểu đồ Pie + Table Status
                           pie_labels=pie_labels,
                           pie_data=pie_data,
                           raw_status=raw_status,
                           
                           # Dữ liệu Map
                           raw_province=raw_province)

if __name__ == '__main__':
    app.run(debug=True)
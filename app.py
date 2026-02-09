# app.py
from flask import Flask, render_template, request
from database.db import Database
from database.queries import QueryManager # Import class quản lý query mới
from datetime import datetime, timedelta

app = Flask(__name__)

# Khởi tạo DB và QueryManager
db = Database()
qm = QueryManager(db) # Truyền db vào để QueryManager sử dụng

@app.route('/')
def dashboard():
    # Gọi đúng 1 dòng để lấy toàn bộ filter
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    # Nếu chưa có (lần đầu vào), mặc định lấy hôm nay
    if not start_date or not end_date:
        today_str = datetime.now().strftime('%Y-%m-%d')
        start_date = today_str
        end_date = today_str
    revenue = qm.get_revenue(start_date, end_date)
    orders = qm.get_orders(start_date, end_date)
    quantity = qm.get_quantity(start_date, end_date)
    AOV = qm.get_AOV(start_date, end_date)
    filters = qm.get_filters()

    raw_trend = qm.get_hourly_trend(start_date, end_date)

    # 2. Chuẩn bị 3 mảng dữ liệu (Arrays)
    hours = list(range(24)) # [0, 1, 2, ..., 23]
    
    # Tạo mảng chứa toàn số 0
    data_revenue = [0] * 24 
    data_orders = [0] * 24

    # 3. Đổ dữ liệu từ SQL vào đúng vị trí giờ
    for row in raw_trend:
        idx = row['HOURNUM'] # Lấy giờ làm index (0-23)
        if 0 <= idx < 24:
            data_revenue[idx] = float(row['Revenue'] or 0)
            data_orders[idx] = int(row['Orders'] or 0)
    
    # 4. Tạo Label cho trục X (0:00, 1:00...)
    labels_hours = [f"{h}:00" for h in hours]
    raw_status = qm.get_order_status(start_date, end_date)

    # 2. Tách dữ liệu cho Pie Chart
    # Nếu StatusName bị None thì đặt là 'Unknown'
    pie_labels = [row['StatusName'] or 'Unknown' for row in raw_status]
    pie_data = [row['Orders'] for row in raw_status]
    raw_province = qm.get_province_data(start_date, end_date)
    return render_template('index.html', 
                           filters=filters, 
                           revenue=revenue, # Truyền biến revenue sang HTML
                           orders = orders,
                           quantity=quantity,
                           AOV= AOV,
                           chart_labels=labels_hours,
                           chart_revenue=data_revenue,
                           chart_orders=data_orders,
                           pie_labels=pie_labels,
                           pie_data=pie_data,
                           raw_status=raw_status,
                           raw_province=raw_province,
                           header_title="[B2C] Revenue & Orders Dashboard")

if __name__ == '__main__':
    app.run(debug=True)
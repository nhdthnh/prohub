class B2CService:
    def process_brand_performance(self, raw_data):
        """Xử lý dữ liệu Brand Performance"""
        if not raw_data:
            # Trả về data rỗng chuẩn định dạng để không gây lỗi JS
            return [], {'revenue': 0, 'orders': 0, 'rev_growth': 0, 'ord_growth': 0}, {'rev': 1, 'ord': 1}, []

        processed_brands = []
        total_rev = 0; total_ord = 0
        total_prev_rev = 0; total_prev_ord = 0
        max_rev = 0; max_ord = 0

        for item in raw_data:
            # Dùng .get() và ép kiểu an toàn
            rev = float(item.get('Revenue') or 0)
            ord_val = int(item.get('Orders') or 0)
            prev_rev = float(item.get('PreviousRevenue') or 0)
            prev_ord = int(item.get('PreviousOrders') or 0)

            total_rev += rev
            total_ord += ord_val
            total_prev_rev += prev_rev
            total_prev_ord += prev_ord
            
            if rev > max_rev: max_rev = rev
            if ord_val > max_ord: max_ord = ord_val

            # Tính Growth
            rev_growth = ((rev - prev_rev) / prev_rev * 100) if prev_rev > 0 else (100 if rev > 0 else 0)
            ord_growth = ((ord_val - prev_ord) / prev_ord * 100) if prev_ord > 0 else (100 if ord_val > 0 else 0)

            processed_brands.append({
                'brand': item.get('brand') or 'Unknown',
                'revenue': rev, 'orders': ord_val,
                'rev_growth': rev_growth, 'ord_growth': ord_growth
            })

        # Tổng cộng
        total_rev_growth = ((total_rev - total_prev_rev) / total_prev_rev * 100) if total_prev_rev > 0 else 0
        total_ord_growth = ((total_ord - total_prev_ord) / total_prev_ord * 100) if total_prev_ord > 0 else 0

        grand_total = {
            'revenue': total_rev, 'orders': total_ord,
            'rev_growth': total_rev_growth, 'ord_growth': total_ord_growth
        }

        # Max values (để vẽ thanh bar)
        max_vals = {'rev': max_rev if max_rev > 0 else 1, 'ord': max_ord if max_ord > 0 else 1}
        
        # Pie Data
        pie_data = [{'name': b['brand'], 'y': b['revenue']} for b in processed_brands]

        return processed_brands, grand_total, max_vals, pie_data

    def process_chart_data(self, raw_trend):
        """Xử lý biểu đồ Line (Hourly) an toàn tuyệt đối"""
        # 1. Tạo khung 24 giờ
        hours = list(range(24))
        data_revenue = [0.0] * 24 
        data_orders = [0] * 24
        labels_hours = [f"{h}:00" for h in hours]

        if not raw_trend:
            return labels_hours, data_revenue, data_orders

        # 2. Map dữ liệu (Hỗ trợ nhiều tên cột khác nhau)
        for row in raw_trend:
            # Thử lấy các key phổ biến: HOURNUM, Hour, hour, HourNum
            raw_hour = row.get('HOURNUM') or row.get('Hour') or row.get('hour') or row.get('HourNum')
            
            idx = -1
            # Xử lý nếu raw_hour là datetime, int, hoặc string
            if hasattr(raw_hour, 'hour'):
                idx = raw_hour.hour
            elif raw_hour is not None:
                try: idx = int(raw_hour)
                except: pass
            
            # Chỉ điền dữ liệu nếu giờ hợp lệ (0-23)
            if 0 <= idx < 24:
                data_revenue[idx] = float(row.get('Revenue') or 0)
                data_orders[idx] = int(row.get('Orders') or 0)
        
        return labels_hours, data_revenue, data_orders

# Khởi tạo instance
b2c_service = B2CService()
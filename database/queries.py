# database/queries.py
import os
from datetime import datetime, timedelta
class QueryManager:
    def __init__(self, db):
        self.db = db
        # Lấy đường dẫn tuyệt đối của folder chứa file này (database/)
        self.db = db
        # 1. Lấy đường dẫn đến file hiện tại (database/queries.py)
        current_file_path = os.path.abspath(__file__)
        
        # 2. Lấy thư mục cha của file này (folder database)
        database_dir = os.path.dirname(current_file_path)
        
        # 3. Nhảy ra ngoài 1 cấp và vào folder 'query'
        # Dùng normpath để nó tự tính toán dấu '..' thành đường dẫn sạch đẹp
        self.query_folder = os.path.normpath(os.path.join(database_dir, '..', 'query'))
        
        # Debug: In ra để kiểm tra
        # print(f"📂 Folder Query chuẩn: {self.query_folder}")

    def _load_sql(self, filename):
        path = os.path.join(self.query_folder, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        print(f"❌ LỖI: Không tìm thấy file {path}") # Debug
        return ""

    def get_filters(self):
        filters = {}
        
        # Danh sách các file cần load
        tasks = {
            'brands': 'get_Brand.sql',
            'platforms': 'get_Platform.sql',
            'shops': 'get_Shop_Name.sql',
            'statuses': 'get_Status_Name.sql'
        }

        for key, filename in tasks.items():
            sql = self._load_sql(filename)
            if sql:
                data = self.db.execute_query(sql)
                filters[key] = data
            else:
                filters[key] = []

        return filters
    
    def get_revenue(self, start_date, end_date):
        """Tính doanh thu theo khoảng thời gian"""
        
        # 1. Xử lý thời gian để lấy trọn vẹn ngày
        # Ví dụ: start='2026-02-08' -> '2026-02-08 00:00:00'
        #        end='2026-02-08'   -> '2026-02-08 23:59:59'
        start_full = f"{start_date} 00:00:00"
        end_full = f"{end_date} 23:59:59"

        sql = self._load_sql('get_Revenue_Order_AOV.sql')
        if sql:
            # Truyền start_full và end_full vào query
            result = self.db.execute_query(sql, (start_full, end_full))
            
            if result and result[0]['Revenue']:
                return result[0]['Revenue']
        return 0
    

    def get_orders(self, start_date, end_date):
        """Tính doanh thu theo khoảng thời gian"""
        
        # 1. Xử lý thời gian để lấy trọn vẹn ngày
        # Ví dụ: start='2026-02-08' -> '2026-02-08 00:00:00'
        #        end='2026-02-08'   -> '2026-02-08 23:59:59'
        start_full = f"{start_date} 00:00:00"
        end_full = f"{end_date} 23:59:59"

        sql = self._load_sql('get_Revenue_Order_AOV.sql')
        if sql:
            # Truyền start_full và end_full vào query
            result = self.db.execute_query(sql, (start_full, end_full))
            
            if result and result[0]['Orders']:
                return result[0]['Orders']
        return 0
    

    def get_orders(self, start_date, end_date):
        """Tính doanh thu theo khoảng thời gian"""
        
        # 1. Xử lý thời gian để lấy trọn vẹn ngày
        # Ví dụ: start='2026-02-08' -> '2026-02-08 00:00:00'
        #        end='2026-02-08'   -> '2026-02-08 23:59:59'
        start_full = f"{start_date} 00:00:00"
        end_full = f"{end_date} 23:59:59"

        sql = self._load_sql('get_Revenue_Order_AOV.sql')
        if sql:
            # Truyền start_full và end_full vào query
            result = self.db.execute_query(sql, (start_full, end_full))
            
            if result and result[0]['Orders']:
                return result[0]['Orders']
        return 0
    
    def get_quantity(self, start_date, end_date):
        """Tính doanh thu theo khoảng thời gian"""
        
        # 1. Xử lý thời gian để lấy trọn vẹn ngày
        # Ví dụ: start='2026-02-08' -> '2026-02-08 00:00:00'
        #        end='2026-02-08'   -> '2026-02-08 23:59:59'
        start_full = f"{start_date} 00:00:00"
        end_full = f"{end_date} 23:59:59"

        sql = self._load_sql('get_Quantity.sql')
        if sql:
            # Truyền start_full và end_full vào query
            result = self.db.execute_query(sql, (start_full, end_full))
            
            if result and result[0]['Quantity']:
                return result[0]['Quantity']
        return 0
    

    def get_AOV(self, start_date, end_date):
        """Tính doanh thu theo khoảng thời gian"""
        
        # 1. Xử lý thời gian để lấy trọn vẹn ngày
        # Ví dụ: start='2026-02-08' -> '2026-02-08 00:00:00'
        #        end='2026-02-08'   -> '2026-02-08 23:59:59'
        start_full = f"{start_date} 00:00:00"
        end_full = f"{end_date} 23:59:59"

        sql = self._load_sql('get_Revenue_Order_AOV.sql')
        if sql:
            # Truyền start_full và end_full vào query
            result = self.db.execute_query(sql, (start_full, end_full))
            
            if result and result[0]['AOV']:
                return result[0]['AOV']
        return 0
    
    def get_hourly_trend(self, start_date, end_date):
        # 1. Xử lý full ngày giờ (như bước trước)
        start_full = f"{start_date} 00:00:00"
        end_full = f"{end_date} 23:59:59"
        
        sql = self._load_sql('get_Hourly_Trend.sql')
        if sql:
            return self.db.execute_query(sql, (start_full, end_full))
        return []
    
    def get_order_status(self, start_date, end_date):
        # Xử lý full ngày giờ
        start_full = f"{start_date} 00:00:00"
        end_full = f"{end_date} 23:59:59"
        
        sql = self._load_sql('get_OrderStatus.sql')
        if sql:
            return self.db.execute_query(sql, (start_full, end_full))
        return []
    
    def get_province_data(self, start_date, end_date):
        start_full = f"{start_date} 00:00:00"
        end_full = f"{end_date} 23:59:59"
        
        sql = self._load_sql('get_Province.sql')
        if sql:
            return self.db.execute_query(sql, (start_full, end_full))
        return []
    
    def get_kpi_growth(self, start_date_str, end_date_str):
        # 1. Tính toán ngày tháng
        fmt = '%Y-%m-%d'
        try:
            curr_start = datetime.strptime(start_date_str, fmt)
            curr_end = datetime.strptime(end_date_str, fmt)
        except ValueError:
            return None # Trả về None nếu lỗi ngày

        # Độ dài chu kỳ (delta)
        delta = curr_end - curr_start
        
        # Ngày của kỳ trước (Previous Period)
        prev_end = curr_start - timedelta(days=1)
        prev_start = prev_end - delta

        # Chuyển thành string full time
        p_curr_start = f"{curr_start.strftime(fmt)} 00:00:00"
        p_curr_end = f"{curr_end.strftime(fmt)} 23:59:59"
        
        p_prev_start = f"{prev_start.strftime(fmt)} 00:00:00"
        p_prev_end = f"{prev_end.strftime(fmt)} 23:59:59"
        
        # Range bao trùm cả 2 kỳ (để tối ưu WHERE)
        p_total_start = p_prev_start
        p_total_end = p_curr_end

        # Load file SQL mới (Xem Bước 2 bên dưới)
        sql = self._load_sql('get_KPI_Growth.sql')
        
        if sql:
            # Thứ tự tham số truyền vào SQL
            params = (
                p_curr_start, p_curr_end,  # Current
                p_curr_start, p_curr_end,
                p_curr_start, p_curr_end,
                
                p_prev_start, p_prev_end,  # Previous
                p_prev_start, p_prev_end,
                p_prev_start, p_prev_end,
                
                p_total_start, p_total_end # WHERE
            )
            
            result = self.db.execute_query(sql, params)
            if result:
                return result[0] # Trả về dict chứa tất cả số liệu
        
        # Mặc định trả về 0 hết nếu lỗi
        return {
            'Revenue': 0, 'RevenueGrowth': 0,
            'Orders': 0, 'OrdersGrowth': 0,
            'Quantity': 0, 'QuantityGrowth': 0,
            'AOV': 0, 'AovGrowth': 0
        }
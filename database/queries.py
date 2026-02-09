# database/queries.py
import os

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
        print(f"📂 Folder Query chuẩn: {self.query_folder}")

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
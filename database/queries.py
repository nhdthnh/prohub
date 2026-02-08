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
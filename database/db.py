# database/db.py
import os
import mysql.connector
from dotenv import load_dotenv

class Database:
    def __init__(self):
        # Nạp biến môi trường từ file .env vào hệ thống
        load_dotenv()

        # Lấy giá trị từ env, tham số thứ 2 là giá trị mặc định nếu không tìm thấy
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', ''),
            'port': int(os.getenv('DB_PORT', 3306)) # Chuyển port về số nguyên
        }

    def get_connection(self):
        try:
            # **self.config sẽ bung dictionary thành các tham số keyword
            return mysql.connector.connect(**self.config)
        except Exception as e:
            print(f"Error connecting to DB: {e}")
            return None

    def execute_query(self, sql_query, params=None): # <--- Thêm params=None
        """Hàm nhận chuỗi SQL và tham số (nếu có)"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            if params:
                cursor.execute(sql_query, params) # <--- Truyền params vào đây
            else:
                cursor.execute(sql_query)
                
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"SQL Error: {e}")
            return []
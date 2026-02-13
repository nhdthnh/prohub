import pymysql
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import streamlit as st

# Cấu hình kết nối cơ sở dữ liệu
DB_HOST = "192.168.1.119"  # Thay đổi với host của bạn
DB_USER = "root"  # Thay đổi với user của bạn
DB_PASSWORD = "Oqr@18009413"  # Thay đổi với password của bạn
DB_NAME = "omisell_db"  # Thay đổi với tên database của bạn
DB_PORT = 3306  # Cổng MySQL mặc định

@st.cache_resource
def get_database_connection():
    """
    Tạo và trả về kết nối cơ sở dữ liệu MySQL
    """
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        st.error(f"Lỗi kết nối cơ sở dữ liệu: {e}")
        return None

@st.cache_resource
def get_sqlalchemy_engine():
    """
    Tạo và trả về SQLAlchemy engine cho pandas
    """
    try:
        # URL encode password để xử lý các ký tự đặc biệt như @
        encoded_password = quote_plus(DB_PASSWORD)
        engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
        )
        return engine
    except Exception as e:
        st.error(f"Lỗi tạo SQLAlchemy engine: {e}")
        return None

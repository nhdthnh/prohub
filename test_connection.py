import pymysql
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

# Cấu hình
DB_HOST = "192.168.1.119"
DB_USER = "root"
DB_PASSWORD = "Oqr@18009413"
DB_NAME = "omisell_db"
DB_PORT = 3306

print("=" * 50)
print("Test Kết Nối MySQL")
print("=" * 50)

# Test 1: Kết nối trực tiếp với pymysql
print("\n1. Test với pymysql...")
try:
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )
    print("✓ Kết nối pymysql thành công!")
    
    # Thử query đơn giản
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print(f"✓ Query test thành công: {result}")
    conn.close()
except Exception as e:
    print(f"✗ Lỗi pymysql: {e}")

# Test 2: Kết nối với SQLAlchemy
print("\n2. Test với SQLAlchemy...")
try:
    encoded_password = quote_plus(DB_PASSWORD)
    connection_string = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    print(f"Connection String: {connection_string}")
    
    engine = create_engine(connection_string)
    
    # Thử execute query
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✓ Kết nối SQLAlchemy thành công!")
        print(f"✓ Query test thành công")
        
    # Thử đọc dữ liệu từ table
    import pandas as pd
    query = "SELECT DISTINCT brand FROM omisell_catalogue LIMIT 5"
    df = pd.read_sql(query, con=engine)
    print(f"✓ Đọc dữ liệu thành công! ({len(df)} hàng)")
    print(df.head())
    
except Exception as e:
    print(f"✗ Lỗi SQLAlchemy: {type(e).__name__}: {e}")

print("\n" + "=" * 50)

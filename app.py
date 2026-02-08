# app.py
from flask import Flask, render_template
from database.db import Database
from database.queries import QueryManager # Import class quản lý query mới

app = Flask(__name__)

# Khởi tạo DB và QueryManager
db = Database()
qm = QueryManager(db) # Truyền db vào để QueryManager sử dụng

@app.route('/')
def dashboard():
    # Gọi đúng 1 dòng để lấy toàn bộ filter
    filter_data = qm.get_filters()

    # Ví dụ lấy data chính sau này:
    # main_data = qm.get_main_data()

    return render_template('index.html', filters=filter_data)

if __name__ == '__main__':
    app.run(debug=True)
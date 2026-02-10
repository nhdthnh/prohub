# app.py
from flask import Flask
# Import Blueprint từ file routes
from routes.b2c_overview import b2c_bp 

app = Flask(__name__)

# Đăng ký Blueprint
# url_prefix='/b2c' nghĩa là truy cập web.com/b2c sẽ vào trang này
# Nếu muốn làm trang chủ thì để url_prefix='/'
app.register_blueprint(b2c_bp, url_prefix='/') 

# Sau này nếu có trang B2B:
# from routes.b2b import b2b_bp
# app.register_blueprint(b2b_bp, url_prefix='/b2b')

if __name__ == '__main__':
    app.run(debug=True)
# app.py
from flask import Flask
# Import Blueprint từ file routes
from routes.b2c_overview import b2c_bp 

app = Flask(__name__)

# Đăng ký Blueprint
# url_prefix='/b2c' nghĩa là truy cập web.com/b2c sẽ vào trang này
# Nếu muốn làm trang chủ thì để url_prefix='/'
app.register_blueprint(b2c_bp, url_prefix='/') 

# --- CONFIG SIDEBAR ---
@app.context_processor
def inject_sidebar():
    sidebar_items = [
        {
            "type": "group",
            "title": "[B2C] Revenue & Orders",
            "icon": "fa-users",
            "submenu": [
                {"title": "Overview", "endpoint": "b2c.dashboard"},
                {"title": "Custom Report", "endpoint": "#"},
                {"title": "Shopee Fee", "endpoint": "#"},
                {"title": "TikTok Shop Fee", "endpoint": "#"}
            ]
        },
        {
            "type": "group",
            "title": "[B2B] Revenue & Orders",
            "icon": "fa-store",
            "submenu": [
                {"title": "Overview", "endpoint": "#"},
                {"title": "Custom Theo KH", "endpoint": "#"},
                {"title": "(Đối chiếu) KH MT/GT", "endpoint": "#"}
            ]
        },
        {
            "type": "single",
            "title": "Kế toán check",
            "icon": "fa-solid fa-calculator",
            "endpoint": "#"
        },
        {
            "type": "group",
            "title": "Fulfillment",
            "icon": "fa-building",
            "submenu": [
                {"title": "Overview", "endpoint": "#"},
                {"title": "Chi phí vận hành", "endpoint": "#"},
                {"title": "Kiểm tra tồn kho", "endpoint": "#"}
            ]
        }
    ]
    return dict(sidebar_items=sidebar_items)


if __name__ == '__main__':
    app.run(debug=True)
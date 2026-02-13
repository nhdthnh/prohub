# Setup Guide - OQR Dashboard

## Initial Setup (First Time)

### 1. Prerequisites
- Python 3.8+ installed
- MySQL/MariaDB server running and accessible
- Database credentials (host, user, password, database name)
- Git (optional, for version control)

### 2. Clone Project
```bash
# Navigate to workspace
cd x:\Streamlit

# (Or clone if from Git)
# git clone <repository> streamlit
# cd streamlit
```

### 3. Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

**Output should show:**
```
Successfully installed streamlit pandas sqlalchemy pymysql plotly ...
```

### 5. Configure Database
```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials
# Windows: notepad .env
# Linux/Mac: nano .env
```

**.env file template:**
```
DB_HOST=192.168.1.119
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=omisell_db
LOG_LEVEL=INFO
```

### 6. Test Database Connection
```bash
python -c "from src.db.connection import get_engine; engine = get_engine(); print('✓ Connected!' if engine else '✗ Failed')"
```

Or use the legacy test script (to be removed):
```bash
python test_connection.py
```

### 7. Run Application
```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

Application opens automatically in default browser.

## Troubleshooting Initial Setup

### Python Not Found
```bash
# Verify Python installation
python --version

# If not found, add Python to PATH or use python3
python3 --version
```

### Virtual Environment Issues
```bash
# On Windows, if activate doesn't work:
venv\Scripts\activate.bat

# Or use PowerShell:
venv\Scripts\Activate.ps1

# If PowerShell execution policy blocks: 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Pip Dependencies Fail
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt

# If specific package fails, install individually
pip install streamlit==1.31.1
pip install pandas==2.1.4
```

### Database Connection Failed
```bash
# 1. Check MySQL is running
# Windows: Services > MySQL
# Linux: sudo systemctl status mysql

# 2. Test connection directly
mysql -h 192.168.1.119 -u root -p

# 3. Check credentials in .env file
cat .env  # Linux/Mac
type .env # Windows

# 4. Check firewall allows connection
# Windows: Run > Windows Defender Firewall with Advanced Security
```

### Port Already in Use
```bash
# Streamlit uses port 8501 by default
# If busy, specify different port:
streamlit run app.py --server.port 8502
```

## Development Environment Setup

### 1. IDE Setup

#### VS Code
```bash
# Install Python extension
# Extensions > Python (Microsoft)

# Select interpreter
Ctrl+Shift+P > Python: Select Interpreter
# Choose: ./venv/Scripts/python.exe
```

#### PyCharm
```
1. Open Project
2. File > Settings > Project > Python Interpreter
3. Add Interpreter > Add Local Interpreter
4. Select: x:\Streamlit\venv\Scripts\python.exe
```

### 2. Code Formatting Tools (Optional)
```bash
# Install dev tools
pip install black flake8 mypy

# Format code
black src/ ui/ app.py

# Check style
flake8 src/ ui/ app.py --max-line-length=100

# Type check
mypy src/ ui/ --ignore-missing-imports
```

### 3. Pre-commit Hooks (Optional)
```bash
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  
  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']
EOF

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Regular Maintenance

### Daily
```bash
# Clear Streamlit cache (if needed)
streamlit cache clear

# Check for errors in logs
tail -f logs/dashboard.log  # Linux/Mac
type logs\dashboard.log     # Windows
```

### Weekly
```bash
# Update dependencies (carefully)
pip list --outdated
pip install --upgrade streamlit  # Update specific package
```

### Monthly
```bash
# Database maintenance
# Optimize tables (if using MySQL)
OPTIMIZE TABLE orders;
OPTIMIZE TABLE customers;

# Check slow queries
# Enable query log in MySQL config
# Analyze with EXPLAIN
EXPLAIN SELECT * FROM orders WHERE date > NOW() - INTERVAL 30 DAY;
```

## Production Deployment

### 1. Streamlit Cloud (Recommended for Simple Setups)
```bash
# 1. Push code to GitHub
git push origin main

# 2. Go to https://streamlit.io/cloud

# 3. Sign in with GitHub

# 4. "New app" > Select repository & branch

# 5. Secrets > Set database credentials
DB_HOST = xxx
DB_PASSWORD = xxx
...

# 6. Deploy automatically
```

### 2. Self-Hosted (AWS EC2, etc.)
```bash
# 1. SSH to server
ssh ubuntu@your-server.com

# 2. Clone repository
git clone <repo> oqr-dashboard
cd oqr-dashboard

# 3. Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Create systemd service
sudo nano /etc/systemd/system/streamlit.service
```

**Systemd service file:**
```ini
[Unit]
Description=OQR Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/oqr-dashboard
Environment="PATH=/home/ubuntu/oqr-dashboard/venv/bin"
ExecStart=/home/ubuntu/oqr-dashboard/venv/bin/streamlit run app.py \
  --server.port=8501 \
  --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 5. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl status streamlit

# 6. Check logs
sudo journalctl -u streamlit -f
```

### 3. Docker Deployment
```bash
# 1. Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
EOF

# 2. Build image
docker build -t oqr-dashboard:latest .

# 3. Run container
docker run -d \
  --name oqr-dashboard \
  -p 8501:8501 \
  -e DB_HOST=your-host \
  -e DB_PASSWORD=your-pass \
  -v logs:/app/logs \
  oqr-dashboard:latest

# 4. Check logs
docker logs -f oqr-dashboard
```

### 4. Docker Compose (Multiple Services)
```bash
# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      DB_HOST: mysql
      DB_USER: root
      DB_PASSWORD: ${DB_PASSWORD}
      DB_NAME: omisell_db
      LOG_LEVEL: INFO
    volumes:
      - ./logs:/app/logs
    depends_on:
      - mysql
    restart: always

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MYSQL_DATABASE: omisell_db
    volumes:
      - mysql_data:/var/lib/mysql
    restart: always

volumes:
  mysql_data:
EOF

# Run
docker-compose up -d
```

## Monitoring & Logging

### Enable File Logging
```bash
# In .env
LOG_FILE=logs/dashboard.log
LOG_LEVEL=INFO

# Create logs directory
mkdir logs

# View logs (real-time)
tail -f logs/dashboard.log  # Linux/Mac
Get-Content logs\dashboard.log -Wait  # Windows PowerShell
```

### Performance Monitoring
```python
# Check what's slow in app
# Enable debug logging in config.py
LOG_LEVEL = "DEBUG"

# Look for slow queries in logs
# grep "took" logs/dashboard.log
```

### Database Monitoring
```sql
-- View slow query log
SHOW VARIABLES LIKE 'slow_query_log';

-- Enable if not active
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- View slow queries
SELECT * FROM mysql.slow_log;
```

## Environment Variables

### Available Options
```bash
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=database

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/dashboard.log  # Leave empty for console only

# Streamlit (in .streamlit/config.toml)
[server]
port = 8501
address = 0.0.0.0
```

## Quick Commands Reference

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Run app
streamlit run app.py

# Run with debug logging
LOG_LEVEL=DEBUG streamlit run app.py

# Clear cache
streamlit cache clear

# Install new package
pip install package_name
pip freeze > requirements.txt  # Update requirements

# Check Python version
python --version

# List installed packages
pip list

# Update all packages
pip install --upgrade -r requirements.txt

# Test database connection
python -c "from src.db.connection import get_engine; print(get_engine())"
```

## Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| Port 8501 in use | `streamlit run app.py --server.port 8502` |
| Module not found | Ensure venv activated, reinstall: `pip install -r requirements.txt` |
| Database connection failed | Check `.env` credentials, verify MySQL running |
| Slow performance | Increase cache TTL in `config.py`, optimize SQL queries |
| Memory leak | Restart app, check for unfinished iterators in code |
| Import errors | Check `__init__.py` files exist in all packages |
| Cached data stale | Run `streamlit cache clear` |

## Next Steps

1. ✅ Complete setup from section 1-7 above
2. ✅ Verify app runs without errors: `streamlit run app.py`
3. ✅ Test all filters work correctly
4. ✅ Check data displays properly
5. ✅ Review logs: `tail -f logs/dashboard.log`
6. ✅ Read [ARCHITECTURE.md](ARCHITECTURE.md) for code structure
7. ✅ Read [CODING_STANDARDS.md](CODING_STANDARDS.md) before contributing

---

**Last Updated**: February 2025  
**Version**: 1.0

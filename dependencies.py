# dependencies.py
from database.db import Database
from database.queries import QueryManager

# Khởi tạo 1 lần duy nhất tại đây
db = Database()
qm = QueryManager(db)
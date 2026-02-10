import os
from datetime import datetime, timedelta

class QueryManager:
    def __init__(self, db):
        self.db = db
        # Setup đường dẫn folder query
        current_file_path = os.path.abspath(__file__)
        database_dir = os.path.dirname(current_file_path)
        self.query_folder = os.path.normpath(os.path.join(database_dir, '..', 'query'))

    def _load_sql(self, filename):
        path = os.path.join(self.query_folder, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        print(f"❌ LỖI: Không tìm thấy file {path}")
        return ""

    # ============================================================
    # 1. CÁC HÀM HELPER (CỐT LÕI ĐỂ TÁI SỬ DỤNG)
    # ============================================================

    def _build_filter_clause(self, filters):
        """Tạo mệnh đề WHERE động dựa trên filter dict"""
        clauses = []
        params = []
        
        # Mapping: Tên trên URL -> Tên cột trong SQL (Alias phải khớp file SQL)
        mapping = {
            'shops': 'ShopName',       
            'platforms': 'PlatformName', 
            'statuses': 'StatusName',
            'brands': 'brand'
        }

        if filters:
            for url_param, db_column in mapping.items():
                values = filters.get(url_param)
                # Chỉ xử lý nếu có giá trị, không rỗng, và không phải 'All'
                if values and len(values) > 0 and values[0] != '':
                    if 'all' in values or 'All' in values:
                        continue 
                    
                    placeholders = ', '.join(['%s'] * len(values))
                    clauses.append(f"AND {db_column} IN ({placeholders})")
                    params.extend(values)

        return " ".join(clauses), params

    def _execute_date_range_query(self, sql_filename, start_date, end_date, filter_dict=None):
        """
        Hàm tổng quát để chạy mọi query có dạng: 
        SELECT ... WHERE CreatedTime BETWEEN %s AND %s {filters}
        """
        # 1. Chuẩn hóa ngày tháng
        start_full = f"{start_date} 00:00:00"
        end_full = f"{end_date} 23:59:59"

        # 2. Xử lý Filter
        filter_sql, filter_params = self._build_filter_clause(filter_dict)

        # 3. Load SQL
        sql_template = self._load_sql(sql_filename)
        if not sql_template:
            return []

        # 4. Inject Filter vào SQL
        try:
            final_sql = sql_template.format(filters=filter_sql)
        except KeyError:
            final_sql = sql_template

        # 5. Ghép tham số: [Start, End] + [Filter Params]
        params = [start_full, end_full] + filter_params
        
        # ==========================================================
        # 🛠️ DEBUG BLOCK: IN QUERY RA CONSOLE
        # ==========================================================
        try:
            # Tạo list tham số hiển thị (Thêm dấu nháy '' nếu là chuỗi)
            debug_params = []
            for p in params:
                if isinstance(p, str):
                    # Nếu là string -> Thêm dấu nháy đơn 'giatri'
                    debug_params.append(f"'{p}'")
                elif p is None:
                    debug_params.append('NULL')
                else:
                    # Số hoặc đối tượng khác -> Giữ nguyên
                    debug_params.append(str(p))
            
            # Thay thế %s bằng giá trị thực để tạo câu SQL hoàn chỉnh
            # Lưu ý: Replace này chỉ mang tính tương đối để debug
            readable_sql = final_sql.replace('%s', '{}').format(*debug_params)
            
            print("\n" + "="*60)
            print(f"🚀 [DEBUG SQL] File: {sql_filename}")
            print("-" * 60)
            print(readable_sql) # <--- COPY CÁI NÀY VÀO DB
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"⚠️ Lỗi hiển thị Debug SQL: {e}")
            # Fallback: In dạng thô nếu lỗi format
            print("SQL Raw:", final_sql)
            print("Params:", params)
        # ==========================================================

        # 6. Execute (Vẫn dùng parameterized query để an toàn bảo mật)
        return self.db.execute_query(final_sql, tuple(params))

    # ============================================================
    # 2. CÁC HÀM NGHIỆP VỤ (GIỜ ĐÃ RẤT NGẮN GỌN)
    # ============================================================

    def get_filters(self, start_date, end_date):
        """Lấy danh sách dữ liệu cho dropdown filter"""
        filters = {}
        # Tận dụng hàm execute tổng quát (không truyền filter_dict vì đây là hàm lấy filter)
        tasks = {
            'platforms': 'get_Platform.sql',
            'shops': 'get_Shop_Name.sql',
            'statuses': 'get_Status_Name.sql',
            'brands': 'get_Brand_Name.sql' # Nhớ tạo file này
        }
        for key, filename in tasks.items():
            data = self._execute_date_range_query(filename, start_date, end_date)
            filters[key] = data if data else []
        return filters

    def get_hourly_trend(self, start_date, end_date, filter_dict=None):
        return self._execute_date_range_query('get_Hourly_Trend.sql', start_date, end_date, filter_dict)

    def get_order_status(self, start_date, end_date, filter_dict=None):
        return self._execute_date_range_query('get_OrderStatus.sql', start_date, end_date, filter_dict)

    def get_province_data(self, start_date, end_date, filter_dict=None):
        return self._execute_date_range_query('get_Province.sql', start_date, end_date, filter_dict)

    # ============================================================
    # 3. HÀM KPI PHỨC TẠP (GIỮ RIÊNG VÌ LOGIC KHÁC BIỆT)
    # ============================================================

    def get_kpi_growth(self, start_date_str, end_date_str, filter_dict=None):
        # 1. Tính toán ngày tháng (Giữ nguyên)
        fmt = '%Y-%m-%d'
        try:
            curr_start = datetime.strptime(start_date_str, fmt)
            curr_end = datetime.strptime(end_date_str, fmt)
        except ValueError:
            return {}

        delta = curr_end - curr_start
        prev_end = curr_start - timedelta(days=1)
        prev_start = prev_end - delta

        # Convert to string
        p_curr_start = f"{curr_start.strftime(fmt)} 00:00:00"
        p_curr_end = f"{curr_end.strftime(fmt)} 23:59:59"
        p_prev_start = f"{prev_start.strftime(fmt)} 00:00:00"
        p_prev_end = f"{prev_end.strftime(fmt)} 23:59:59"
        
        # Range tổng cho WHERE
        p_total_start = p_prev_start
        p_total_end = p_curr_end

        # 2. Xử lý Filter (Dùng chung cho cả 2 query)
        filter_sql, filter_params = self._build_filter_clause(filter_dict)

        # ==============================================================================
        # BƯỚC A: LẤY SỐ LIỆU QUANTITY (TỪ INVENTORY)
        # ==============================================================================
        quantity_data = {'Quantity': 0, 'QuantityGrowth': 0}
        
        sql_qty = self._load_sql('get_Quantity.sql')
        if sql_qty:
            try:
                final_sql_qty = sql_qty.format(filters=filter_sql)
                
                # Params cho Quantity: [Curr, Prev, RangeTotal] + Filter
                params_qty = [
                    p_curr_start, p_curr_end,   # CASE WHEN Current
                    p_prev_start, p_prev_end,   # CASE WHEN Previous
                    p_total_start, p_total_end  # WHERE Range
                ]
                if filter_params:
                    params_qty.extend(filter_params)
                
                res_qty = self.db.execute_query(final_sql_qty, tuple(params_qty))
                if res_qty:
                    quantity_data = res_qty[0] # Lấy kết quả Quantity & Growth
            except Exception as e:
                print(f"Error getting Quantity: {e}")

        # ==============================================================================
        # BƯỚC B: LẤY SỐ LIỆU REVENUE & ORDERS (TỪ CATALOGUE)
        # ==============================================================================
        kpi_data = {'Revenue': 0, 'Orders': 0, 'AOV': 0, 'RevenueGrowth': 0, 'OrdersGrowth': 0, 'AovGrowth': 0}
        
        sql_kpi = self._load_sql('get_KPI_Growth.sql')
        if sql_kpi:
            try:
                final_sql_kpi = sql_kpi.format(filters=filter_sql)
                
                # Params cho KPI chính: [CurrRev, CurrOrd, PrevRev, PrevOrd, RangeTotal] + Filter
                # Lưu ý: File get_KPI_Growth.sql cần bỏ phần tính Quantity đi để khớp params
                params_kpi = [
                    p_curr_start, p_curr_end, # Curr Revenue
                    p_curr_start, p_curr_end, # Curr Orders
                    p_prev_start, p_prev_end, # Prev Revenue
                    p_prev_start, p_prev_end, # Prev Orders
                    p_total_start, p_total_end # WHERE Range
                ]
                if filter_params:
                    params_kpi.extend(filter_params)

                res_kpi = self.db.execute_query(final_sql_kpi, tuple(params_kpi))
                if res_kpi:
                    kpi_data = res_kpi[0]
            except Exception as e:
                print(f"Error getting KPI: {e}")

        # ==============================================================================
        # BƯỚC C: GỘP KẾT QUẢ (MERGE)
        # ==============================================================================
        # Gộp 2 dictionary lại thành 1 để trả về cho Dashboard
        final_result = {**kpi_data, **quantity_data}
        
        return final_result
    


    def get_revenue_by_brand_platform(self, start_date_str, end_date_str, filter_dict=None):
        # 1. Chuẩn bị tham số ngày tháng
        start_full = f"{start_date_str} 00:00:00"
        end_full = f"{end_date_str} 23:59:59"
        
        # 2. Xử lý Filter
        filter_sql, filter_params = self._build_filter_clause(filter_dict)
        params = [start_full, end_full] + filter_params

        # 3. Query Database
        sql = self._load_sql('get_Revenue_By_Brand_Platform.sql')
        if not sql: return {}
        
        try:
            final_sql = sql.format(filters=filter_sql)
            raw_data = self.db.execute_query(final_sql, tuple(params))
        except Exception as e:
            print(f"Error: {e}")
            return {}

        if not raw_data:
            return {'categories': [], 'series': []}

        # --- 4. PIVOT DỮ LIỆU (QUAN TRỌNG) ---
        
        # B1: Lấy danh sách tất cả Brand (Unique) và Platform (Unique)
        # Sắp xếp Brand theo tổng doanh thu (để biểu đồ đẹp)
        brand_revenue = {}
        all_platforms = set()

        for row in raw_data:
            b = row['brand']
            p = row['PlatformName']
            rev = float(row['TotalRevenue'])
            
            all_platforms.add(p)
            brand_revenue[b] = brand_revenue.get(b, 0) + rev

        # Sort brand giảm dần theo doanh thu
        sorted_brands = sorted(brand_revenue.keys(), key=lambda k: brand_revenue[k], reverse=True)
        sorted_platforms = sorted(list(all_platforms))

        # B2: Build Series cho Highcharts
        # Cấu trúc: series = [{name: 'Shopee', data: [100, 200...]}, {name: 'Tiktok', data: [...]}]
        series_data = []

        for platform in sorted_platforms:
            p_data = []
            for brand in sorted_brands:
                # Tìm giá trị của (Brand này + Platform này) trong raw_data
                # Nếu không có thì bằng 0
                val = next((float(item['TotalRevenue']) for item in raw_data if item['brand'] == brand and item['PlatformName'] == platform), 0)
                p_data.append(val)
            
            series_data.append({
                'name': platform,
                'data': p_data
            })

        return {
            'categories': sorted_brands, # Trục tung
            'series': series_data        # Dữ liệu
        }
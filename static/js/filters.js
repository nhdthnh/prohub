document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. HÀM APPLY FILTER (Gửi dữ liệu lên URL) ---
    function applyFilters() {
        const params = new URLSearchParams(window.location.search);
        
        // Lấy value hiện tại đang chọn trong Virtual Select
        const brands = document.querySelector('#brand-select').value;
        const platforms = document.querySelector('#platform-select').value;
        const shops = document.querySelector('#shop-select').value;
        const statuses = document.querySelector('#status-select').value;

        // Xóa param cũ
        params.delete('brands');
        params.delete('platforms');
        params.delete('shops');
        params.delete('statuses');

        // Hàm append an toàn
        function appendParams(key, values) {
            if (Array.isArray(values)) {
                if (values.length > 0) {
                    values.forEach(v => params.append(key, v));
                }
            } else if (values) {
                params.append(key, values);
            }
        }

        appendParams('brands', brands);
        appendParams('platforms', platforms);
        appendParams('shops', shops);
        appendParams('statuses', statuses);

        // Reload trang
        window.location.search = params.toString();
    }

    // --- 2. HÀM LẤY DATA TỪ URL ---
    function getQueryValues(key) {
        // getAll trả về mảng các giá trị (VD: ['Samsung', 'Apple'])
        // Tự động giải mã URL (%20 -> khoảng trắng)
        return new URLSearchParams(window.location.search).getAll(key);
    }

    // --- 3. KHỞI TẠO VIRTUAL SELECT ---
    const commonConfig = {
        search: true,
        showValueAsTags: false,
    };

    // Khởi tạo (Lưu ý: Không cần truyền selectedValue ở đây nữa, ta sẽ set ở bước 4 cho chắc ăn)
    VirtualSelect.init({ ...commonConfig, ele: '#brand-select', placeholder: 'Chọn Brand', allOptionsSelectedText: 'Brand' });
    VirtualSelect.init({ ...commonConfig, ele: '#platform-select', placeholder: 'Chọn Nền tảng', allOptionsSelectedText: 'Nền tảng' });
    VirtualSelect.init({ ...commonConfig, ele: '#shop-select', placeholder: 'Chọn Shop', allOptionsSelectedText: 'Shop' });
    VirtualSelect.init({ ...commonConfig, ele: '#status-select', placeholder: 'Chọn Trạng thái', allOptionsSelectedText: 'Trạng thái' });

    // --- 4. FORCE UPDATE (ÉP HIỂN THỊ GIÁ TRỊ TỪ URL) ---
    // Đây là bước quan trọng nhất để sửa lỗi hiển thị "ALL"
    
    function setDropdownValue(id, urlParam) {
        const element = document.querySelector(id);
        const valuesFromUrl = getQueryValues(urlParam);
        
        // Chỉ set nếu trên URL có giá trị
        if (valuesFromUrl && valuesFromUrl.length > 0) {
            // setValue là hàm có sẵn của thư viện VirtualSelect
            // Nó sẽ so sánh value với options và tick chọn cái đúng
            element.setValue(valuesFromUrl);
        }
    }

    // Gọi hàm set cho từng cái
    setDropdownValue('#brand-select', 'brands');
    setDropdownValue('#platform-select', 'platforms');
    setDropdownValue('#shop-select', 'shops');
    setDropdownValue('#status-select', 'statuses');


    // --- 5. GÁN SỰ KIỆN CLICK CHO NÚT APPLY ---
    const applyBtn = document.querySelector('#btn-apply-filter');
    if (applyBtn) {
        applyBtn.addEventListener('click', applyFilters);
    }
});



document.addEventListener('DOMContentLoaded', function() {
    
    // --- KHAI BÁO CÁC ID CỦA NÚT ---
    const btnApply = document.querySelector('#btn-apply-filter');
    const btnReset = document.querySelector('#btn-reset-filter');

    // Danh sách các param cần theo dõi để bật nút Reset
    const filterKeys = ['brands', 'platforms', 'shops', 'statuses'];

    // 1. HÀM CHECK TRẠNG THÁI NÚT RESET
    function updateResetButtonState() {
        const params = new URLSearchParams(window.location.search);
        let hasFilter = false;

        // Kiểm tra xem URL có chứa bất kỳ key nào trong danh sách filter không
        for (const key of filterKeys) {
            if (params.has(key)) {
                hasFilter = true;
                break;
            }
        }

        // Cập nhật giao diện nút
        if (hasFilter) {
            btnReset.classList.remove('disabled');
            btnReset.removeAttribute('disabled');
        } else {
            btnReset.classList.add('disabled');
            btnReset.setAttribute('disabled', 'true');
        }
    }

    // 2. HÀM XỬ LÝ KHI BẤM RESET
    function handleReset() {
        const currentParams = new URLSearchParams(window.location.search);
        const newParams = new URLSearchParams();

        // Chỉ giữ lại ngày tháng (start, end)
        if (currentParams.has('start')) newParams.append('start', currentParams.get('start'));
        if (currentParams.has('end')) newParams.append('end', currentParams.get('end'));

        // Reload trang với URL sạch
        window.location.search = newParams.toString();
    }

    // --- GÁN SỰ KIỆN ---
    
    // Chạy check ngay khi load trang
    updateResetButtonState();

    if (btnReset) {
        btnReset.addEventListener('click', handleReset);
    }
    
    // ... (Giữ nguyên các code xử lý Apply Filter cũ của bạn ở dưới) ...
});
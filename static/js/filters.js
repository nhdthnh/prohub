document.addEventListener('DOMContentLoaded', function() {
    
    // =========================================================================
    // PHẦN 1: LOGIC NÚT RESET
    // =========================================================================
    const btnReset = document.querySelector('#btn-reset-filter');
    const filterKeys = ['brands', 'platforms', 'shops', 'statuses'];

    function updateResetButtonState() {
        const params = new URLSearchParams(window.location.search);
        let hasFilter = false;
        for (const key of filterKeys) {
            if (params.has(key)) {
                hasFilter = true;
                break;
            }
        }
        if (hasFilter) {
            btnReset?.classList.remove('disabled');
            btnReset?.removeAttribute('disabled');
        } else {
            btnReset?.classList.add('disabled');
            btnReset?.setAttribute('disabled', 'true');
        }
    }

    function handleReset() {
        const currentParams = new URLSearchParams(window.location.search);
        const newParams = new URLSearchParams();
        // Giữ lại ngày tháng
        if (currentParams.has('start')) newParams.append('start', currentParams.get('start'));
        if (currentParams.has('end')) newParams.append('end', currentParams.get('end'));
        
        // Khi reload lại URL sạch, logic ở PHẦN 2 (TH2) sẽ chạy và tự apply default
        window.location.search = newParams.toString();
    }

    updateResetButtonState();
    if (btnReset) btnReset.addEventListener('click', handleReset);


    // =========================================================================
    // PHẦN 2: KHỞI TẠO & LOGIC DEFAULT (QUAN TRỌNG NHẤT)
    // =========================================================================
    
    const commonConfig = { search: true, showValueAsTags: false };
    
    VirtualSelect.init({ ...commonConfig, ele: '#brand-select', placeholder: 'Brand', allOptionsSelectedText: 'Brand' });
    VirtualSelect.init({ ...commonConfig, ele: '#platform-select', placeholder: 'Nền tảng', allOptionsSelectedText: 'Nền tảng' });
    VirtualSelect.init({ ...commonConfig, ele: '#shop-select', placeholder: 'Shop', allOptionsSelectedText: 'Shop' });
    VirtualSelect.init({ ...commonConfig, ele: '#status-select', placeholder: 'Trạng thái', allOptionsSelectedText: 'Trạng thái' });

    function getQueryValues(key) {
        return new URLSearchParams(window.location.search).getAll(key);
    }

    function setDropdownValue(id, urlParam) {
        const element = document.querySelector(id);
        const valuesFromUrl = getQueryValues(urlParam);
        if (valuesFromUrl && valuesFromUrl.length > 0) {
            element.setValue(valuesFromUrl);
        }
    }

    setDropdownValue('#brand-select', 'brands');
    setDropdownValue('#platform-select', 'platforms');
    setDropdownValue('#shop-select', 'shops');

    // --- XỬ LÝ STATUS: NẾU CHƯA CÓ TRÊN URL -> TỰ ĐỘNG APPLY VÀ RELOAD ---
    const statusSelect = document.querySelector('#status-select');
    const statusParams = getQueryValues('statuses');

    if (statusParams && statusParams.length > 0) {
        // TH1: Đã có filter trên URL -> Hiển thị visual cho đúng
        statusSelect.setValue(statusParams);
    } else {
        // TH2: Chưa có filter (Mới mở trang) -> TÍNH TOÁN VÀ RELOAD TRANG NGAY
        
        const blackList = [
            'ngoại lệ',
            'huỷ bởi đối tác',
            'hoàn thành công',     // User yêu cầu bỏ default
            'đang chuyển hoàn',
            'huỷ bởi người bán',
            'mất hàng',
            'huỷ bởi hệ thống',
            'đang chờ hủy',
            'đang chờ huỷ'
        ];

        const allOptions = Array.from(statusSelect.options).map(opt => opt.value);
        
        const goodStatuses = allOptions.filter(val => {
            const text = val.toLowerCase().trim();
            if (blackList.includes(text)) return false;
            if (text.includes('huỷ') || text.includes('hủy')) return false;
            return true;
        });

        // 1. Set visual cho dropdown (để đỡ bị giật visual)
        statusSelect.setValue(goodStatuses);

        // 2. [MỚI] Tự động xây dựng URL và Reload trang để áp dụng dữ liệu
        const params = new URLSearchParams(window.location.search);
        
        // Thêm danh sách Good Statuses vào URL
        goodStatuses.forEach(st => params.append('statuses', st));

        // Redirect ngay lập tức để Server lọc dữ liệu
        window.location.search = params.toString();
    }


    // =========================================================================
    // PHẦN 3: NÚT APPLY THỦ CÔNG
    // =========================================================================
    const applyBtn = document.querySelector('#btn-apply-filter');
    if (applyBtn) {
        applyBtn.addEventListener('click', function() {
            const params = new URLSearchParams(window.location.search);
            
            const brands = document.querySelector('#brand-select').value;
            const platforms = document.querySelector('#platform-select').value;
            const shops = document.querySelector('#shop-select').value;
            const statuses = document.querySelector('#status-select').value;

            params.delete('brands'); params.delete('platforms'); 
            params.delete('shops'); params.delete('statuses');

            function appendParams(key, values) {
                if (Array.isArray(values)) {
                    if (values.length > 0) values.forEach(v => params.append(key, v));
                } else if (values) {
                    params.append(key, values);
                }
            }

            appendParams('brands', brands);
            appendParams('platforms', platforms);
            appendParams('shops', shops);
            appendParams('statuses', statuses);

            window.location.search = params.toString();
        });
    }
});
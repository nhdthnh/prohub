document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Cấu hình Filter Brand
    VirtualSelect.init({
        ele: '#brand-select',
        selectAllText: 'Chọn tất cả',
        search: true,
        placeholder: 'Chọn Brand',
        noOptionsText: 'Không có dữ liệu',
        noSearchResultsText: 'Không tìm thấy kết quả',
        searchPlaceholderText: 'Tìm kiếm...',
        optionsCount: 4, 

        // --- CẤU HÌNH MỚI ---
        allOptionsSelectedText: 'Brand', // 1. Khi chọn All -> Hiện chữ "Brand"
        showValueAsTags: false,          // 2. Tắt dạng thẻ tag -> Hiển thị text cách nhau dấu phẩy
    });

    // 2. Cấu hình Filter Nền tảng
    VirtualSelect.init({
        ele: '#platform-select',
        selectAllText: 'Chọn tất cả',
        placeholder: 'Chọn Nền tảng',
        search: true,
        searchPlaceholderText: 'Tìm kiếm...',

        // --- CẤU HÌNH MỚI ---
        allOptionsSelectedText: 'Nền tảng', // Khi chọn All -> Hiện chữ "Nền tảng"
        showValueAsTags: false,
    });

    // 3. Cấu hình Filter Shop
    VirtualSelect.init({
        ele: '#shop-select',
        selectAllText: 'Chọn tất cả',
        placeholder: 'Chọn Shop',
        search: true,
        searchPlaceholderText: 'Tìm kiếm...',

        // --- CẤU HÌNH MỚI ---
        allOptionsSelectedText: 'Shop', // Khi chọn All -> Hiện chữ "ShopName"
        showValueAsTags: false,
    });

    // 4. Cấu hình Filter Trạng thái
    VirtualSelect.init({
        ele: '#status-select',
        selectAllText: 'Chọn tất cả',
        placeholder: 'Chọn Trạng thái',
        search: true,
        searchPlaceholderText: 'Tìm kiếm...',

        // --- CẤU HÌNH MỚI ---
        allOptionsSelectedText: 'Trạng thái', // Khi chọn All -> Hiện chữ "StatusName"
        showValueAsTags: false,
    });
});
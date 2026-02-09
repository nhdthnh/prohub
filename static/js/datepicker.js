document.addEventListener('DOMContentLoaded', function() {
    // 1. Lấy tham số ngày từ URL hiện tại (để giữ nguyên ngày khi F5)
    const urlParams = new URLSearchParams(window.location.search);
    const startParam = urlParams.get('start');
    const endParam = urlParams.get('end');
    
    // Mặc định là hôm nay nếu không có trên URL
    const defaultDate = (startParam && endParam) ? [startParam, endParam] : ["today", "today"];

    flatpickr("#dateRangePicker", {
        mode: "range",
        dateFormat: "Y-m-d", // Định dạng chuẩn SQL (Năm-Tháng-Ngày)
        defaultDate: defaultDate, 
        showMonths: 2,
        
        // --- SỰ KIỆN QUAN TRỌNG NHẤT ---
        onChange: function(selectedDates, dateStr, instance) {
            // Chỉ chạy khi đã chọn đủ 2 ngày (Từ ngày -> Đến ngày)
            if (selectedDates.length === 2) {
                const startDate = instance.formatDate(selectedDates[0], "Y-m-d");
                const endDate = instance.formatDate(selectedDates[1], "Y-m-d");

                // Tạo URL mới chứa tham số start & end
                const currentUrl = new URL(window.location);
                currentUrl.searchParams.set('start', startDate);
                currentUrl.searchParams.set('end', endDate);

                // Reload trang với tham số mới
                window.location.href = currentUrl.toString();
            }
        }
    });
});


/* static/js/datepicker.js */
flatpickr("#dateRangePicker", {
    mode: "range",
    dateFormat: "Y-m-d",
    // ... các config khác ...
    
    // Thêm sự kiện onClose để tự động điền End Date nếu user chỉ chọn 1 ngày
    onClose: function(selectedDates, dateStr, instance) {
        if (selectedDates.length === 1) {
            // Nếu chỉ chọn 1 ngày, coi như Start = End
            const date = instance.formatDate(selectedDates[0], "Y-m-d");
            
            // Reload trang ngay lập tức
            const currentUrl = new URL(window.location);
            currentUrl.searchParams.set('start', date);
            currentUrl.searchParams.set('end', date);
            window.location.href = currentUrl.toString();
        }
    }
});
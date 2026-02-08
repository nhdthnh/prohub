// Khởi tạo Flatpickr khi DOM đã load xong
document.addEventListener('DOMContentLoaded', function() {
    flatpickr("#dateRangePicker", {
        mode: "range",
        dateFormat: "M j, Y",
        defaultDate: ["today", "today"],
        showMonths: 2,
        onChange: function(selectedDates, dateStr, instance) {
            console.log("Ngày đã chọn:", dateStr);
            // Tại đây có thể gọi hàm để reload dữ liệu bảng
        }
    });
});
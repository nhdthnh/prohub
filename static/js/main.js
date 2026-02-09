document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.getElementById("toggleSidebar");
    
    // Nút này quan trọng: Toggle class cho BODY
    if (toggleBtn) {
        toggleBtn.addEventListener("click", function() {
            // Thêm/Xóa class 'sidebar-collapsed' trên thẻ BODY
            document.body.classList.toggle("sidebar-collapsed");

            // Lưu trạng thái vào LocalStorage (để F5 không bị mất)
            const isCollapsed = document.body.classList.contains("sidebar-collapsed");
            localStorage.setItem("sidebarCollapsed", isCollapsed);
            
            // Trigger sự kiện resize để các biểu đồ Highcharts/ChartJS tự vẽ lại kích thước
            setTimeout(() => {
                window.dispatchEvent(new Event('resize'));
            }, 300);
        });
    }

    // Giữ trạng thái khi F5
    if (localStorage.getItem("sidebarCollapsed") === "true") {
        document.body.classList.add("sidebar-collapsed");
    }
});
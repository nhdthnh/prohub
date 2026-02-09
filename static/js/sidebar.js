/**
 * Hàm xử lý đóng mở nhóm menu trong Sidebar
 * Được gọi từ sự kiện onclick bên HTML
 */
function toggleGroup(headerElement) {
    const group = headerElement.parentElement;
    group.classList.toggle('collapsed');
}

/**
 * Hàm xử lý thu gọn / mở rộng Sidebar
 */
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
}
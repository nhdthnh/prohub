/**
 * Hàm xử lý đóng mở nhóm menu trong Sidebar
 * Được gọi từ sự kiện onclick bên HTML
 */
function toggleGroup(headerElement) {
    const group = headerElement.parentElement;
    group.classList.toggle('collapsed');
}
// Hàm khởi tạo biểu đồ 2 trục (Dual Axis)
function initDualAxisChart(labels, revenueData, ordersData) {
    const canvas = document.getElementById('revenueChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // Gradient màu xanh cho doanh thu
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Doanh thu',
                    data: revenueData,
                    borderColor: '#3b82f6', // Xanh dương
                    backgroundColor: gradient,
                    yAxisID: 'y', // Trục trái
                    fill: true,
                    tension: 0.4,
                    order: 2
                },
                {
                    label: 'Đơn hàng',
                    data: ordersData,
                    borderColor: '#f97316', // Cam
                    backgroundColor: 'rgba(249, 115, 22, 0.5)',
                    yAxisID: 'y1', // Trục phải
                    fill: false,
                    borderDash: [5, 5], // Nét đứt
                    tension: 0.4,
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top', // Đưa chú thích lên trên cùng
                    align: 'end',    // Căn phải để đỡ che tiêu đề
                    labels: {
                        usePointStyle: true,
                        boxWidth: 8
                    }
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    beginAtZero: true,
                    title: { display: true, text: 'Doanh thu (VNĐ)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    beginAtZero: true,
                    grid: { drawOnChartArea: false }, // Tắt lưới ngang của trục phải
                    title: { display: true, text: 'Số đơn' }
                }
            },
            responsive: true,
            maintainAspectRatio: false, // Quan trọng: Để nó tự co giãn theo khung mới
            layout: {
                padding: {
                    top: 20,    // Thêm khoảng trống bên trên để không bị cắt số
                    left: 10,
                    right: 10
                }
            },
        }
    });
}
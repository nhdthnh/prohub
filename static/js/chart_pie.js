function initPieChart(labels, data, centerElementId, totalValue) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    const centerDiv = document.getElementById(centerElementId);

    // Bảng màu giống ảnh mẫu (Xanh Cyan, Xanh Dương...)
    const colors = [
        '#06b6d4', // Cyan
        '#3b82f6', // Blue
        '#8b5cf6', // Violet
        '#f43f5e', // Rose
        '#f59e0b', // Amber
        '#10b981', // Emerald
        '#64748b'  // Slate
    ];

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%', // Làm vòng tròn mỏng đi để chỗ trống ở giữa rộng hơn
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false } // Tắt tooltip mặc định để dùng hiệu ứng center text
            },
            onHover: (event, elements) => {
                if (elements.length > 0) {
                    // Khi hover vào 1 miếng bánh
                    const index = elements[0].index;
                    const value = data[index];
                    const label = labels[index];

                    // Đổi nội dung ở giữa
                    centerDiv.innerHTML = `
                        <div style="font-size: 12px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px;">${label}</div>
                        <div style="font-size: 24px; font-weight: 700; color: ${colors[index % colors.length]};">
                            ${new Intl.NumberFormat('en-US').format(value)}
                        </div>
                    `;
                } else {
                    // Khi chuột đi ra ngoài -> Trả về Tổng
                    centerDiv.innerHTML = `
                        <div style="font-size: 12px; color: #64748b;">Tổng đơn</div>
                        <div style="font-size: 24px; font-weight: 700; color: #334155;">
                            ${new Intl.NumberFormat('en-US').format(totalValue)}
                        </div>
                    `;
                }
            }
        }
    });
}
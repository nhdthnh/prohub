// static/js/chart_factory.js

// --- CẤU HÌNH CHUNG CHO TOÀN BỘ CHART ---
const commonOptions = {
    chart: {
        style: { fontFamily: 'Inter, sans-serif' },
        backgroundColor: 'transparent', // Nền trong suốt để ăn theo màu thẻ chứa
        spacingTop: 20
    },
    credits: { enabled: false },
    title: { text: null },
    // Cấu hình Tooltip chung cho đẹp (Nền tối, chữ trắng)
    tooltip: {
        backgroundColor: 'rgba(30, 41, 59, 0.9)', // Màu xanh đen đậm
        style: { color: '#f1f5f9', fontSize: '13px' },
        borderRadius: 8,
        borderWidth: 0,
        shadow: false,
        useHTML: true,
        headerFormat: '<span style="font-size: 12px; color: #94a3b8">{point.key}</span><br/>'
    },
    // Làm mờ đường lưới trục Y cho thoáng
    yAxis: {
        gridLineColor: '#f1f5f9',
        labels: { style: { color: '#64748b' } }
    },
    xAxis: {
        lineColor: '#e2e8f0',
        tickColor: '#e2e8f0',
        labels: { style: { color: '#64748b' } }
    },
    legend: {
        itemStyle: { color: '#475569', fontWeight: '500' },
        itemHoverStyle: { color: '#000' }
    }
};


window.ChartFactory = {
    // ========================================================================
    // 1. BAR CHART (Stacked - Doanh số theo Brand/Platform)
    // ========================================================================
    createStackedBar: function(id, data) {
        if (!data || !data.series || data.series.length === 0) {
            console.warn("No data for Bar Chart:", id); return;
        }
        
        const platformColors = {
            'Shopee': '#ee4d2d', 'Tiktok Shop': '#000000', 
            'Lazada': '#0f156d', 'Haravan': '#2563eb', 
            'Shopify': '#96bf48', 'Tiki': '#1a94ff'
        };

        // Map màu và làm đậm cột hơn một chút
        const coloredSeries = data.series.map(s => ({
            ...s, 
            color: platformColors[s.name] || '#94a3b8',
            borderWidth: 0 // Bỏ viền trắng giữa các đoạn stack
        }));

        Highcharts.chart(id, {
            ...commonOptions,
            chart: { ...commonOptions.chart, type: 'bar' },
            xAxis: { categories: data.categories, ...commonOptions.xAxis },
            yAxis: { 
                ...commonOptions.yAxis,
                title: { text: null }, // Bỏ chữ "Doanh số (VNĐ)" cho gọn
                stackLabels: { 
                    enabled: true, 
                    style: { fontWeight: 'bold', color: '#64748b' },
                    formatter: function() {
                        // Format số lớn (ví dụ 1.2M, 500K)
                        if (this.total >= 1000000000) return (this.total / 1000000000).toFixed(1) + 'B';
                        if (this.total >= 1000000) return (this.total / 1000000).toFixed(1) + 'M';
                        if (this.total >= 1000) return (this.total / 1000).toFixed(0) + 'K';
                        return this.total;
                    }
                }
            },
            plotOptions: { 
                series: { 
                    stacking: 'normal',
                    borderRadius: 4 // Bo tròn góc cột cho mềm mại
                } 
            },
            tooltip: {
                 ...commonOptions.tooltip,
                 pointFormat: '<span style="color:{series.color}">●</span> {series.name}: <b>{point.y:,.0f} đ</b><br/>',
                 footerFormat: 'Tổng: <b>{point.total:,.0f} đ</b>'
            },
            series: coloredSeries
        });
    },

    // ========================================================================
    // 2. LINE CHART (Dual Axis - Doanh thu & Đơn hàng theo giờ)
    // ========================================================================
    createDualLine: function(id, data) {
        if (!data || !data.hours || data.hours.length === 0) {
            console.warn("No data for Line Chart:", id); return;
        }
        Highcharts.chart(id, {
            ...commonOptions,
            chart: { ...commonOptions.chart, zoomType: 'xy', marginTop: 30 },
            xAxis: { ...commonOptions.xAxis, categories: data.hours, crosshair: true },
            yAxis: [
                { // Trục trái (Doanh thu)
                    ...commonOptions.yAxis,
                    title: { text: null },
                    labels: { 
                        style: { color: '#2563eb' }, // Màu xanh theo line doanh thu
                        formatter: function() { return this.value >= 1000000 ? (this.value/1000000).toFixed(1) + 'M' : Highcharts.numberFormat(this.value, 0); }
                    } 
                }, 
                { // Trục phải (Đơn hàng)
                    ...commonOptions.yAxis,
                    title: { text: null },
                    opposite: true,
                    labels: { style: { color: '#f97316' } } // Màu cam theo line đơn hàng
                }
            ],
            tooltip: {
                ...commonOptions.tooltip,
                shared: true,
            },
            exporting: {
                buttons: {
                    contextButton: {
                        verticalAlign: 'top',
                        y: -25 // <--- Đẩy nút lên cao hơn so với khu vực vẽ
                    }
                }
            },
            plotOptions: {
                series: {
                    // --- TĂNG ĐỘ DÀY LINE Ở ĐÂY ---
                    lineWidth: 2, 
                    marker: {
                        enabled: true, // Hiện điểm dữ liệu
                        radius: 2,     // Điểm to hơn
                        symbol: 'circle',
                        fillColor: '#ffffff', // Điểm màu trắng
                        lineWidth: 3,         // Viền điểm dày
                        lineColor: null       // Viền theo màu của line
                    },
                    states: {
                        hover: { lineWidth: 6 } // Hover vào dày hơn nữa
                    }
                }
            },
            series: [
                { 
                    name: 'Doanh thu', type: 'areaspline', data: data.revenue, yAxis: 0, 
                    color: { // Gradient màu xanh cho vùng area
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [[0, 'rgba(59, 130, 246, 0.5)'], [1, 'rgba(59, 130, 246, 0.05)']]
                    },
                    lineColor: '#2563eb', 
                    zIndex: 2
                },
                { 
                    name: 'Đơn hàng', type: 'spline', data: data.orders, yAxis: 1, 
                    color: '#f97316', // Màu cam đậm hơn
                    dashStyle: 'DashDot', // Kiểu nét đứt đẹp hơn ShortDot cũ
                    zIndex: 3
                }
            ]
        });
    },

    // ========================================================================
    // 3. PIE CHART (Donut - Trạng thái đơn hàng)
    // ========================================================================
    createDonut: function(id, data) {
        if (!data || data.length === 0) {
            console.warn("No data for Pie Chart:", id); return;
        }
        Highcharts.chart(id, {
            ...commonOptions,
            chart: { ...commonOptions.chart, type: 'pie' },
            // Bảng màu hiện đại cho các trạng thái
            colors: ['#2563eb', '#f97316', '#22c55e', '#ef4444', '#eab308', '#a855f7'],
            plotOptions: {
                pie: {
                    innerSize: '65%', // Donut mỏng hơn một chút cho sang
                    borderWidth: 3,
                    borderColor: '#ffffff', // Viền trắng ngăn cách các miếng
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        // --- BẬT DATA LABEL Ở ĐÂY ---
                        enabled: true,
                        // Format: Tên (Đậm) <xuống dòng> Giá trị (Nhạt)
                        format: '<b>{point.name}</b><br><span style="opacity:0.7">{point.percentage:.1f} %</span>',
                        distance: 20, // Khoảng cách từ biểu đồ đến nhãn
                        filter: {
                            property: 'percentage',
                            operator: '>',
                            value: 1 // Chỉ hiện nhãn cho các miếng > 1% để đỡ rối
                        },
                        style: {
                            fontSize: '12px',
                            fontWeight: 'normal',
                            color: '#334155',
                            textOutline: 'none' // Bỏ viền chữ mặc định
                        },
                        connectorShape: 'crookedLine', // Đường nối gấp khúc đẹp mắt
                        connectorColor: '#cbd5e1'
                    },
                    showInLegend: true // Vẫn hiện chú thích bên dưới
                }
            },
            tooltip: {
                ...commonOptions.tooltip,
                pointFormat: '{series.name}: <b>{point.y}</b> ({point.percentage:.1f}%)'
            },
            legend: {
                ...commonOptions.legend,
                layout: 'horizontal',
                align: 'center',
                verticalAlign: 'bottom',
                itemMarginTop: 10
            },
            series: [{
                name: 'Số lượng',
                colorByPoint: true,
                data: data
            }]
        });
    },


    createBrandDonut: function(id, data, totalText) {
        if (!data || data.length === 0) {
            console.warn("No data for Brand Donut:", id); return;
        }

        Highcharts.chart(id, {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart, 
                type: 'pie',
                backgroundColor: 'transparent' // Để không bị đè nền trắng
            },
            // Cấu hình Tiêu đề ở giữa (Hiển thị Tổng doanh thu)
            title: {
                text: totalText || '',
                align: 'center',
                verticalAlign: 'middle',
                y: 10, // Căn chỉnh vị trí dọc một chút cho cân
                style: { fontSize: '16px', fontWeight: 'bold', color: '#334155' }
            },
            plotOptions: {
                pie: {
                    innerSize: '60%',      // Tạo lỗ rỗng
                    borderWidth: 2,
                    borderColor: '#ffffff',
                    dataLabels: { enabled: false }, // Tắt nhãn chỉ đường (cho gọn)
                    showInLegend: false             // Tắt chú thích bên dưới (vì đã có bảng bên phải)
                }
            },
            tooltip: {
                ...commonOptions.tooltip,
                pointFormat: 'Doanh số: <b>{point.y:,.0f}</b> ({point.percentage:.1f}%)'
            },
            // Bảng màu riêng cho Brand (hơi trầm hơn để sang trọng)
            colors: ['#94a3b8', '#1e1b4b', '#4ade80', '#38bdf8', '#a78bfa', '#f472b6'],
            series: [{
                name: 'Doanh số',
                colorByPoint: true,
                data: data
            }]
        });
    }
};
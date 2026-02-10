function initBrandPlatformChart(chartData) {
    // 1. Định nghĩa Bảng màu cố định (Hardcode Colors)
    const platformColors = {
        'Shopee': '#ee4d2d',      // Cam Shopee
        'Tiktok Shop': '#000000', // Đen Tiktok
        'Lazada': '#0f156d',      // Xanh đậm Lazada
        'Haravan': '#2563eb',     // Xanh dương Haravan
        'Shopify': '#96bf48',     // Xanh lá Shopify
        'Tiki': '#1a94ff',        // Xanh Tiki
        'WooCommerce': '#96588a', // Tím Woo
        'Other': '#94a3b8'        // Xám mặc định
    };

    // 2. Map màu vào Series
    const coloredSeries = chartData.series.map(item => {
        return {
            name: item.name,
            data: item.data,
            // Nếu tên Platform có trong bảng màu thì lấy, không thì lấy màu xám
            color: platformColors[item.name] || platformColors['Other']
        };
    });

    // 3. Vẽ Chart
    Highcharts.chart('brandPlatformChart', {
        chart: {
            type: 'bar', // 'bar' là biểu đồ ngang, 'column' là dọc
            style: { fontFamily: 'Inter, sans-serif' }
        },
        title: { text: 'Doanh Số Theo Brand Và Nền Tảng', align: 'left' },
        xAxis: {
            categories: chartData.categories, // Danh sách Brand
            title: { text: null },
            gridLineWidth: 0
        },
        yAxis: {
            min: 0,
            title: { text: 'Doanh số (VNĐ)', align: 'high' },
            labels: {
                overflow: 'justify',
                formatter: function() {
                    // Format số tiền gọn (1M, 1B...)
                    return Highcharts.numberFormat(this.value, 0, '.', ','); 
                }
            },
            stackLabels: {
                enabled: true, // Hiện tổng số ở cuối thanh
                style: { fontWeight: 'bold', color: 'gray' }
            }
        },
        legend: {
            reversed: true, // Đảo ngược thứ tự chú thích để khớp với thanh stack
            verticalAlign: 'top'
        },
        plotOptions: {
            series: {
                stacking: 'normal', // Kích hoạt chế độ Stack (Chồng lên nhau)
                dataLabels: {
                    enabled: false // Tắt số trên từng đoạn màu cho đỡ rối
                }
            }
        },
        tooltip: {
            shared: true,
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y:,.0f} đ<br/>',
            footerFormat: 'Total: <b>{point.total:,.0f} đ</b>'
        },
        series: coloredSeries, // Dữ liệu đã gán màu
        credits: { enabled: false }
    });
}
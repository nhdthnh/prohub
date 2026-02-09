function initVietnamMap(dbData) {
    // 1. Bảng Mapping: Tên trong DB -> Mã Highcharts (vn-xxx)
    // (Phần này giữ nguyên như cũ, chỉ rút gọn để dễ nhìn)
    const provinceMapping = {
        "Hồ Chí Minh": "vn-hc", "TP. Hồ Chí Minh": "vn-hc", "Ho Chi Minh City": "vn-hc",
        "Hà Nội": "vn-hn", "TP. Hà Nội": "vn-hn", "Ha Noi": "vn-hn", "Hanoi": "vn-hn",
        "Đà Nẵng": "vn-da", "TP. Đà Nẵng": "vn-da",
        "Bình Dương": "vn-bi", "Đồng Nai": "vn-dn", "Hải Phòng": "vn-hp",
        "Nghệ An": "vn-na", "Thanh Hóa": "vn-th", "Bắc Ninh": "vn-bn",
        "Khánh Hòa": "vn-kh", "Lâm Đồng": "vn-ld", "Quảng Ninh": "vn-qn",
        "Bà Rịa - Vũng Tàu": "vn-bv", "Vũng Tàu": "vn-bv", "Nam Định": "vn-nd",
        "Hải Dương": "vn-hd", "Hưng Yên": "vn-hy", "Thái Bình": "vn-tb",
        "Tiền Giang": "vn-tg", "Cần Thơ": "vn-ct", "Đắk Lắk": "vn-dl",
        "Bình Định": "vn-bj", "Vĩnh Phúc": "vn-vp", "Long An": "vn-307",
        "Quảng Nam": "vn-qa", "Phú Thọ": "vn-pt", "Thái Nguyên": "vn-ty",
        "Bắc Giang": "vn-bg", "Bình Thuận": "vn-bt", "An Giang": "vn-ag",
        "Kiên Giang": "vn-kg", "Hà Nam": "vn-hm", "Tây Ninh": "vn-tn",
        "Bến Tre": "vn-br", "Quảng Ngãi": "vn-qg", "Đồng Tháp": "vn-dt",
        "Ninh Bình": "vn-nb", "Bình Phước": "vn-bp", "Hà Tĩnh": "vn-ht",
        "Cà Mau": "vn-cm", "Vĩnh Long": "vn-vl", "Trà Vinh": "vn-tv",
        "Sóc Trăng": "vn-st", "Bạc Liêu": "vn-bl", "Hậu Giang": "vn-hg",
        "Ninh Thuận": "vn-nt", "Phú Yên": "vn-py", "Gia Lai": "vn-gl",
        "Lào Cai": "vn-lc", "Lạng Sơn": "vn-ls", "Quảng Bình": "vn-qb",
        "Quảng Trị": "vn-qt", "Thừa Thiên Huế": "vn-tt", "Huế": "vn-tt",
        "Yên Bái": "vn-yb", "Sơn La": "vn-sl", "Hòa Bình": "vn-ho",
        "Tuyên Quang": "vn-tq", "Hà Giang": "vn-hg", "Cao Bằng": "vn-cb",
        "Lai Châu": "vn-lc", "Điện Biên": "vn-db", "Đắk Nông": "vn-da",
        "Kon Tum": "vn-kt"
    };

    // 2. Xử lý dữ liệu (CÓ THAY ĐỔI QUAN TRỌNG)
    let tempMapData = [];
    
    dbData.forEach(item => {
        let provinceName = item.ProvinceName;
        if (provinceName) {
            provinceName = provinceName.trim();
            let mapKey = provinceMapping[provinceName];
            
            if (mapKey) {
                // Thay vì đẩy mảng [key, value], ta đẩy Object để dễ config sau này
                tempMapData.push({
                    'hc-key': mapKey,
                    value: item.Orders,
                    name: provinceName // Lưu lại tên gốc để hiển thị tooltip nếu cần
                });
            }
        }
    });

    // --- LOGIC MỚI: Sắp xếp và chỉ hiện Label cho Top 10 ---

    // B1: Sắp xếp giảm dần theo số lượng đơn (value)
    // Để đảm bảo Top 10 người nhiều đơn nhất nằm đầu danh sách
    tempMapData.sort((a, b) => b.value - a.value);

    // B2: Duyệt qua danh sách, Top 10 bật label, còn lại tắt
    const finalMapData = tempMapData.map((item, index) => {
        if (index < 10) {
            // Nếu nằm trong Top 10 (index 0 đến 9)
            item.dataLabels = { 
                enabled: true,
                style: { 
                    fontWeight: 'bold', 
                    color: '#1e293b', // Màu chữ đậm
                    textOutline: '1px white' // Viền trắng để dễ đọc trên nền xanh
                },
                // Cho phép label đè lên nhau nếu cần thiết để luôn hiển thị
                allowOverlap: true 
            }; 
            // Mẹo: Đặt z-index cao để label của Top 10 nằm đè lên các vùng khác
            item.z = 1000 - index; 
        } else {
            // Các tỉnh còn lại -> Tắt tên
            item.dataLabels = { enabled: false };
        }
        return item;
    });

    // -------------------------------------------------------

    // 3. Vẽ Map
    Highcharts.mapChart('vietnamMap', {
        chart: {
            map: 'countries/vn/vn-all',
            style: { fontFamily: 'Inter, sans-serif' }
        },
        title: { text: '' },
        subtitle: { text: '' },
        mapNavigation: {
            enabled: true,
            buttonOptions: { verticalAlign: 'bottom' }
        },
        colorAxis: {
            min: 0,
            stops: [
                [0, '#e0f2fe'],   // Màu rất nhạt
                [0.5, '#3b82f6'], // Màu trung bình
                [1, '#1e3a8a']    // Màu đậm
            ]
        },
        series: [{
            data: finalMapData, // Sử dụng dữ liệu đã xử lý Top 10
            name: 'Số đơn hàng',
            states: {
                hover: { color: '#f59e0b' }
            },
            // Cấu hình dataLabels mặc định cho toàn bộ series (sẽ bị ghi đè bởi từng item)
            dataLabels: {
                enabled: true,
                format: '{point.name}',
                style: { fontWeight: 'normal', color: '#334155', textOutline: 'none' }
            },
            tooltip: {
                pointFormat: '{point.name}: <b>{point.value}</b> đơn',
                headerFormat: ''
            }
        }],
        credits: { enabled: false }
    });
}
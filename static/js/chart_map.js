function initVietnamMap(dbData) {
    // 1. Mapping (Giữ nguyên như cũ)
    const provinceMapping = {
        "hồ chí minh": "vn-hc", "tp. hồ chí minh": "vn-hc", "ho chi minh city": "vn-hc", "tphcm": "vn-hc",
        "hà nội": "vn-hn", "tp. hà nội": "vn-hn", "ha noi": "vn-hn", "hanoi": "vn-hn",
        "đà nẵng": "vn-da", "tp. đà nẵng": "vn-da",
        "bình dương": "vn-bi", "đồng nai": "vn-dn", "hải phòng": "vn-hp",
        "nghệ an": "vn-na", "thanh hóa": "vn-th", "bắc ninh": "vn-bn",
        "khánh hòa": "vn-kh", "lâm đồng": "vn-ld", "quảng ninh": "vn-qn",
        "bà rịa - vũng tàu": "vn-bv", "vũng tàu": "vn-bv", "nam định": "vn-nd",
        "hải dương": "vn-hd", "hưng yên": "vn-hy", "thái bình": "vn-tb",
        "tiền giang": "vn-tg", "cần thơ": "vn-ct", "đắk lắk": "vn-dl", "dak lak": "vn-dl",
        "bình định": "vn-bj", "vĩnh phúc": "vn-vp", "long an": "vn-307",
        "quảng nam": "vn-qa", "phú thọ": "vn-pt", "thái nguyên": "vn-ty",
        "bắc giang": "vn-bg", "bình thuận": "vn-bt", "an giang": "vn-ag",
        "kiên giang": "vn-kg", "hà nam": "vn-hm", "tây ninh": "vn-tn",
        "bến tre": "vn-br", "quảng ngãi": "vn-qg", "đồng tháp": "vn-dt",
        "ninh bình": "vn-nb", "bình phước": "vn-bp", "hà tĩnh": "vn-ht",
        "cà mau": "vn-cm", "vĩnh long": "vn-vl", "trà vinh": "vn-tv",
        "sóc trăng": "vn-st", "bạc liêu": "vn-bl", "hậu giang": "vn-hg",
        "ninh thuận": "vn-nt", "phú yên": "vn-py", "gia lai": "vn-gl",
        "lào cai": "vn-lc", "lạng sơn": "vn-ls", "quảng bình": "vn-qb",
        "quảng trị": "vn-qt", "thừa thiên huế": "vn-tt", "huế": "vn-tt",
        "yên bái": "vn-yb", "sơn la": "vn-sl", "hòa bình": "vn-ho",
        "tuyên quang": "vn-tq", "hà giang": "vn-hg", "cao bằng": "vn-cb",
        "lai châu": "vn-lc", "điện biên": "vn-db", "đắk nông": "vn-da", "dak nong": "vn-da",
        "kon tum": "vn-kt"
    };

    let tempMapData = [];
    let maxValue = 0;

    // 2. Xử lý dữ liệu
    dbData.forEach(item => {
        let rawName = item.Province || item.ProvinceName; 
        if (rawName) {
            let normalizedName = rawName.toString().trim().toLowerCase();
            let mapKey = provinceMapping[normalizedName];
            
            if (mapKey) {
                let val = parseInt(item.Orders);
                if (val > maxValue) maxValue = val;

                tempMapData.push({
                    'hc-key': mapKey,
                    value: val,
                    name: rawName
                });
            }
        }
    });

    // Sort giảm dần
    tempMapData.sort((a, b) => b.value - a.value);

    // Cấu hình Label (chỉ hiện Top 10)
    const finalMapData = tempMapData.map((item, index) => {
        if (index < 10) {
             item.dataLabels = { 
                 enabled: true,
                 format: '{point.name}<br/><span style="font-size:11px; font-weight:bold">{point.value}</span>', 
                 style: { fontWeight: 'normal', color: 'black', textOutline: '1px white', textAlign: 'center' },
                 allowOverlap: true,
                 y: -5
             };
             item.z = 1000 - index;
        } else {
             item.dataLabels = { enabled: false };
        }
        return item;
    });

    // 3. Render Map
    Highcharts.mapChart('vietnamMap', {
        chart: {
            map: 'countries/vn/vn-all',
            style: { fontFamily: 'Inter, sans-serif' },
            
            // --- CẤU HÌNH AUTO ZOOM ---
            events: {
                load: function () {
                    // Tìm điểm có giá trị lớn nhất (đã sort ở trên nên là phần tử đầu tiên của finalMapData)
                    // Tuy nhiên cần tìm object Point thực tế của Highcharts để gọi hàm zoomTo
                    const series = this.series[0];
                    if (series.points.length > 0) {
                        // Tìm point có value = maxValue
                        let maxPoint = null;
                        for (let i = 0; i < series.points.length; i++) {
                             if (series.points[i].value === maxValue) {
                                 maxPoint = series.points[i];
                                 break;
                             }
                        }

                        // Thực hiện Zoom nếu tìm thấy
                        if (maxPoint) {
                            maxPoint.zoomTo(); 
                        }
                    }
                }
            }
            // --------------------------
        },

        // --- XÓA CHART TITLE ---
        title: { text: '' }, 
        // -----------------------

        // Bật điều hướng để user có thể Zoom Out lại
        mapNavigation: {
            enabled: true,
            enableMouseWheelZoom: true, // Cho phép lăn chuột để zoom
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },

        colorAxis: {
            min: 1,
            max: maxValue,
            type: 'logarithmic',
            stops: [
                [0, '#fff7bc'], 
                [0.3, '#fec44f'], 
                [0.6, '#d95f0e'], 
                [1, '#993404']
            ]
        },

        series: [{
            data: finalMapData,
            name: 'Số đơn hàng',
            joinBy: 'hc-key',
            borderColor: '#A0A0A0',
            borderWidth: 0.5,
            states: {
                hover: { color: '#2563eb' }
            },
            tooltip: {
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                headerFormat: '<span style="font-size: 13px; font-weight: bold">{point.key}</span><br/>',
                pointFormat: '📦 <b>{point.value}</b> đơn hàng'
            }
        }],
        credits: { enabled: false }
    });
}
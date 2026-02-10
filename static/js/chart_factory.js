// static/js/chart_factory.js

window.ChartFactory = {
    // ========================================================================
    // 1. BAR CHART (Stacked - Doanh số theo Brand/Platform)
    // ========================================================================
    createStackedBar: function (id, data) {
        if (!data || !data.series || data.series.length === 0) {
            console.warn("No data for Bar Chart:", id); return;
        }

        const platformColors = {
            'Shopee': '#ee4d2d', 'Tiktok Shop': '#000000',
            'Lazada': '#0f156d', 'Haravan': '#2563eb',
            'Shopify': '#96bf48', 'Tiki': '#1a94ff'
        };

        const coloredSeries = data.series.map(s => ({
            ...s,
            color: platformColors[s.name] || '#94a3b8',
            borderWidth: 0
        }));

        ChartBuilder.stackedBar(id, data.categories, coloredSeries, {
            yAxis: {
                title: { text: null },
                stackLabels: {
                    formatter: function () {
                        if (this.total >= 1000000000) return (this.total / 1000000000).toFixed(1) + 'B';
                        if (this.total >= 1000000) return (this.total / 1000000).toFixed(1) + 'M';
                        if (this.total >= 1000) return (this.total / 1000).toFixed(0) + 'K';
                        return this.total;
                    }
                }
            },
            tooltip: {
                pointFormat: '<span style="color:{series.color}">●</span> {series.name}: <b>{point.y:,.0f} đ</b><br/>',
                footerFormat: 'Tổng: <b>{point.total:,.0f} đ</b>'
            }
        });
    },

    // ========================================================================
    // 2. LINE CHART (Dual Axis - Doanh thu & Đơn hàng theo giờ)
    // ========================================================================
    createDualLine: function (id, data) {
        if (!data || !data.hours || data.hours.length === 0) {
            console.warn("No data for Line Chart:", id); return;
        }

        const seriesData = [
            {
                name: 'Doanh thu', type: 'areaspline', data: data.revenue, yAxis: 0,
                color: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [[0, 'rgba(59, 130, 246, 0.5)'], [1, 'rgba(59, 130, 246, 0.05)']]
                },
                lineColor: '#2563eb',
                zIndex: 2,
                marker: { enabled: true, radius: 2, fillColor: '#ffffff', lineWidth: 2, lineColor: null }
            },
            {
                name: 'Đơn hàng', type: 'spline', data: data.orders, yAxis: 1,
                color: '#f97316',
                dashStyle: 'DashDot',
                zIndex: 3,
                marker: { enabled: true, radius: 2, fillColor: '#ffffff', lineWidth: 2, lineColor: null }
            }
        ];

        ChartBuilder.dualAxis(id, data.hours, seriesData, {
            yAxis: [
                { // Override for specific formatter
                    labels: {
                        style: { color: '#2563eb' },
                        formatter: function () { return this.value >= 1000000 ? (this.value / 1000000).toFixed(1) + 'M' : Highcharts.numberFormat(this.value, 0); }
                    }
                },
                { // Right Axis
                    labels: { style: { color: '#f97316' } },
                    opposite: true
                }
            ],
            exporting: {
                buttons: { contextButton: { verticalAlign: 'top', y: -10 } }
            }
        });
    },

    // ========================================================================
    // 3. PIE CHART (Donut - Trạng thái đơn hàng)
    // ========================================================================
    createDonut: function (id, data) {
        if (!data || data.length === 0) {
            console.warn("No data for Pie Chart:", id); return;
        }

        ChartBuilder.donut(id, data, {
            colors: ['#2563eb', '#f97316', '#22c55e', '#ef4444', '#eab308', '#a855f7'],
            plotOptions: {
                pie: {
                    dataLabels: {
                        filter: { property: 'percentage', operator: '>', value: 1 },
                        connectorShape: 'crookedLine',
                        connectorColor: '#cbd5e1'
                    },
                    innerSize: '65%'
                }
            },
            legend: {
                layout: 'horizontal',
                align: 'center',
                verticalAlign: 'bottom',
                itemMarginTop: 10
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.y}</b> ({point.percentage:.1f}%)'
            }
        });
    },

    // ========================================================================
    // 4. PERF CHART (Donut - Brand Performance)
    // ========================================================================
    createPerfDonut: function (id, data, centerText) {
        if (!data || data.length === 0) return;

        ChartBuilder.donut(id, data, {
            chart: { height: 350 },
            title: {
                text: centerText || '',
                align: 'center',
                verticalAlign: 'middle',
                y: 10,
                style: { fontSize: '18px', fontWeight: 'bold', color: '#334155' }
            },
            plotOptions: {
                pie: {
                    innerSize: '65%',
                    dataLabels: { enabled: false }, // Hide labels
                    showInLegend: false             // Hide legend
                }
            },
            colors: ['#94a3b8', '#1e1b4b', '#0ea5e9', '#22c55e', '#eab308', '#f472b6', '#64748b'],
            tooltip: {
                pointFormat: '<b>{point.name}</b>: {point.y:,.0f} ({point.percentage:.1f}%)'
            }
        });
    },

    // Alias for backward compatibility if needed
    createBrandDonut: function (id, data, centerText) {
        this.createPerfDonut(id, data, centerText);
    }
};

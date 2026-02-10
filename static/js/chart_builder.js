/**
 * ChartBuilder - A generic wrapper for Highcharts to ensure consistent styling and easy reuse.
 */
const ChartBuilder = (function () {

    // --- DEFAULT CONFIGURATION (Apply to all charts) ---
    const defaultOptions = {
        chart: {
            style: { fontFamily: 'Inter, sans-serif' },
            backgroundColor: 'transparent',
            spacingTop: 20
        },
        credits: { enabled: false },
        title: { text: null },
        tooltip: {
            backgroundColor: 'rgba(30, 41, 59, 0.95)',
            style: { color: '#f8fafc', fontSize: '13px' },
            borderRadius: 8,
            borderWidth: 0,
            shadow: false,
            useHTML: true,
            headerFormat: '<span style="font-size: 12px; color: #94a3b8; font-weight: 500">{point.key}</span><br/>'
        },
        xAxis: {
            lineColor: '#cbd5e1',
            tickColor: '#cbd5e1',
            labels: { style: { color: '#64748b', fontSize: '11px' } },
            gridLineColor: '#f1f5f9'
        },
        yAxis: {
            gridLineColor: '#f1f5f9',
            labels: { style: { color: '#64748b', fontSize: '11px' } },
            title: { text: null }
        },
        legend: {
            itemStyle: { color: '#475569', fontWeight: '500', fontSize: '12px' },
            itemHoverStyle: { color: '#1e293b' }
        },
        plotOptions: {
            series: {
                animation: { duration: 1000 }
            }
        }
    };

    /**
     * Merge default options with user provided options
     */
    function mergeOptions(defaults, user) {
        // Simple deep merge or use Highcharts.merge if available
        if (typeof Highcharts !== 'undefined' && Highcharts.merge) {
            return Highcharts.merge(defaults, user);
        }
        return { ...defaults, ...user };
    }

    return {
        /**
         * Generic Chart Creator
         */
        create: function (id, options) {
            if (!document.getElementById(id)) {
                console.warn(`ChartBuilder: Container #${id} not found.`);
                return;
            }
            const finalOptions = mergeOptions(defaultOptions, options);
            return Highcharts.chart(id, finalOptions);
        },

        /**
         * Helper for Donut Charts
         */
        donut: function (id, seriesData, options = {}) {
            const defaults = {
                chart: { type: 'pie' },
                plotOptions: {
                    pie: {
                        innerSize: '65%',
                        borderWidth: 3,
                        borderColor: '#ffffff',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b><br><span style="opacity:0.7">{point.percentage:.1f} %</span>',
                            distance: 20,
                            style: { fontWeight: 'normal', color: '#334155', textOutline: 'none' }
                        },
                        showInLegend: true
                    }
                },
                series: [{
                    name: 'Data',
                    colorByPoint: true,
                    data: seriesData
                }]
            };
            return this.create(id, mergeOptions(defaults, options));
        },

        /**
         * Helper for Stacked Bar Charts
         */
        stackedBar: function (id, categories, seriesData, options = {}) {
            const defaults = {
                chart: { type: 'bar' },
                xAxis: { categories: categories },
                yAxis: {
                    stackLabels: {
                        enabled: true,
                        style: { fontWeight: 'bold', color: '#64748b' }
                    }
                },
                plotOptions: {
                    series: {
                        stacking: 'normal',
                        borderRadius: 3
                    }
                },
                series: seriesData
            };
            return this.create(id, mergeOptions(defaults, options));
        },

        /**
         * Helper for Dual Axis Line Charts
         */
        dualAxis: function (id, categories, seriesData, options = {}) {
            const defaults = {
                chart: { zoomType: 'xy', marginTop: 30 },
                xAxis: { categories: categories, crosshair: true },
                yAxis: [
                    { // Primary yAxis (Left)
                        labels: { style: { color: (seriesData[0] && seriesData[0].color) || '#2563eb' } },
                        title: { text: null }
                    },
                    { // Secondary yAxis (Right)
                        title: { text: null },
                        labels: { style: { color: (seriesData[1] && seriesData[1].color) || '#f97316' } },
                        opposite: true
                    }
                ],
                tooltip: { shared: true },
                series: seriesData
            };
            // Ensure second series is on sec axis if not specified
            if (seriesData[1] && seriesData[1].yAxis === undefined) {
                seriesData[1].yAxis = 1;
            }

            return this.create(id, mergeOptions(defaults, options));
        },
        /**
         * Helper for Map Charts
         */
        map: function (id, options) {
            // Check if map module is loaded
            if (!Highcharts.mapChart) {
                console.warn('Highcharts Map module not loaded');
                return;
            }
            if (!document.getElementById(id)) {
                console.warn(`ChartBuilder: Container #${id} not found.`);
                return;
            }
            const finalOptions = mergeOptions(defaultOptions, options);
            return Highcharts.mapChart(id, finalOptions);
        }
    };
})();

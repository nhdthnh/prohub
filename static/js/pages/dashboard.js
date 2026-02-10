/**
 * static/js/pages/dashboard.js
 * Logic khởi tạo biểu đồ cho trang Dashboard B2C Overview
 */

document.addEventListener("DOMContentLoaded", function () {
    // Lấy data từ biến toàn cục window.dashboardData (được inject từ template)
    const data = window.dashboardData || {};

    // --- 1. PREPARE DATA ---
    const hourlyData = {
        hours: data.chartLabels || [],
        revenue: data.chartRevenue || [],
        orders: data.chartOrders || []
    };

    const pieData = (data.rawStatus || []).map(item => ({
        name: item.StatusName || 'Unknown',
        y: item.Orders
    }));

    const mapData = data.rawProvince || [];
    const barData = data.rawBrandPlatform || null;
    const brandPieData = data.brandPieData || [];
    const totalRevenueStr = data.brandTotalRevenue || '0';

    // --- 2. RENDER CHARTS ---

    // Hourly Trend Chart (Dual Axis)
    if (hourlyData.hours && hourlyData.hours.length > 0) {
        ChartFactory.createDualLine('hourlyTrendChart', hourlyData);
    }

    // Status Donut Chart
    if (pieData && pieData.length > 0) {
        ChartFactory.createDonut('statusPieChart', pieData);
    }

    // Vietnam Map
    if (mapData && typeof ChartBuilder.map === 'function') {
        // Sử dụng logic map trong chart_map.js (đã refactor dùng ChartBuilder)
        // Lưu ý: initVietnamMap là hàm toàn cục từ chart_map.js
        if (typeof initVietnamMap === 'function') {
            initVietnamMap(mapData);
        } else {
            console.warn('initVietnamMap function not found');
        }
    }

    // Stacked Bar Chart (Brand x Platform)
    if (barData) {
        ChartFactory.createStackedBar('brandPlatformChart', barData);
    }

    // Brand Performance Donut
    if (brandPieData && brandPieData.length > 0) {
        ChartFactory.createPerfDonut('brandPerformancePie', brandPieData, totalRevenueStr);
    }
});

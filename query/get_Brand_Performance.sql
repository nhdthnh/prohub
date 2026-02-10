SELECT 
    T.brand,
    
    /* 1. Hiển thị lại số liệu thô */
    T.CurrRevenue AS Revenue,
    T.CurrOrders AS Orders,
    T.PrevRevenue AS PreviousRevenue,
    T.PrevOrders AS PreviousOrders,

    /* 2. Tính % Tăng trưởng Doanh thu (Revenue Growth) */
    CASE 
        /* Nếu kỳ trước = 0 mà kỳ này > 0 -> Tăng trưởng 100% */
        WHEN T.PrevRevenue = 0 AND T.CurrRevenue > 0 THEN 100
        /* Nếu kỳ trước = 0 và kỳ này cũng = 0 -> Tăng trưởng 0% */
        WHEN T.PrevRevenue = 0 THEN 0
        /* Công thức: ((Kỳ này - Kỳ trước) / Kỳ trước) * 100 */
        ELSE ((T.CurrRevenue - T.PrevRevenue) / T.PrevRevenue) * 100
    END AS RevenueGrowth,

    /* 3. Tính % Tăng trưởng Số đơn (Orders Growth) */
    CASE 
        WHEN T.PrevOrders = 0 AND T.CurrOrders > 0 THEN 100
        WHEN T.PrevOrders = 0 THEN 0
        ELSE ((T.CurrOrders - T.PrevOrders) / T.PrevOrders) * 100
    END AS OrdersGrowth

FROM (
    /* --- BẢNG TẠM: TÍNH TOÁN SỐ LIỆU THÔ --- */
    SELECT 
        brand,
        
        /* Kỳ Hiện Tại */
        SUM(CASE WHEN CreatedTime BETWEEN %s AND %s THEN Revenue ELSE 0 END) as CurrRevenue,
        COUNT(DISTINCT CASE WHEN CreatedTime BETWEEN %s AND %s THEN OmisellOrderNumber END) as CurrOrders,

        /* Kỳ Trước */
        SUM(CASE WHEN CreatedTime BETWEEN %s AND %s THEN Revenue ELSE 0 END) as PrevRevenue,
        COUNT(DISTINCT CASE WHEN CreatedTime BETWEEN %s AND %s THEN OmisellOrderNumber END) as PrevOrders

    FROM 
        omisell_catalogue
    WHERE 
        brand IS NOT NULL 
        AND brand <> ''
        AND CreatedTime BETWEEN %s AND %s /* Range tổng: StartPrev -> EndCurr */
        {filters}
    GROUP BY 
        brand
) AS T

ORDER BY 
    T.CurrRevenue DESC;
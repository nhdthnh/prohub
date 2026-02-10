SELECT 
    /* --- 1. SỐ LIỆU HIỆN TẠI --- */
    T.CurrRevenue AS Revenue,
    T.CurrOrders AS Orders,
    /* Quantity đã lấy ở query khác nên để null hoặc 0 ở đây cũng được, 
       Python sẽ merge đè lên sau. */
    0 AS Quantity, 
    
    CASE WHEN T.CurrOrders = 0 THEN 0 ELSE T.CurrRevenue / T.CurrOrders END AS AOV,

    /* --- 2. TÍNH % TĂNG TRƯỞNG (GROWTH) --- */
    
    /* Revenue Growth */
    CASE 
        WHEN T.PrevRevenue = 0 AND T.CurrRevenue > 0 THEN 100
        WHEN T.PrevRevenue = 0 THEN 0
        ELSE ((T.CurrRevenue - T.PrevRevenue) / T.PrevRevenue) * 100
    END AS RevenueGrowth,

    /* Orders Growth */
    CASE 
        WHEN T.PrevOrders = 0 AND T.CurrOrders > 0 THEN 100
        WHEN T.PrevOrders = 0 THEN 0
        ELSE ((T.CurrOrders - T.PrevOrders) / T.PrevOrders) * 100
    END AS OrdersGrowth,
    
    /* Quantity Growth (Python sẽ tự xử lý, ở đây trả về 0) */
    0 AS QuantityGrowth,

    /* AOV Growth */
    CASE 
        WHEN (CASE WHEN T.PrevOrders = 0 THEN 0 ELSE T.PrevRevenue / T.PrevOrders END) = 0 THEN 0
        ELSE (
            (CASE WHEN T.CurrOrders = 0 THEN 0 ELSE T.CurrRevenue / T.CurrOrders END) - 
            (CASE WHEN T.PrevOrders = 0 THEN 0 ELSE T.PrevRevenue / T.PrevOrders END)
        ) / (CASE WHEN T.PrevOrders = 0 THEN 0 ELSE T.PrevRevenue / T.PrevOrders END) * 100
    END AS AovGrowth

FROM (
    SELECT 
        /* === KỲ HIỆN TẠI === */
        /* Param 1, 2: Doanh thu hiện tại */
        SUM(CASE WHEN CreatedTime BETWEEN %s AND %s THEN (OriginalPrice - DiscountSeller - VoucherSeller) * Quantity ELSE 0 END) AS CurrRevenue,
        
        /* Param 3, 4: Số đơn hiện tại */
        COUNT(DISTINCT CASE WHEN CreatedTime BETWEEN %s AND %s THEN OmisellOrderNumber END) AS CurrOrders,
        
        /* === KỲ TRƯỚC === */
        /* Param 5, 6: Doanh thu kỳ trước */
        SUM(CASE WHEN CreatedTime BETWEEN %s AND %s THEN (OriginalPrice - DiscountSeller - VoucherSeller) * Quantity ELSE 0 END) AS PrevRevenue,
        
        /* Param 7, 8: Số đơn kỳ trước */
        COUNT(DISTINCT CASE WHEN CreatedTime BETWEEN %s AND %s THEN OmisellOrderNumber END) AS PrevOrders

    FROM
        omisell_catalogue
        
    WHERE 
        /* Param 9, 10: Range tổng cho WHERE */
        CreatedTime BETWEEN %s AND %s
        {filters}
) AS T;
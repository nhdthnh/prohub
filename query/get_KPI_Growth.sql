SELECT 
    /* --- 1. SỐ LIỆU HIỆN TẠI (Hiển thị to) --- */
    T.CurrRevenue AS Revenue,
    T.CurrOrders AS Orders,
    T.CurrQty AS Quantity,
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
    
    /* Quantity Growth */
    CASE 
        WHEN T.PrevQty = 0 AND T.CurrQty > 0 THEN 100
        WHEN T.PrevQty = 0 THEN 0
        ELSE ((T.CurrQty - T.PrevQty) / T.PrevQty) * 100
    END AS QuantityGrowth,

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
        /* === KỲ HIỆN TẠI (3 dòng đầu) === */
        SUM(CASE WHEN o.CreatedTime BETWEEN %s AND %s THEN (c.OriginalPrice - c.DiscountSeller - c.VoucherSeller) * c.Quantity ELSE 0 END) AS CurrRevenue,
        COUNT(DISTINCT CASE WHEN o.CreatedTime BETWEEN %s AND %s THEN o.OmisellOrderNumber END) AS CurrOrders,
        SUM(CASE WHEN o.CreatedTime BETWEEN %s AND %s THEN c.Quantity ELSE 0 END) AS CurrQty,

        /* === KỲ TRƯỚC (3 dòng sau) === */
        SUM(CASE WHEN o.CreatedTime BETWEEN %s AND %s THEN (c.OriginalPrice - c.DiscountSeller - c.VoucherSeller) * c.Quantity ELSE 0 END) AS PrevRevenue,
        COUNT(DISTINCT CASE WHEN o.CreatedTime BETWEEN %s AND %s THEN o.OmisellOrderNumber END) AS PrevOrders,
        SUM(CASE WHEN o.CreatedTime BETWEEN %s AND %s THEN c.Quantity ELSE 0 END) AS PrevQty

    FROM
        orders o 
        LEFT JOIN catalogueitems c ON c.OmisellOrderNumber = o.OmisellOrderNumber 
        /* Join thêm các bảng khác nếu cần lọc filter brand/shop... */
    WHERE 
        o.CreatedTime BETWEEN %s AND %s
) AS T;
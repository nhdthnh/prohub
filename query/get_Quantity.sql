SELECT T.CurrQty AS Quantity, T.PrevQty AS PreviousQuantity,

/* Tinh Tang truong ngay trong SQL */


CASE 
        WHEN T.PrevQty = 0 AND T.CurrQty > 0 THEN 100
        WHEN T.PrevQty = 0 THEN 0
        ELSE ((T.CurrQty - T.PrevQty) / T.PrevQty) * 100
    END AS QuantityGrowth

FROM (
    SELECT 
        /* Tính Tổng Kỳ Hiện Tại */
        SUM(CASE WHEN CreatedTime BETWEEN %s AND %s THEN Quantity ELSE 0 END) AS CurrQty,

/* Tính Tổng Kỳ Trước */


SUM(CASE WHEN CreatedTime BETWEEN %s AND %s THEN Quantity ELSE 0 END) AS PrevQty

    FROM 
        omisell_inventory
    WHERE 
        /* Lọc khoảng thời gian bao trùm cả 2 kỳ (để tối ưu Index) */
        CreatedTime BETWEEN %s AND %s
        {filters}
) AS T;
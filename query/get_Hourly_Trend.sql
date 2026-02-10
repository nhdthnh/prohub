SELECT 
    HOUR(CreatedTime) as HOURNUM,
    COUNT(DISTINCT OmisellOrderNumber) as Orders,
    /* Tính doanh thu trực tiếp từ các cột có trong View */
    SUM((OriginalPrice - DiscountSeller - VoucherSeller) * Quantity) as Revenue
FROM 
    omisell_catalogue
    
WHERE 
    CreatedTime BETWEEN %s AND %s
    {filters}  /* Python sẽ điền: AND ShopName IN (...) */

GROUP BY 
    HOUR(CreatedTime)
ORDER BY 
    HOURNUM ASC;
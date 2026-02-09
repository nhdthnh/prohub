/* query/get_Revenue.sql */
SELECT 
    COUNT(DISTINCT o.OmisellOrderNumber) AS Orders,
    SUM((c.OriginalPrice - c.DiscountSeller - c.VoucherSeller) * c.Quantity) AS Revenue,
    SUM((c.OriginalPrice - c.DiscountSeller - c.VoucherSeller) * c.Quantity)/COUNT(DISTINCT o.OmisellOrderNumber) as AOV
FROM
    orders o 
    LEFT JOIN catalogueitems c ON c.OmisellOrderNumber = o.OmisellOrderNumber 
    LEFT JOIN status st ON st.StatusID = o.StatusId
    LEFT JOIN platforms p2 ON p2.Platform = o.Platform
    LEFT JOIN shops s2 ON s2.ShopId = o.ShopId
WHERE 
    o.CreatedTime BETWEEN %s AND %s;


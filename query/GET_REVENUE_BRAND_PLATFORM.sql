-- GET Revenue by Brand and Platform
SELECT 
    b.brand,
    p.PlatformName,
    SUM(o.Revenue) as Revenue,
    COUNT(DISTINCT o.OmisellOrderNumber) as Orders
FROM omisell_db.omisell_order o
LEFT JOIN omisell_db.omisell_brand b ON o.BrandID = b.BrandID
LEFT JOIN omisell_db.omisell_platform p ON o.PlatformID = p.PlatformID
WHERE o.CreatedTime BETWEEN %s AND %s
GROUP BY b.brand, p.PlatformName
ORDER BY Revenue DESC

-- GET Revenue proportion by Platform
SELECT 
    p.PlatformName as PlatformName,
    SUM(o.Revenue) as Revenue,
    COUNT(DISTINCT o.OmisellOrderNumber) as Orders,
    ROUND((SUM(o.Revenue) / (SELECT SUM(Revenue) FROM omisell_db.omisell_order WHERE CreatedTime BETWEEN %s AND %s)) * 100, 1) as RevenuePercent
FROM omisell_db.omisell_order o
LEFT JOIN omisell_db.omisell_platform p ON o.PlatformID = p.PlatformID
WHERE o.CreatedTime BETWEEN %s AND %s
GROUP BY p.PlatformName
ORDER BY Revenue DESC

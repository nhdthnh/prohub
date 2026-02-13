-- GET Revenue proportion by Brand
SELECT 
    b.brand as Brand,
    SUM(o.Revenue) as Revenue,
    COUNT(DISTINCT o.OmisellOrderNumber) as Orders,
    ROUND((SUM(o.Revenue) / (SELECT SUM(Revenue) FROM omisell_db.omisell_order WHERE CreatedTime BETWEEN %s AND %s)) * 100, 1) as RevenuePercent
FROM omisell_db.omisell_order o
LEFT JOIN omisell_db.omisell_brand b ON o.BrandID = b.BrandID
WHERE o.CreatedTime BETWEEN %s AND %s
GROUP BY b.brand
ORDER BY Revenue DESC

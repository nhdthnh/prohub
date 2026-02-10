SELECT DISTINCT sh.ShopName, sh.ShopId
FROM shops sh
JOIN orders o ON o.ShopId = sh.ShopId
WHERE o.CreatedTime BETWEEN %s AND %s
ORDER BY sh.ShopName ASC;
SELECT DISTINCT
    sh.ShopName,
    sh.ShopId
FROM omisell_catalogue sh
WHERE
    sh.CreatedTime BETWEEN %s AND %s
ORDER BY sh.ShopName ASC;
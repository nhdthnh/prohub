SELECT 
    Province,
    COUNT(DISTINCT OmisellOrderNumber) as Orders
FROM 
    omisell_catalogue
WHERE 
    CreatedTime BETWEEN %s AND %s
    AND Province IS NOT NULL 
    AND Province <> ''
    {filters}
GROUP BY 
    Province
ORDER BY 
    Orders DESC;
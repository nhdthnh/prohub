SELECT 
    StatusName,
    COUNT(DISTINCT OmisellOrderNumber) as Orders
FROM 
    omisell_catalogue
WHERE 
    CreatedTime BETWEEN %s AND %s
    {filters}
GROUP BY 
    StatusName
ORDER BY 
    Orders DESC;
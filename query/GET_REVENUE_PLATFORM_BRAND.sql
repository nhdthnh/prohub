SELECT 
    brand, 
    PlatformName, 
    SUM(Revenue) as TotalRevenue
FROM 
    omisell_catalogue
WHERE 
    brand IS NOT NULL 
    AND brand <> ''
    AND CreatedTime BETWEEN %s AND %s
    {filters}
GROUP BY 
    brand, 
    PlatformName
ORDER BY 
    TotalRevenue DESC;
/* Sắp xếp để Brand doanh số cao nhất hiện lên đầu */
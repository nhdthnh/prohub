SELECT 
	r.Province AS ProvinceName,
    COUNT(DISTINCT o.OmisellOrderNumber) AS Orders
FROM
    orders o 
    LEFT JOIN catalogueitems c ON c.OmisellOrderNumber = o.OmisellOrderNumber 
    LEFT JOIN status st ON st.StatusID = o.StatusId
    LEFT JOIN platforms p2 ON p2.Platform = o.Platform
    LEFT JOIN shops s2 ON s2.ShopId = o.ShopId
    LEFT JOIN receiver r ON r.OmisellOrderNumber = o.OmisellOrderNumber 
WHERE 
    o.CreatedTime BETWEEN %s AND %s 
    AND r.Province IS NOT NULL 
    AND r.Province <> ''
GROUP BY 
    r.Province 
ORDER BY 
    Orders DESC;
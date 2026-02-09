SELECT 
	st.StatusName,
    COUNT(DISTINCT o.OmisellOrderNumber) AS Orders
FROM
    orders o 
    LEFT JOIN catalogueitems c ON c.OmisellOrderNumber = o.OmisellOrderNumber 
    LEFT JOIN status st ON st.StatusID = o.StatusId
    LEFT JOIN platforms p2 ON p2.Platform = o.Platform
    LEFT JOIN shops s2 ON s2.ShopId = o.ShopId
WHERE 
    o.CreatedTime BETWEEN %s AND %s
GROUP BY 
    st.StatusName
ORDER BY 
    Orders DESC;
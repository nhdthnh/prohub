/* query/get_Revenue.sql */
SELECT 
    SUM(i.`quantity`) as `Quantity`
FROM
    inventoryitems i 
    LEFT JOIN orders o ON i.OmisellOrderNumber = o.OmisellOrderNumber
    LEFT JOIN product p ON p.sku = i.CatalogueSKU
    LEFT JOIN status st ON st.StatusID = o.StatusId
    LEFT JOIN platforms p2 ON p2.Platform = o.Platform
    LEFT JOIN shops s2 ON s2.ShopId = o.ShopId
WHERE 
    o.CreatedTime BETWEEN %s AND %s
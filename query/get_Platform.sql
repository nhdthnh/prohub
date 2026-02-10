SELECT DISTINCT pl.PlatformName, pl.Platform
FROM platforms pl
JOIN orders o ON o.Platform = pl.Platform
WHERE o.CreatedTime BETWEEN %s AND %s
ORDER BY pl.PlatformName ASC;
SELECT DISTINCT
    `PlatformName`
from omisell_catalogue
WHERE
    CreatedTime BETWEEN % s AND %  s
ORDER BY PlatformName ASC;
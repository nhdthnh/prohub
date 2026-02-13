SELECT DISTINCT
    brand
FROM omisell_catalogue
WHERE
    brand IS NOT NULL
    AND brand <> ''
    AND CreatedTime BETWEEN %s AND %s
ORDER BY brand ASC;
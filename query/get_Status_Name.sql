SELECT DISTINCT st.StatusName, st.StatusID
FROM status st
JOIN orders o ON o.StatusId = st.StatusID
WHERE o.CreatedTime BETWEEN %s AND %s
ORDER BY st.StatusName ASC;
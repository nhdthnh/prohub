SELECT DISTINCT
    st.StatusName,
    st.StatusID
from omisell_catalogue st
WHERE
    st.CreatedTime BETWEEN %s AND %s
ORDER BY st.StatusName ASC;
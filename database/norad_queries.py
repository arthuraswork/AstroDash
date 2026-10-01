current_cte = """--sql
WITH current_date AS (
    SELECT MAX(updated_at) FROM starlink_moscow
);
"""

select_current_sputnics_lat_lon = """--sql
SELECT lat, lon FROM starlink_moscow WHERE updated_at = (SELECT MAX(updated_at) FROM starlink_moscow);
""" 

select_current_count = """--sql
SELECT COUNT(*) FROM starlink_moscow
WHERE updated_at = (SELECT MAX(updated_at) FROM starlink_moscow);
"""

select_total_count = """--sql
SELECT COUNT(*) FROM starlink_moscow;
"""

select_max_alt = """--sql
SELECT MAX(alt) FROM starlink_moscow;
"""


select_min_alt = """--sql
SELECT MIN(alt) FROM starlink_moscow;
"""
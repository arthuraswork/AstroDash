select_all_near_earth_objects = """--sql
SELECT 
    nasa_id,
    name,
    absolute_magnitude,
    miss_distance_km,
    relative_velocity_kmh,
    diameter_min_m,
    diameter_max_m
FROM near_earth_objects
"""

select_count_near_earth_objects = """--sql
SELECT COUNT(*) FROM near_earth_objects
"""

select_speed_near_earth_objects = """--sql
SELECT AVG(relative_velocity_kmh) FROM near_earth_objects
"""

select_dist_near_earth_objects = """--sql
SELECT AVG(miss_distance_km) FROM near_earth_objects
"""


top_near_earth_objects = """--sql
SELECT name, miss_distance_km FROM near_earth_objects ORDER BY miss_distance_km DESC
"""

top_fast_earth_objects = """--sql
SELECT name, relative_velocity_kmh FROM near_earth_objects ORDER BY relative_velocity_kmh DESC
"""

top_big_earth_objects = """--sql
SELECT name, diameter_max_m FROM near_earth_objects ORDER BY diameter_max_m DESC
"""
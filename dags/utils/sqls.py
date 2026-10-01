
create_table_near_earth_objects = """--sql
CREATE TABLE IF NOT EXISTS  near_earth_objects (
    nasa_id BIGINT PRIMARY KEY,
    name                  VARCHAR(128) NOT NULL,
    absolute_magnitude    DOUBLE PRECISION NOT NULL,
    miss_distance_km      DOUBLE PRECISION NOT NULL,
    relative_velocity_kmh DOUBLE PRECISION NOT NULL,
    diameter_min_m        DOUBLE PRECISION NOT NULL,
    diameter_max_m        DOUBLE PRECISION NOT NULL,
    created_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT chk_diameter_order CHECK (diameter_max_m >= diameter_min_m)
);
"""

insert_one_near_earth_objects = """--sql
INSERT INTO near_earth_objects (
    nasa_id,
    name,
    absolute_magnitude,
    miss_distance_km,
    relative_velocity_kmh,
    diameter_min_m,
    diameter_max_m
) VALUES (
    %s, %s, %s, %s, %s, %s, %s
) ON CONFLICT (nasa_id) DO
UPDATE SET  
    name                  = EXCLUDED.name,
    absolute_magnitude    = EXCLUDED.absolute_magnitude,
    miss_distance_km      = EXCLUDED.miss_distance_km,
    relative_velocity_kmh = EXCLUDED.relative_velocity_kmh,
    diameter_min_m        = EXCLUDED.diameter_min_m,
    diameter_max_m        = EXCLUDED.diameter_max_m,
    updated_at            = now()
"""

create_table_starlink_moscow =  """--sql
CREATE TABLE IF NOT EXISTS starlink_moscow (
    norad_id   BIGINT PRIMARY KEY,
    name       VARCHAR(128) NOT NULL,
    designator  VARCHAR(64) NOT NULL,
    launch_date DATE NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    alt DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT now()
);
"""

insert_starlink_moscow = """--sql
INSERT INTO starlink_moscow 
    (
        norad_id, 
        name,
        designator,
        launch_date, 
        lat,
        lon,
        alt
    ) VALUES (
    %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (norad_id) DO
UPDATE SET 
name = EXCLUDED.name,
designator = EXCLUDED.designator
launch_date = EXCLUDED.launch_date,
lat = EXCLUDED.lat,
lon = EXCLUDED.lon,
alt = EXCLUDED.alt,
updated_at = now()
"""
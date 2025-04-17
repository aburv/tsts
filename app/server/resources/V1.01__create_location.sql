CREATE TABLE IF NOT EXISTS t_location (
    id VARCHAR(36) PRIMARY KEY,
    l_name VARCHAR(20),
    locality VARCHAR(20),
    l_city VARCHAR(20),
    l_state VARCHAR(20),
    l_country VARCHAR(20),
    l_pin VARCHAR(7),
    lat VARCHAR(20),
    long VARCHAR(20),
    is_active BOOLEAN
);

CREATE INDEX IF NOT EXISTS idx_location ON t_location(id);
CREATE INDEX IF NOT EXISTS idx_location_name ON t_location(l_name);
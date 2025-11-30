CREATE TABLE IF NOT EXISTS t_image (
    id VARCHAR(36) PRIMARY KEY,
    i_name VARCHAR(100),
    original BYTEA,
    c_original BYTEA,
    one BYTEA,
    two BYTEA,
    three BYTEA
);

CREATE INDEX IF NOT EXISTS idx_image ON t_image(id);

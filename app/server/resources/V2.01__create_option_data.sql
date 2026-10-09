CREATE TABLE IF NOT EXISTS form_field(
    id VARCHAR(36) PRIMARY KEY,
    form VARCHAR(50),
    field VARCHAR(50),
    is_active BOOLEAN
);

CREATE TABLE IF NOT EXISTS data_option(
    id VARCHAR(36) PRIMARY KEY,
    field_id VARCHAR(36) REFERENCES form_field(id),
    f_value VARCHAR(150),
    is_active BOOLEAN
);
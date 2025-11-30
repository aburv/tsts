CREATE TABLE IF NOT EXISTS migration (
    version VARCHAR(5),
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS audit (
    id VARCHAR(36) PRIMARY KEY,
    table_name VARCHAR(15),
    record_id VARCHAR(36),
    operation VARCHAR(6),
    op_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    op_user VARCHAR(36)
);

CREATE TABLE If NOT EXISTS audit_field (
    audit_id VARCHAR(36) REFERENCES audit(id),
    field_name VARCHAR(15),
    old_value VARCHAR(255),
    new_value VARCHAR(255)
);

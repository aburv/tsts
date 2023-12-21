CREATE SCHEMA IF NOT EXISTS game;

CREATE TABLE IF NOT EXISTS game.migrate (
    version VARCHAR(5),
    date_time timestamp default CURRENT_TIMESTAMP not null
);

CREATE TABLE IF NOT EXISTS game.audit (
    id VARCHAR(16) PRIMARY KEY,
    table_name VARCHAR(15),
    record_id VARCHAR(16),
    edit_type VARCHAR(10),
    edit_time TIMESTAMP default CURRENT_TIMESTAMP not null,
    edit_user VARCHAR(16)
);

CREATE TABLE If NOT EXISTS game.audit_field (
    audit_id VARCHAR(16),
    field_name VARCHAR(15),
    old_value VARCHAR(255),
    new_value VARCHAR(255)
);

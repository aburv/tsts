CREATE TABLE IF NOT EXISTS t_user (
    id VARCHAR(36) PRIMARY KEY,
    u_name VARCHAR(100),
    dp VARCHAR(36) REFERENCES t_image(id),
    is_active BOOLEAN
);

CREATE TABLE IF NOT EXISTS user_identifier (
    t_user VARCHAR(36) REFERENCES t_user(id),
    val VARCHAR(256) UNIQUE,
    type VARCHAR(1),
    g_id VARCHAR(256),
    is_verified BOOLEAN
);

CREATE TABLE If NOT EXISTS t_role (
    t_user VARCHAR(36) REFERENCES t_user(id),
    resource VARCHAR(1),
    record_id VARCHAR(36),
    permission VARCHAR(1)
);
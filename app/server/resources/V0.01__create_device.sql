CREATE TABLE IF NOT EXISTS device (
    id VARCHAR(36) PRIMARY KEY,
    device_id VARCHAR(30),
    other VARCHAR(255),
    os VARCHAR(10),
    os_version VARCHAR(10),
    device_type VARCHAR(10),
    platform VARCHAR(200),
    is_active Boolean
);
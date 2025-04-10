CREATE TABLE IF NOT EXISTS t_login (
    date_time timestamp default CURRENT_TIMESTAMP,
    t_user VARCHAR(36) REFERENCES t_user(id),
    device VARCHAR(36) REFERENCES device(id),
    l_location VARCHAR(36) REFERENCES t_location(id),
    ipv4 VARCHAR(40)
);
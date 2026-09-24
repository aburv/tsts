CREATE TABLE IF NOT EXISTS player (
    id VARCHAR(36) PRIMARY KEY NOT NULL,
    p_call_name VARCHAR(50) NOT NULL,
    p_gender VARCHAR(36) REFERENCES data_option(id) NOT NULL,
    p_birth DATE NOT NULL,
    p_weight FLOAT NOT NULL,
    p_height FLOAT NOT NULL,
    p_location VARCHAR(36) REFERENCES t_location(id),
    p_blood_group VARCHAR(36) REFERENCES data_option(id) NOT NULL,
    is_active BOOLEAN
);

CREATE TABLE IF NOT EXISTS player_gear (
    t_player VARCHAR(36) REFERENCES player(id),
    p_jersey_name VARCHAR(50) NOT NULL,
    p_jersey_number VARCHAR(2) NOT NULL,
    p_jersey_size VARCHAR(36) REFERENCES data_option(id) NOT NULL,
    p_shoe_size VARCHAR(36) REFERENCES data_option(id) NOT NULL
);

CREATE TABLE IF NOT EXISTS player_position (
    t_player VARCHAR(36) REFERENCES player(id),
    p_position VARCHAR(36) REFERENCES data_option(id) NOT NULL,
    delta REAL CHECK (delta >= 0 AND delta <= 1) NOT NULL,
    PRIMARY KEY (t_player, p_position)
);
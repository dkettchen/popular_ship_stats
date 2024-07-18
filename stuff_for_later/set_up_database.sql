DROP DATABASE IF EXISTS ship_rankings_db;
CREATE DATABASE ship_rankings_db;


CREATE TABLE property_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(20)
);

CREATE TABLE properties (
    property_id SERIAL PRIMARY KEY,
    property_name VARCHAR(50) NOT NULL,
    type_id INTEGER REFERENCES property_types(type_id),
    release_year INTEGER,
    ending_year INTEGER,
    total_instances INTEGER,
    total_parts INTEGER
);

CREATE TABLE parts (
    part_id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(property_id),
    part VARCHAR(50),
    release_year INTEGER,
    instances_in_part INTEGER
);

CREATE TABLE genders (
    gender_id SERIAL PRIMARY KEY,
    category_label VARCHAR(10)
);

CREATE TABLE racial_groups (
    eg_id SERIAL PRIMARY KEY,
    category_name VARCHAR(10)
);

CREATE TABLE characters (
    character_id SERIAL PRIMARY KEY,
    character_name VARCHAR(50) NOT NULL,
    property_id INTEGER REFERENCES properties(property_id),
    gender_id INTEGER REFERENCES genders(gender_id),
    racial_group INTEGER REFERENCES racial_groups(eg_id),
    total_appearances INTEGER,
    actor_name VARCHAR(50)
);

CREATE TABLE appearances_junction(
    appearance_id SERIAL PRIMARY KEY,
    character_id INTEGER REFERENCES characters(character_id),
    part_appeared_in INTEGER REFERENCES parts(part_id)
);

CREATE TABLE ships (
    ship_id SERIAL PRIMARY KEY,
    character_1 INTEGER NOT NULL REFERENCES characters(character_id),
    character_2 INTEGER NOT NULL REFERENCES characters(character_id),
    character_3 INTEGER REFERENCES characters(character_id),
    gender_combo VARCHAR(10)
);

CREATE TABLE ship_rankings (
    website VARCHAR(20) NOT NULL,
    ranking_year INTEGER NOT NULL,
    ranking INTEGER NOT NULL,
    ship_id INTEGER NOT NULL REFERENCES ships(ship_id),
    fic_type VARCHAR(20) DEFAULT 'slash',
    new_fic_instances INTEGER,
    total_fic_instances INTEGER
);
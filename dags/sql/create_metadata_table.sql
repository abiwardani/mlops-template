CREATE TABLE IF NOT EXISTS metadata_table (
    metadata_id SERIAL PRIMARY KEY,
    entry_name VARCHAR NOT NULL,
    entry_value VARCHAR NOT NULL,
    entry_datetime VARCHAR
);
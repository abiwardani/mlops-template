CREATE TABLE IF NOT EXISTS monitoring (
    monitoring_id SERIAL PRIMARY KEY,
    monitoring_datetime VARCHAR NOT NULL,
    target_drift NUMERIC NOT NULL,
    data_drift BOOLEAN NOT NULL,
    base_accuracy NUMERIC NOT NULL,
    new_accuracy NUMERIC NOT NULL
);
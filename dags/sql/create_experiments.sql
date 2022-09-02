CREATE TABLE IF NOT EXISTS experiments (
    experiment_id SERIAL PRIMARY KEY,
    experiment_datetime VARCHAR NOT NULL,
    cv_folds NUMERIC NOT NULL,
    rf_maxiter NUMERIC NOT NULL,
    rd_state NUMERIC NOT NULL,
    n_estimators NUMERIC NOT NULL,
    max_depth NUMERIC,
    min_samples_split NUMERIC NOT NULL,
    min_samples_leaf NUMERIC NOT NULL,
    test_acc NUMERIC NOT NULL
);
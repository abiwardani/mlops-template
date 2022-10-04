params = {
    "db_engine": "postgresql+psycopg2://airflow:airflow@postgres/airflow",
    "db_schema": "public",
    "db_experiments_table": "experiments",
    "db_monitoring_table": "monitoring",
    "db_batch_table": "batch_data",
    "test_split_ratio": 0.3,
    "cv_folds": 5,
    "rf_maxiter": 1000,
    "rd_state": 0,
    "save_experiments": True
}

import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

import experiment.ml_pipeline_config as config

db_engine = config.params["db_engine"]
db_schema = config.params["db_schema"]
table_name = config.params["db_monitoring_table"]


def insert_evaluation_results(**kwargs):
    target_drift = float(kwargs['ti'].xcom_pull(
        task_ids="data_and_model_evaluation.monitoring_model", key='target_drift'))
    data_drift = kwargs['ti'].xcom_pull(
        task_ids="data_and_model_evaluation.monitoring_model", key='data_drift') == "True"
    acc0 = float(kwargs['ti'].xcom_pull(
        task_ids="data_and_model_evaluation.monitoring_model", key='acc0'))
    acc1 = float(kwargs['ti'].xcom_pull(
        task_ids="data_and_model_evaluation.monitoring_model", key='acc1'))

    now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    log_df = pd.DataFrame([[now,
                            target_drift,
                            data_drift,
                            acc0,
                            acc1]],
                          columns=['monitoring_datetime',
                                   'target_drift',
                                   'data_drift',
                                   'base_accuracy',
                                   'new_accuracy',
                                   ])
    log_df.name = 'log_df'

    engine = create_engine(db_engine)
    log_df.to_sql(table_name, engine, schema=db_schema,
                  if_exists='append', index=False)

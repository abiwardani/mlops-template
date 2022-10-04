import subprocess
import mlflow

try:
    # Creating an experiment
    mlflow.create_experiment('producrec_production_model')
except:
    pass


def select_model(**kwargs):
    mlflow.set_tracking_uri('file:///opt/airflow/mlruns')
    mlflow.set_experiment('producrec_production_model')
    best_model_root = mlflow.get_experiment_by_name(
        'producrec_production_model').artifact_location
    best_run = mlflow.search_runs(
        experiment_names=['producrec_production_model'], order_by=["metrics.acc"])["artifact_uri"][0]

    model_dir = f'{best_run}/model/model.pkl'
    kwargs['ti'].xcom_push(key='model_dir', value=best_run)

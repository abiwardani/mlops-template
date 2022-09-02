import numpy as np
import logging

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, r2_score
import mlflow

from utils.files_util import load_files
import experiment.ml_pipeline_config as config

mlflow.set_tracking_uri('file:///opt/airflow/mlruns')
try:
    # Creating an experiment
    mlflow.create_experiment('producrec_baselining')
except:
    pass


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    acc = accuracy_score(actual, pred)
    return acc, rmse, mae, r2


def create_baseline():
    x_train, x_test, y_train, y_test = load_files(
        ['x_train', 'x_test', 'y_train', 'y_test'])

    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)

    rd_state = config.params['rd_state']

    rf_base = RandomForestClassifier(random_state=rd_state)
    rf_base.fit(x_train, y_train)

    y_pred = rf_base.predict(x_test)
    acc, rmse, mae, r2 = eval_metrics(y_test, y_pred)

    mlflow.set_tracking_uri('file:///opt/airflow/mlruns')

    # Setting the environment with the created experiment
    mlflow.set_experiment('producrec_baselining')

    with mlflow.start_run() as run:
        run_id = run.info.run_id

        logging.info("Random Forest Model (n_estimators=%f, max_depth=%f, min_samples_split=%f, min_samples_leaf=%f): acc - %f , rmse - %f , mae - %f, r2 - %f" %
                     (rf_base.n_estimators, rf_base.max_depth if rf_base.max_depth else 0, rf_base.min_samples_split, rf_base.min_samples_leaf, acc, rmse, mae, r2))

        mlflow.log_param("n_estimators", rf_base.n_estimators)
        mlflow.log_param("max_depth", rf_base.max_depth)
        mlflow.log_param("min_samples_split", rf_base.min_samples_split)
        mlflow.log_param("min_samples_leaf", rf_base.min_samples_leaf)
        mlflow.log_metric("acc", acc)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(rf_base, "baseline_model_"+run_id)

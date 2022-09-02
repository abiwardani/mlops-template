from cgi import test
from random import Random
import pandas as pd
from datetime import datetime
import mlflow
import numpy as np
import joblib
import pickle

from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestClassifier

from utils.files_util import load_files

try:
    # Creating an experiment
    mlflow.create_experiment('producrec_production_model')
except:
    pass


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    acc = accuracy_score(actual, pred)
    return acc, rmse, mae, r2


def fit_best_model():

    x_train, x_test, y_train, y_test, best_params = load_files(
        ['x_train', 'x_test', 'y_train', 'y_test', 'exp_info'])
    mlflow.set_tracking_uri('file:///opt/airflow/mlruns')

    baseline = mlflow.search_runs(experiment_names=[
                                  'producrec_baselining'], output_format="list")[0].data

    # Setting the environment with the created experiment
    mlflow.set_experiment('producrec_production_model')

    # start mlflow run
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        print(mlflow.get_tracking_uri())

        best_acc = 0
        best_idx = 0

        for i, test_acc in enumerate(best_params['test_acc']):
            if (test_acc > best_acc):
                best_acc = test_acc
                best_idx = i

        if (best_acc > baseline.metrics['acc']):
            n_estimators = best_params['n_estimators'][best_idx]
            max_depth = best_params['max_depth'][best_idx]
            min_samples_split = best_params['min_samples_split'][best_idx]
            min_samples_leaf = best_params['min_samples_leaf'][best_idx]
        else:
            n_estimators = int(baseline.params['n_estimators'])
            max_depth = None if baseline.params['max_depth'] == str(
                None) else int(baseline.params['max_depth'])
            min_samples_split = int(baseline.params['min_samples_split'])
            min_samples_leaf = int(baseline.params['min_samples_leaf'])

        rf_clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split,
                                        min_samples_leaf=min_samples_leaf, random_state=best_params['rd_state'][best_idx])
        rf_clf.fit(x_train, y_train)

        y_pred = rf_clf.predict(x_test)

        (acc, rmse, mae, r2) = eval_metrics(y_test, y_pred)

        print("Random Forest Model (n_estimators=%f, max_depth=%f, min_samples_split=%f, min_samples_leaf=%f):" % (
            n_estimators, max_depth if max_depth else 0, min_samples_split, min_samples_leaf))
        print("  Acc: %s " % acc)
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("min_samples_split", min_samples_split)
        mlflow.log_param("min_samples_leaf", min_samples_leaf)
        mlflow.log_metric("acc", acc)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(rf_clf, "model")

        # save best model
        # now = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
        filename = 'inference_model.pkl'
        # joblib.dump(rf_clf, '/opt/airflow/data/06_models/' + filename, compress=1)
        with open('/opt/airflow/data/06_models/' + filename, 'wb') as handle:
            pickle.dump(rf_clf, handle, protocol=pickle.HIGHEST_PROTOCOL)

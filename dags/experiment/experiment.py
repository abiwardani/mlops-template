import numpy as np
import pandas as pd
import logging
from datetime import datetime

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, r2_score, make_scorer
from sklearn.model_selection import ShuffleSplit
import mlflow

from utils.files_util import save_files, load_files
import experiment.ml_pipeline_config as config

mlflow.set_tracking_uri('file:///opt/airflow/mlruns')
try:
    # Creating an experiment
    mlflow.create_experiment('producrec_hyperparam_tuning')
except:
    pass


def experiment():
    x_train, y_train = load_files(
        ['x_train', 'y_train'])

    y_train = np.ravel(y_train)

    # define search space
    n_estimators = [int(x)
                    for x in np.linspace(start=100, stop=1000, num=10)]
    max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
    max_depth.append(None)
    min_samples_split = [2, 5, 10]
    min_samples_leaf = [1, 2, 4]

    # short version
    n_estimators = [100, 700]
    max_depth = [None]
    min_samples_split = [5]
    min_samples_leaf = [2]

    # def evaluation metrics
    rd_state = config.params["rd_state"]
    rf_maxiter = config.params["rf_maxiter"]
    scoring = {"acc": make_scorer(accuracy_score), "rmse": make_scorer(mean_squared_error, greater_is_better=False), "mae": make_scorer(
        mean_absolute_error, greater_is_better=False), "r2": make_scorer(r2_score)}
    cv_folds = config.params["cv_folds"]
    cv = ShuffleSplit(
        n_splits=cv_folds, test_size=0.3, random_state=rd_state)

    # create random grid
    random_grid = {'n_estimators': n_estimators,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf}

    # cross-validated training with randomized search
    rf_base = RandomForestClassifier(random_state=rd_state)
    rf_random = RandomizedSearchCV(
        estimator=rf_base, param_distributions=random_grid, n_iter=rf_maxiter, cv=cv, scoring=scoring, refit="acc", random_state=rd_state, n_jobs=1)
    rf_random.fit(x_train, y_train)

    # select best parameters
    best_params = rf_random.best_params_
    best_n_estimators = best_params['n_estimators']
    best_max_depth = best_params['max_depth']
    best_min_samples_split = best_params['min_samples_split']
    best_min_samples_leaf = best_params['min_samples_leaf']

    # performances on test set
    test_acc = rf_random.best_score_

    searched_params = rf_random.cv_results_['params']
    test_accs = rf_random.cv_results_['mean_test_acc']
    test_rmses = rf_random.cv_results_['mean_test_rmse']
    test_maes = rf_random.cv_results_['mean_test_mae']
    test_r2s = rf_random.cv_results_['mean_test_r2']

    if (config.params['save_experiments']):
        mlflow.set_tracking_uri('file:///opt/airflow/mlruns')

        # Setting the environment with the created experiment
        mlflow.set_experiment('producrec_hyperparam_tuning')

        for i in range(len(searched_params)):
            # start mlflow run
            with mlflow.start_run() as run:
                run_id = run.info.run_id
                rf_run = RandomForestClassifier(
                    **searched_params[i], random_state=rd_state).fit(x_train, y_train)
                acc, rmse, mae, r2 = test_accs[i], test_rmses[i], test_maes[i], test_r2s[i]

                logging.info("Random Forest Model (n_estimators=%f, max_depth=%f, min_samples_split=%f, min_samples_leaf=%f): acc - %f , rmse - %f , mae - %f, r2 - %f" % (
                    searched_params[i]['n_estimators'], searched_params[i]['max_depth'] if searched_params[i]['max_depth'] else 0, searched_params[i]['min_samples_split'], searched_params[i]['min_samples_leaf'], acc, rmse, mae, r2))

                mlflow.log_param("n_estimators", n_estimators)
                mlflow.log_param("max_depth", max_depth)
                mlflow.log_param("min_samples_split", min_samples_split)
                mlflow.log_param("min_samples_leaf", min_samples_leaf)
                mlflow.log_metric("acc", acc)
                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)

                mlflow.sklearn.log_model(rf_run, "model_"+run_id)

    # save experiments information for historical persistence
    now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    exp_info = pd.DataFrame([[now,
                            cv_folds,
                            rf_maxiter,
                            rd_state,
                            best_n_estimators,
                            best_max_depth,
                            best_min_samples_split,
                            best_min_samples_leaf,
                            test_acc]],
                            columns=['experiment_datetime',
                                     'cv_folds',
                                     'rf_maxiter',
                                     'rd_state',
                                     'n_estimators',
                                     'max_depth',
                                     'min_samples_split',
                                     'min_samples_leaf',
                                     'test_acc'
                                     ])
    exp_info.name = 'exp_info'

    save_files([exp_info])

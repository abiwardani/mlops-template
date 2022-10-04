from platform import python_branch

from airflow.models import DAG

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup

from datetime import datetime
import time

from utils.load_data import load_data
from experiment.preprocess_data import preprocess_data
from experiment.create_baseline import create_baseline
from experiment.experiment import experiment
from experiment.track_experiments_info import track_experiments_info
from experiment.fit_best_model import fit_best_model
from utils.save_batch_data import save_batch_data
from predict.select_model import select_model


default_args = {
    'owner': 'Muhammad Rifat Abiwardani',
    'email_on_failure': False,
    'email': ['13519205@std.stei.itb.ac.id'],
    'start_date': datetime(2022, 7, 13)
}

with DAG(
    "ml_pipeline",
    description='End-to-end ML pipeline example',
    schedule_interval='@monthly',
    default_args=default_args,
        catchup=False) as dag:

    # task: 1
    with TaskGroup('creating_storage_structures') as creating_storage_structures:

        # task: 1.1
        creating_batch_data_table = PostgresOperator(
            task_id="creating_batch_data_table",
            postgres_conn_id='postgres_default',
            sql='sql/create_batch_data_table.sql'
        )

    #task: 2
    with TaskGroup('fetching_data') as fetching_data:

        fetching_csv_data = PythonOperator(
            task_id='fetching_data',
            python_callable=load_data
        )

    # task: 3
    with TaskGroup('preparing_data') as preparing_data:

        # task: 3.1
        preprocessing = PythonOperator(
            task_id='preprocessing',
            python_callable=preprocess_data
        )

    # task: 4
    with TaskGroup('model_experimentation') as model_experimentation:

        # =======
        # task: 4.1
        creating_baseline = PythonOperator(
            task_id='creating_baseline',
            python_callable=create_baseline
        )

        # task: 4.2
        hyperparam_tuning = PythonOperator(
            task_id='hyperparam_tuning',
            python_callable=experiment
        )

        creating_baseline >> hyperparam_tuning

    # task: 5
    with TaskGroup('after_crossvalidation') as after_crossvalidation:

        # =======
        # task: 5.1
        saving_results = PythonOperator(
            task_id='saving_results',
            python_callable=track_experiments_info
        )

        # task: 5.2
        fitting_best_model = PythonOperator(
            task_id='fitting_best_model',
            python_callable=fit_best_model
        )

        saving_results >> fitting_best_model

    # task: 6
    with TaskGroup('update_model_serving') as update_model_serving:

        # =======
        # task: 6.1
        stopping_serving = BashOperator(
            task_id='stopping_serving',
            bash_command='sshpass -p "sshpass" nohup ssh pythonssh@mlflow-model-server -o StrictHostKeyChecking=no -t -f -n "fuser -k 50051/tcp" >/dev/null 2>/dev/null &',
            do_xcom_push=True,
            dag=dag
        )

        # task: 6.2
        selecting_model = PythonOperator(
            task_id='selecting_model',
            python_callable=select_model,
            do_xcom_push=True
        )

        # task: 6.3
        preparing_server = BashOperator(
            task_id='preparing_server',
            bash_command='sshpass -p "sshpass" nohup ssh pythonssh@mlflow-model-server -o StrictHostKeyChecking=no -t -f -n "python -m pip install --user --no-index --find-links /opt/airflow/data/artifacts grpcio==1.47.0" >/dev/null 2>/dev/null &',
            do_xcom_push=True,
            dag=dag
        )

        # task: 6.4
        # delay 10s
        waiting_installation = PythonOperator(
            task_id='waiting_installation',
            python_callable=lambda: time.sleep(10)
        )

        # task: 6.5
        serving_model = BashOperator(
            task_id='serving_model',
            # bash_command='sshpass -p "sshpass" nohup ssh pythonssh@mlflow-model-server -o StrictHostKeyChecking=no -t -f -n "mlflow models serve -m {{ ti.xcom_pull(task_ids="update_model_serving.selecting_model", key="model_dir") }}/model -p 1234 --host 0.0.0.0 --env-manager local" >/dev/null 2>/dev/null &',
            bash_command='sshpass -p "sshpass" nohup ssh pythonssh@mlflow-model-server -o StrictHostKeyChecking=no -t -f -n "python /opt/airflow/dags/predict/server.py {{ ti.xcom_pull(task_ids="update_model_serving.selecting_model", key="model_dir") }}/model" >/dev/null 2>/dev/null &',
            do_xcom_push=True,
            dag=dag
        )

        stopping_serving >> selecting_model >> preparing_server >> waiting_installation >> serving_model

    creating_storage_structures >> fetching_data >> preparing_data >> model_experimentation >> after_crossvalidation >> update_model_serving

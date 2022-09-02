from platform import python_branch
from airflow.models import DAG

from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.email import EmailOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup

from datetime import datetime

from monitoring.monitor_model import monitor_model
from monitoring.branch_monitoring import branch_monitoring

default_args = {
    'owner': 'Muhammad Rifat Abiwardani',
    'email_on_failure': False,
    'email': ['13519205@std.stei.itb.ac.id'],
    'start_date': datetime(2022, 7, 13)
}

with DAG(
    "monitoring_pipeline",
    description='Target and dataset drift monitoring with model degradation check pipeline',
    schedule_interval='@daily',
    default_args=default_args,
        catchup=False) as dag:

    # task: 1
    with TaskGroup('preparing_data') as preparing_data:

        # task 1.1
        creating_monitoring = PostgresOperator(
            task_id="creating_monitoring",
            postgres_conn_id='postgres_default',
            sql='sql/create_monitoring.sql'
        )

        # task 1.2
        # fetching_new_data = PostgresOperator(

        # )

    # task: 2
    with TaskGroup('data_and_model_evaluation') as data_and_model_evaluation:

        # task: 2.1
        monitoring_model = PythonOperator(
            task_id='monitoring_model',
            python_callable=monitor_model
        )

    # task: 3
    with TaskGroup('reporting') as reporting:

        # task: 3.1
        inserting_evaluation_results = PostgresOperator(
            task_id='inserting_evaluation_results',
            postgres_conn_id='postgres_default',
            sql='sql/insert_evaluation_results.sql'
        )

    # task: 4
    branching_monitoring = BranchPythonOperator(
        task_id='branching_monitoring',
        python_callable=branch_monitoring,
        provide_context=True,
        dag=dag
    )

    # task: 5
    with TaskGroup('evaluation_result_handling') as evaluation_result_handling:

        # task: 5.a.1
        retraining = TriggerDagRunOperator(
            task_id='retraining',
            trigger_dag_id='ml_pipeline',
        )

        # task: 5.a.2
        sending_notification = EmailOperator(
            task_id='sending_notification',
            to='abi.wardani85@gmail.com',
            subject=f'PRODUCREC_MONITORING_{datetime.now()}',
            html_content="{{ task_instance.xcom_pull(task_ids='data_and_model_evaluation.monitoring_model', key='report_message') }}"
        )

        # task: 5.b
        skipping_retraining = EmptyOperator(
            task_id='skipping_retraining'
        )

        retraining >> sending_notification

    data_and_model_evaluation >> branching_monitoring >> evaluation_result_handling

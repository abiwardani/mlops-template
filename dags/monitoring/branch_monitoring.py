

def branch_monitoring(**kwargs):
    TARGET_DRIFT_THRESHOLD = 0.5
    DEGRADATION_THRESHOLD = 0.75

    target_drift = float(kwargs['ti'].xcom_pull(
        task_ids="data_and_model_evaluation.monitoring_model", key='target_drift'))
    data_drift = kwargs['ti'].xcom_pull(
        task_ids="data_and_model_evaluation.monitoring_model", key='data_drift') == "True"
    acc0 = float(kwargs['ti'].xcom_pull(
        task_ids="data_and_model_evaluation.monitoring_model", key='acc0'))
    acc1 = float(kwargs['ti'].xcom_pull(
        task_ids="data_and_model_evaluation.monitoring_model", key='acc1'))

    if (target_drift > TARGET_DRIFT_THRESHOLD or data_drift == True or acc1 <= acc0 * DEGRADATION_THRESHOLD):
        print(target_drift, str(type(target_drift)))
        print(data_drift, str(type(data_drift)))
        return 'evaluation_result_handling.retraining'
    else:
        return 'evaluation_result_handling.skipping_retraining'

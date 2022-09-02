import requests
import pandas as pd
import numpy as np
import json

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection, CatTargetDriftProfileSection
from evidently.pipeline.column_mapping import ColumnMapping

from utils.files_util import load_files


def monitor_model(**kwargs):
    import warnings
    warnings.filterwarnings('ignore')
    warnings.simplefilter('ignore')

    # REST version

    # column mapping
    column_mapping = ColumnMapping()
    column_mapping.target = 'producrec_dataset_acq.reordered'
    column_mapping.id = None
    column_mapping.numerical_features = ['producrec_dataset_acq.price', 'producrec_dataset_acq.site_prod_trx', 'producrec_dataset_acq.site_prod_reorder_trx',
                                         'producrec_dataset_acq.num_package_purchased', 'producrec_dataset_acq.site_trx', 'producrec_dataset_acq.site_reorder_trx']
    column_mapping.categorical_features = ['producrec_dataset_acq.site_id', 'producrec_dataset_acq.content_id', 'producrec_dataset_acq.category',
                                           'producrec_dataset_acq.num_msisdn_purchaser', 'producrec_dataset_acq.prod_trx', 'producrec_dataset_acq.prod_reorder_trx']

    # check target and data drift

    drift_profile = Profile(sections=[DataDriftProfileSection(),
                                      CatTargetDriftProfileSection()])

    # schema 1
    # canonical data and new data kept in separate tables
    canonical_data, new_data = load_files(['raw_data', 'new_data'])

    drift_profile.calculate(canonical_data, new_data,
                            column_mapping=column_mapping)

    # schema 2
    # all N rows of data is kept in one table, rows 0-X is canonical data, rows X-N is new data
    # initial_data_size = 100000
    # producrec_data = load_files(["producrec_data"])[0]

    # drift_profile.calculate(producrec_data.iloc[:initial_data_size, :],
    #                         producrec_data.iloc[initial_data_size:, :], column_mapping=None)

    # read drift
    profile_info = json.loads(drift_profile.json())

    target_drift = profile_info["cat_target_drift"]["data"]["metrics"]["target_drift"]
    data_drift = profile_info["data_drift"]["data"]["metrics"]["dataset_drift"]

    # check model performance

    # schema 1
    r0 = requests.post("http://mlflow-service:6000/predict", json=canonical_data[['producrec_dataset_acq.site_id', 'producrec_dataset_acq.content_id', 'producrec_dataset_acq.category', 'producrec_dataset_acq.price', 'producrec_dataset_acq.site_prod_trx', 'producrec_dataset_acq.site_prod_reorder_trx',
                       'producrec_dataset_acq.num_package_purchased', 'producrec_dataset_acq.site_trx', 'producrec_dataset_acq.site_reorder_trx', 'producrec_dataset_acq.num_msisdn_purchaser', 'producrec_dataset_acq.prod_trx', 'producrec_dataset_acq.prod_reorder_trx']].to_dict(orient='records'))
    r1 = requests.post("http://mlflow-service:6000/predict", json=new_data[['producrec_dataset_acq.site_id', 'producrec_dataset_acq.content_id', 'producrec_dataset_acq.category', 'producrec_dataset_acq.price', 'producrec_dataset_acq.site_prod_trx', 'producrec_dataset_acq.site_prod_reorder_trx',
                       'producrec_dataset_acq.num_package_purchased', 'producrec_dataset_acq.site_trx', 'producrec_dataset_acq.site_reorder_trx', 'producrec_dataset_acq.num_msisdn_purchaser', 'producrec_dataset_acq.prod_trx', 'producrec_dataset_acq.prod_reorder_trx']].to_dict(orient='records'))

    canon_pred = list(map(int, r0._content.decode('UTF-8')[1:-1].split(',')))
    new_pred = list(map(int, r0._content.decode('UTF-8')[1:-1].split(',')))

    acc0 = np.sum(np.array(canon_pred) ==
                  canonical_data['producrec_dataset_acq.reordered'].values)/len(canon_pred)
    acc1 = np.sum(np.array(new_pred) ==
                  new_data['producrec_dataset_acq.reordered'].values)/len(new_pred)

    # schema 2
    # r0 = requests.post("http://mlflow-service:6000/predict", json=producrec_data[['producrec_dataset_acq.site_id', 'producrec_dataset_acq.content_id', 'producrec_dataset_acq.category', 'producrec_dataset_acq.price', 'producrec_dataset_acq.site_prod_trx', 'producrec_dataset_acq.site_prod_reorder_trx', 'producrec_dataset_acq.num_package_purchased', 'producrec_dataset_acq.site_trx', 'producrec_dataset_acq.site_reorder_trx', 'producrec_dataset_acq.num_msisdn_purchaser', 'producrec_dataset_acq.prod_trx', 'producrec_dataset_acq.prod_reorder_trx'].iloc[:initial_data_size, :-1]].to_dict(orient='records'))
    # r1 = requests.post("http://mlflow-service:6000/predict", json=producrec_data[['producrec_dataset_acq.site_id', 'producrec_dataset_acq.content_id', 'producrec_dataset_acq.category', 'producrec_dataset_acq.price', 'producrec_dataset_acq.site_prod_trx', 'producrec_dataset_acq.site_prod_reorder_trx', 'producrec_dataset_acq.num_package_purchased', 'producrec_dataset_acq.site_trx', 'producrec_dataset_acq.site_reorder_trx', 'producrec_dataset_acq.num_msisdn_purchaser', 'producrec_dataset_acq.prod_trx', 'producrec_dataset_acq.prod_reorder_trx'].iloc[initial_data_size:, :-1]].to_dict(orient='records'))

    # acc0 = np.sum(r0._content == producrec_data.iloc
    #               [:initial_data_size, -1].values)/len(r0._content)
    # acc1 = np.sum(r1._content == producrec_data.iloc
    #               [initial_data_size:, -1].values)/len(r1._content)

    report_message = ""
    report_message += f'TARGET DRIFT    : {target_drift}<br>'
    report_message += f'DATA DRIFT      : {data_drift}<br>'
    report_message += f'BASE ACCURACY   : {acc0}<br>'
    report_message += f'NEW ACCURACY    : {acc1}<br>'

    kwargs['ti'].xcom_push(key='target_drift', value=target_drift)
    kwargs['ti'].xcom_push(key='data_drift', value=data_drift)
    kwargs['ti'].xcom_push(key='acc0', value=acc0)
    kwargs['ti'].xcom_push(key='acc1', value=acc1)
    kwargs['ti'].xcom_push(key='report_message', value=report_message)

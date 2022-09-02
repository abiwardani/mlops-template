from flask import Flask

#!/usr/bin/env python
# encoding: utf-8
import json
import pandas as pd
from requests import post
from requests.models import Response
import os
from flask import Flask, request
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)


def load_files(filename):
    if os.path.isfile('../opt/airflow/data/01_raw/' + filename):
        df = pd.read_csv("../opt/airflow/data/01_raw/" + filename)
        return df


@app.route('/predict', methods=['POST'])
def predict():
    # print(request.json)
    new_inputs_df = pd.DataFrame(request.json)

    producrec_ds = load_files('raw_data.csv')
    producrec_data = producrec_ds.iloc[:, :-2]
    ref_df = producrec_data

    # label encoding for categorical fields
    le = LabelEncoder()
    le.fit(ref_df['producrec_dataset_acq.site_id'])
    new_inputs_df['producrec_dataset_acq.site_id'] = le.transform(
        new_inputs_df['producrec_dataset_acq.site_id'])

    le.fit(ref_df['producrec_dataset_acq.category'])
    new_inputs_df['producrec_dataset_acq.category'] = le.transform(
        new_inputs_df['producrec_dataset_acq.category'])

    new_inputs_json = new_inputs_df.to_dict(orient='records')
    predictions = post(
        url="http://mlflow-model-server:1234/invocations", json=new_inputs_json)

    response = Response()
    response.status_code = predictions.status_code
    response._content = predictions._content

    return (response._content, response.status_code, response.headers.items())


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='6000')

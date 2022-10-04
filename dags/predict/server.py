import grpc
from concurrent import futures
import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder

import mlflow.pyfunc

import producrec_pb2 as producrec_pb2
import producrec_pb2_grpc as producrec_pb2_grpc

if (len(sys.argv) == 1):
    print("Specify model path. Usage `$ python server.py /path/to/model`")
    exit(1)

MODEL_PATH = sys.argv[1]
MODEL = mlflow.pyfunc.load_model(MODEL_PATH)
CANONICAL_DATA = pd.read_csv("/opt/airflow/data/01_raw/raw_data.csv")


def encode_data(new_data):
    df = CANONICAL_DATA.iloc[:, :-2]
    # labels = canonical_data.iloc[:, -2]

    # label encoding for categorical fields
    le = LabelEncoder()
    le.fit(df['producrec_dataset_acq.site_id'])
    new_data['producrec_dataset_acq.site_id'] = le.transform(
        new_data['producrec_dataset_acq.site_id'])
    le.fit(df['producrec_dataset_acq.category'])
    new_data['producrec_dataset_acq.category'] = le.transform(
        new_data['producrec_dataset_acq.category'])

    # save dataset
    new_data.name = 'df'

    return new_data


class ProducrecModelsServicer(producrec_pb2_grpc.ProducrecServicer):
    def _predict(self, input):
        new_data = pd.DataFrame({"producrec_dataset_acq.site_id": [_ for _ in input.list_site_id], "producrec_dataset_acq.content_id": [_ for _ in input.list_content_id], "producrec_dataset_acq.category": [_ for _ in input.list_category], "producrec_dataset_acq.price": [_ for _ in input.list_price], "producrec_dataset_acq.site_prod_trx": [_ for _ in input.list_site_prod_trx], "producrec_dataset_acq.site_prod_reorder_trx": [_ for _ in input.list_site_prod_reorder_trx],
                                 "producrec_dataset_acq.num_package_purchased": [_ for _ in input.list_num_package_purchased], "producrec_dataset_acq.site_trx": [_ for _ in input.list_site_trx], "producrec_dataset_acq.site_reorder_trx": [_ for _ in input.list_site_reorder_trx], "producrec_dataset_acq.num_msisdn_purchaser": [_ for _ in input.list_num_msisdn_purchaser], "producrec_dataset_acq.prod_trx": [_ for _ in input.list_prod_trx], "producrec_dataset_acq.prod_reorder_trx": [_ for _ in input.list_prod_reorder_trx]})
        encoded_data = encode_data(new_data)
        return MODEL.predict(encoded_data[['producrec_dataset_acq.site_id', 'producrec_dataset_acq.content_id', 'producrec_dataset_acq.category', 'producrec_dataset_acq.price', 'producrec_dataset_acq.site_prod_trx', 'producrec_dataset_acq.site_prod_reorder_trx',
                                           'producrec_dataset_acq.num_package_purchased', 'producrec_dataset_acq.site_trx', 'producrec_dataset_acq.site_reorder_trx', 'producrec_dataset_acq.num_msisdn_purchaser', 'producrec_dataset_acq.prod_trx', 'producrec_dataset_acq.prod_reorder_trx']])

    def predict(self, request, context):
        print(f"RECEIVED: {request}")
        response = producrec_pb2.Output(
            list_label=[_ for _ in self._predict(request).tolist()])

        return response


maxMsgLength = 16 * 1024 * 1024
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[('grpc.max_message_length', maxMsgLength), ('grpc.max_send_message_length', maxMsgLength), ('grpc.max_receive_message_length', maxMsgLength)])
producrec_pb2_grpc.add_ProducrecServicer_to_server(ProducrecModelsServicer(), server)

print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()

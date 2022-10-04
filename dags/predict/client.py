import grpc
import sys
import pandas as pd
import os.path

import producrec_pb2 as producrec_pb2
import producrec_pb2_grpc as producrec_pb2_grpc


def run_client(predict_df):
    maxMsgLength = 16 * 1024 * 1024
    channel = grpc.insecure_channel('mlflow-model-server:50051', options=[('grpc.max_message_length', maxMsgLength), ('grpc.max_send_message_length', maxMsgLength), ('grpc.max_receive_message_length', maxMsgLength)])
    stub = producrec_pb2_grpc.ProducrecStub(channel)

    list_site_id = [_ for _ in predict_df["producrec_dataset_acq.site_id"]]
    list_content_id = [_ for _ in predict_df["producrec_dataset_acq.content_id"]]
    list_category = [_ for _ in predict_df["producrec_dataset_acq.category"]]
    list_price = [_ for _ in predict_df["producrec_dataset_acq.price"]]
    list_site_prod_trx = [_ for _ in predict_df["producrec_dataset_acq.site_prod_trx"]]
    list_site_prod_reorder_trx = [
        _ for _ in predict_df["producrec_dataset_acq.site_prod_reorder_trx"]]
    list_num_package_purchased = [
        _ for _ in predict_df["producrec_dataset_acq.num_package_purchased"]]
    list_site_trx = [_ for _ in predict_df["producrec_dataset_acq.site_trx"]]
    list_site_reorder_trx = [
        _ for _ in predict_df["producrec_dataset_acq.site_reorder_trx"]]
    list_num_msisdn_purchaser = [
        _ for _ in predict_df["producrec_dataset_acq.num_msisdn_purchaser"]]
    list_prod_trx = [_ for _ in predict_df["producrec_dataset_acq.prod_trx"]]
    list_prod_reorder_trx = [
        _ for _ in predict_df["producrec_dataset_acq.prod_reorder_trx"]]
    input = producrec_pb2.Input(list_site_id=list_site_id, list_content_id=list_content_id, list_category=list_category, list_price=list_price, list_site_prod_trx=list_site_prod_trx, list_site_prod_reorder_trx=list_site_prod_reorder_trx,
                                list_num_package_purchased=list_num_package_purchased, list_site_trx=list_site_trx, list_site_reorder_trx=list_site_reorder_trx, list_num_msisdn_purchaser=list_num_msisdn_purchaser, list_prod_trx=list_prod_trx, list_prod_reorder_trx=list_prod_reorder_trx)

    response = stub.predict(input)

    return response.list_label


if (__name__ == "__main__"):

    if (len(sys.argv) == 1):
        print("Specify test data path. Usage `$ python server.py /path/to/data`")
        exit(1)
    elif (not (os.path.isfile(sys.argv[1]))):
        print("Invalid filepath.")
        exit(1)
    
    test_data = pd.read_csv(sys.argv[1])

    list_label = run_client(test_data)
    print(list_label)

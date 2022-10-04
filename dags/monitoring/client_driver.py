import grpc

import monitoring.producrec_pb2 as producrec_pb2
import monitoring.producrec_pb2_grpc as producrec_pb2_grpc

maxMsgLength = 16 * 1024 * 1024
channel = grpc.insecure_channel('mlflow-model-server:50051', options=[('grpc.max_message_length', maxMsgLength), ('grpc.max_send_message_length', maxMsgLength), ('grpc.max_receive_message_length', maxMsgLength)])
stub = producrec_pb2_grpc.ProducrecStub(channel)

list_site_id = ["ADL001"]
list_content_id = [34209]
list_category = ["Acquisition _ InternetMax"]
list_price = [73000]
list_site_prod_trx = [1]
list_site_prod_reorder_trx = [0]
list_num_package_purchased = [14]
list_site_trx = [31]
list_site_reorder_trx = [3]
list_num_msisdn_purchaser = [3345]
list_prod_trx = [3784]
list_prod_reorder_trx = [235]
input = producrec_pb2.Input(list_site_id=list_site_id, list_content_id=list_content_id, list_category=list_category, list_price=list_price, list_site_prod_trx=list_site_prod_trx, list_site_prod_reorder_trx=list_site_prod_reorder_trx,
                            list_num_package_purchased=list_num_package_purchased, list_site_trx=list_site_trx, list_site_reorder_trx=list_site_reorder_trx, list_num_msisdn_purchaser=list_num_msisdn_purchaser, list_prod_trx=list_prod_trx, list_prod_reorder_trx=list_prod_reorder_trx)

response = stub.predict(input)

print(response.list_label)

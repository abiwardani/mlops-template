# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: producrec.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fproducrec.proto\"\xd4\x02\n\x05Input\x12\x14\n\x0clist_site_id\x18\x01 \x03(\t\x12\x17\n\x0flist_content_id\x18\x02 \x03(\x05\x12\x15\n\rlist_category\x18\x03 \x03(\t\x12\x12\n\nlist_price\x18\x04 \x03(\x05\x12\x1a\n\x12list_site_prod_trx\x18\x05 \x03(\x05\x12\"\n\x1alist_site_prod_reorder_trx\x18\x06 \x03(\x05\x12\"\n\x1alist_num_package_purchased\x18\x07 \x03(\x05\x12\x15\n\rlist_site_trx\x18\x08 \x03(\x05\x12\x1d\n\x15list_site_reorder_trx\x18\t \x03(\x05\x12!\n\x19list_num_msisdn_purchaser\x18\n \x03(\x05\x12\x15\n\rlist_prod_trx\x18\x0b \x03(\x05\x12\x1d\n\x15list_prod_reorder_trx\x18\x0c \x03(\x05\"\x1c\n\x06Output\x12\x12\n\nlist_label\x18\x01 \x03(\x05\x32)\n\tProducrec\x12\x1c\n\x07predict\x12\x06.Input\x1a\x07.Output\"\x00\x62\x06proto3')



_INPUT = DESCRIPTOR.message_types_by_name['Input']
_OUTPUT = DESCRIPTOR.message_types_by_name['Output']
Input = _reflection.GeneratedProtocolMessageType('Input', (_message.Message,), {
  'DESCRIPTOR' : _INPUT,
  '__module__' : 'producrec_pb2'
  # @@protoc_insertion_point(class_scope:Input)
  })
_sym_db.RegisterMessage(Input)

Output = _reflection.GeneratedProtocolMessageType('Output', (_message.Message,), {
  'DESCRIPTOR' : _OUTPUT,
  '__module__' : 'producrec_pb2'
  # @@protoc_insertion_point(class_scope:Output)
  })
_sym_db.RegisterMessage(Output)

_PRODUCREC = DESCRIPTOR.services_by_name['Producrec']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _INPUT._serialized_start=20
  _INPUT._serialized_end=360
  _OUTPUT._serialized_start=362
  _OUTPUT._serialized_end=390
  _PRODUCREC._serialized_start=392
  _PRODUCREC._serialized_end=433
# @@protoc_insertion_point(module_scope)

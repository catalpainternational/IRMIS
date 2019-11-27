# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: report.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='report.proto',
  package='assets',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0creport.proto\x12\x06\x61ssets\x1a\x1fgoogle/protobuf/timestamp.proto\"[\n\x06Report\x12\x0e\n\x06\x66ilter\x18\x01 \x01(\t\x12\x0f\n\x07lengths\x18\x02 \x01(\t\x12\x30\n\x10\x61ttribute_tables\x18\x03 \x03(\x0b\x32\x16.assets.AttributeTable\"{\n\x0e\x41ttributeTable\x12\x19\n\x11primary_attribute\x18\x01 \x01(\t\x12\x1b\n\x13secondary_attribute\x18\x02 \x03(\t\x12\x31\n\x11\x61ttribute_entries\x18\x03 \x03(\x0b\x32\x16.assets.AttributeEntry\"\xc1\x01\n\x0e\x41ttributeEntry\x12\x16\n\x0e\x63hainage_start\x18\x01 \x01(\x02\x12\x14\n\x0c\x63hainage_end\x18\x02 \x01(\x02\x12\x0e\n\x06values\x18\x03 \x01(\t\x12\x11\n\tsurvey_id\x18\x04 \x01(\r\x12\x31\n\rdate_surveyed\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08\x61\x64\x64\x65\x64_by\x18\x06 \x01(\t\x12\x19\n\x11primary_attribute\x18\x07 \x01(\tb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_REPORT = _descriptor.Descriptor(
  name='Report',
  full_name='assets.Report',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='assets.Report.filter', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lengths', full_name='assets.Report.lengths', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attribute_tables', full_name='assets.Report.attribute_tables', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=148,
)


_ATTRIBUTETABLE = _descriptor.Descriptor(
  name='AttributeTable',
  full_name='assets.AttributeTable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='primary_attribute', full_name='assets.AttributeTable.primary_attribute', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='secondary_attribute', full_name='assets.AttributeTable.secondary_attribute', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attribute_entries', full_name='assets.AttributeTable.attribute_entries', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=150,
  serialized_end=273,
)


_ATTRIBUTEENTRY = _descriptor.Descriptor(
  name='AttributeEntry',
  full_name='assets.AttributeEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chainage_start', full_name='assets.AttributeEntry.chainage_start', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chainage_end', full_name='assets.AttributeEntry.chainage_end', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='values', full_name='assets.AttributeEntry.values', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='survey_id', full_name='assets.AttributeEntry.survey_id', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_surveyed', full_name='assets.AttributeEntry.date_surveyed', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='added_by', full_name='assets.AttributeEntry.added_by', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='primary_attribute', full_name='assets.AttributeEntry.primary_attribute', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=276,
  serialized_end=469,
)

_REPORT.fields_by_name['attribute_tables'].message_type = _ATTRIBUTETABLE
_ATTRIBUTETABLE.fields_by_name['attribute_entries'].message_type = _ATTRIBUTEENTRY
_ATTRIBUTEENTRY.fields_by_name['date_surveyed'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['Report'] = _REPORT
DESCRIPTOR.message_types_by_name['AttributeTable'] = _ATTRIBUTETABLE
DESCRIPTOR.message_types_by_name['AttributeEntry'] = _ATTRIBUTEENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Report = _reflection.GeneratedProtocolMessageType('Report', (_message.Message,), {
  'DESCRIPTOR' : _REPORT,
  '__module__' : 'report_pb2'
  # @@protoc_insertion_point(class_scope:assets.Report)
  })
_sym_db.RegisterMessage(Report)

AttributeTable = _reflection.GeneratedProtocolMessageType('AttributeTable', (_message.Message,), {
  'DESCRIPTOR' : _ATTRIBUTETABLE,
  '__module__' : 'report_pb2'
  # @@protoc_insertion_point(class_scope:assets.AttributeTable)
  })
_sym_db.RegisterMessage(AttributeTable)

AttributeEntry = _reflection.GeneratedProtocolMessageType('AttributeEntry', (_message.Message,), {
  'DESCRIPTOR' : _ATTRIBUTEENTRY,
  '__module__' : 'report_pb2'
  # @@protoc_insertion_point(class_scope:assets.AttributeEntry)
  })
_sym_db.RegisterMessage(AttributeEntry)


# @@protoc_insertion_point(module_scope)

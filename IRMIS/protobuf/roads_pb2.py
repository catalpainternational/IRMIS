# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: roads.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='roads.proto',
  package='assets',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0broads.proto\x12\x06\x61ssets\"\xd3\x02\n\x04Road\x12\n\n\x02id\x18\x01 \x01(\r\x12\x12\n\ngeojson_id\x18\x02 \x01(\r\x12\x11\n\troad_code\x18\x03 \x01(\t\x12\x11\n\troad_name\x18\x04 \x01(\t\x12\x11\n\troad_type\x18\n \x01(\t\x12\x11\n\tlink_code\x18\x05 \x01(\t\x12\x11\n\tlink_name\x18\x06 \x01(\t\x12\x1b\n\x13link_start_chainage\x18\x0b \x01(\x02\x12\x19\n\x11link_end_chainage\x18\x0c \x01(\x02\x12\x13\n\x0blink_length\x18\x07 \x01(\x02\x12\x14\n\x0csurface_type\x18\x08 \x01(\t\x12\x19\n\x11surface_condition\x18\t \x01(\t\x12\x16\n\x0epavement_class\x18\r \x01(\t\x12\x19\n\x11\x63\x61rriageway_width\x18\x0e \x01(\x02\x12\x1b\n\x13\x61\x64ministrative_area\x18\x0f \x01(\t\"$\n\x05Roads\x12\x1b\n\x05roads\x18\x01 \x03(\x0b\x32\x0c.assets.Roadb\x06proto3')
)




_ROAD = _descriptor.Descriptor(
  name='Road',
  full_name='assets.Road',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='assets.Road.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='geojson_id', full_name='assets.Road.geojson_id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='road_code', full_name='assets.Road.road_code', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='road_name', full_name='assets.Road.road_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='road_type', full_name='assets.Road.road_type', index=4,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='link_code', full_name='assets.Road.link_code', index=5,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='link_name', full_name='assets.Road.link_name', index=6,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='link_start_chainage', full_name='assets.Road.link_start_chainage', index=7,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='link_end_chainage', full_name='assets.Road.link_end_chainage', index=8,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='link_length', full_name='assets.Road.link_length', index=9,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='surface_type', full_name='assets.Road.surface_type', index=10,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='surface_condition', full_name='assets.Road.surface_condition', index=11,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pavement_class', full_name='assets.Road.pavement_class', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='carriageway_width', full_name='assets.Road.carriageway_width', index=13,
      number=14, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='administrative_area', full_name='assets.Road.administrative_area', index=14,
      number=15, type=9, cpp_type=9, label=1,
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
  serialized_start=24,
  serialized_end=363,
)


_ROADS = _descriptor.Descriptor(
  name='Roads',
  full_name='assets.Roads',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='roads', full_name='assets.Roads.roads', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=365,
  serialized_end=401,
)

_ROADS.fields_by_name['roads'].message_type = _ROAD
DESCRIPTOR.message_types_by_name['Road'] = _ROAD
DESCRIPTOR.message_types_by_name['Roads'] = _ROADS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Road = _reflection.GeneratedProtocolMessageType('Road', (_message.Message,), {
  'DESCRIPTOR' : _ROAD,
  '__module__' : 'roads_pb2'
  # @@protoc_insertion_point(class_scope:assets.Road)
  })
_sym_db.RegisterMessage(Road)

Roads = _reflection.GeneratedProtocolMessageType('Roads', (_message.Message,), {
  'DESCRIPTOR' : _ROADS,
  '__module__' : 'roads_pb2'
  # @@protoc_insertion_point(class_scope:assets.Roads)
  })
_sym_db.RegisterMessage(Roads)


# @@protoc_insertion_point(module_scope)

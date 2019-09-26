# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: roads.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="roads.proto",
    package="assets",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x0broads.proto\x12\x06\x61ssets""\n\nProjection\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02"\xff\x04\n\x04Road\x12\n\n\x02id\x18\x01 \x01(\r\x12\x12\n\ngeojson_id\x18\x02 \x01(\r\x12\x11\n\troad_code\x18\x03 \x01(\t\x12\x11\n\troad_name\x18\x04 \x01(\t\x12\x11\n\troad_type\x18\n \x01(\t\x12\x13\n\x0broad_status\x18\x14 \x01(\t\x12\x11\n\tlink_code\x18\x05 \x01(\t\x12\x11\n\tlink_name\x18\x06 \x01(\t\x12\x17\n\x0flink_start_name\x18\x10 \x01(\t\x12\x1b\n\x13link_start_chainage\x18\x0b \x01(\x02\x12\x15\n\rlink_end_name\x18\x11 \x01(\t\x12\x19\n\x11link_end_chainage\x18\x0c \x01(\x02\x12\x13\n\x0blink_length\x18\x07 \x01(\x02\x12\x14\n\x0csurface_type\x18\x08 \x01(\t\x12\x19\n\x11surface_condition\x18\t \x01(\t\x12\x16\n\x0epavement_class\x18\r \x01(\t\x12\x19\n\x11\x63\x61rriageway_width\x18\x0e \x01(\x02\x12\x1b\n\x13\x61\x64ministrative_area\x18\x0f \x01(\t\x12\x0f\n\x07project\x18\x12 \x01(\t\x12\x16\n\x0e\x66unding_source\x18\x13 \x01(\t\x12\x17\n\x0ftechnical_class\x18\x15 \x01(\t\x12\x18\n\x10maintenance_need\x18\x16 \x01(\t\x12\x15\n\rtraffic_level\x18\x17 \x01(\t\x12\x18\n\x10last_revision_id\x18\x18 \x01(\r\x12,\n\x10projection_start\x18\x19 \x01(\x0b\x32\x12.assets.Projection\x12*\n\x0eprojection_end\x18\x1a \x01(\x0b\x32\x12.assets.Projection"$\n\x05Roads\x12\x1b\n\x05roads\x18\x01 \x03(\x0b\x32\x0c.assets.Roadb\x06proto3'
    ),
)


_PROJECTION = _descriptor.Descriptor(
    name="Projection",
    full_name="assets.Projection",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="x",
            full_name="assets.Projection.x",
            index=0,
            number=1,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="y",
            full_name="assets.Projection.y",
            index=1,
            number=2,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=23,
    serialized_end=57,
)


_ROAD = _descriptor.Descriptor(
    name="Road",
    full_name="assets.Road",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="assets.Road.id",
            index=0,
            number=1,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="geojson_id",
            full_name="assets.Road.geojson_id",
            index=1,
            number=2,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="road_code",
            full_name="assets.Road.road_code",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="road_name",
            full_name="assets.Road.road_name",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="road_type",
            full_name="assets.Road.road_type",
            index=4,
            number=10,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="road_status",
            full_name="assets.Road.road_status",
            index=5,
            number=20,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="link_code",
            full_name="assets.Road.link_code",
            index=6,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="link_name",
            full_name="assets.Road.link_name",
            index=7,
            number=6,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="link_start_name",
            full_name="assets.Road.link_start_name",
            index=8,
            number=16,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="link_start_chainage",
            full_name="assets.Road.link_start_chainage",
            index=9,
            number=11,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="link_end_name",
            full_name="assets.Road.link_end_name",
            index=10,
            number=17,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="link_end_chainage",
            full_name="assets.Road.link_end_chainage",
            index=11,
            number=12,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="link_length",
            full_name="assets.Road.link_length",
            index=12,
            number=7,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="surface_type",
            full_name="assets.Road.surface_type",
            index=13,
            number=8,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="surface_condition",
            full_name="assets.Road.surface_condition",
            index=14,
            number=9,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="pavement_class",
            full_name="assets.Road.pavement_class",
            index=15,
            number=13,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="carriageway_width",
            full_name="assets.Road.carriageway_width",
            index=16,
            number=14,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="administrative_area",
            full_name="assets.Road.administrative_area",
            index=17,
            number=15,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="project",
            full_name="assets.Road.project",
            index=18,
            number=18,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="funding_source",
            full_name="assets.Road.funding_source",
            index=19,
            number=19,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="technical_class",
            full_name="assets.Road.technical_class",
            index=20,
            number=21,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="maintenance_need",
            full_name="assets.Road.maintenance_need",
            index=21,
            number=22,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="traffic_level",
            full_name="assets.Road.traffic_level",
            index=22,
            number=23,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="last_revision_id",
            full_name="assets.Road.last_revision_id",
            index=23,
            number=24,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="projection_start",
            full_name="assets.Road.projection_start",
            index=24,
            number=25,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="projection_end",
            full_name="assets.Road.projection_end",
            index=25,
            number=26,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=60,
    serialized_end=699,
)


_ROADS = _descriptor.Descriptor(
    name="Roads",
    full_name="assets.Roads",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="roads",
            full_name="assets.Roads.roads",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=701,
    serialized_end=737,
)

_ROAD.fields_by_name["projection_start"].message_type = _PROJECTION
_ROAD.fields_by_name["projection_end"].message_type = _PROJECTION
_ROADS.fields_by_name["roads"].message_type = _ROAD
DESCRIPTOR.message_types_by_name["Projection"] = _PROJECTION
DESCRIPTOR.message_types_by_name["Road"] = _ROAD
DESCRIPTOR.message_types_by_name["Roads"] = _ROADS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Projection = _reflection.GeneratedProtocolMessageType(
    "Projection",
    (_message.Message,),
    {
        "DESCRIPTOR": _PROJECTION,
        "__module__": "roads_pb2"
        # @@protoc_insertion_point(class_scope:assets.Projection)
    },
)
_sym_db.RegisterMessage(Projection)

Road = _reflection.GeneratedProtocolMessageType(
    "Road",
    (_message.Message,),
    {
        "DESCRIPTOR": _ROAD,
        "__module__": "roads_pb2"
        # @@protoc_insertion_point(class_scope:assets.Road)
    },
)
_sym_db.RegisterMessage(Road)

Roads = _reflection.GeneratedProtocolMessageType(
    "Roads",
    (_message.Message,),
    {
        "DESCRIPTOR": _ROADS,
        "__module__": "roads_pb2"
        # @@protoc_insertion_point(class_scope:assets.Roads)
    },
)
_sym_db.RegisterMessage(Roads)


# @@protoc_insertion_point(module_scope)

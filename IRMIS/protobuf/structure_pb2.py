# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: structure.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="structure.proto",
    package="assets",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x0fstructure.proto\x12\x06\x61ssets\x1a\x1fgoogle/protobuf/timestamp.proto"P\n\nStructures\x12\x1f\n\x07\x62ridges\x18\x01 \x03(\x0b\x32\x0e.assets.Bridge\x12!\n\x08\x63ulverts\x18\x02 \x03(\x0b\x32\x0f.assets.Culvert"\xf4\x03\n\x06\x42ridge\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07road_id\x18\x02 \x01(\r\x12\x30\n\x0c\x64\x61te_created\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rlast_modified\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x0estructure_code\x18\x05 \x01(\t\x12\x16\n\x0estructure_name\x18\x06 \x01(\t\x12\x17\n\x0fstructure_class\x18\x07 \x01(\t\x12\x1b\n\x13\x61\x64ministrative_area\x18\x08 \x01(\t\x12\x11\n\troad_code\x18\t \x01(\t\x12\x19\n\x11\x63onstruction_year\x18\n \x01(\x05\x12\x0e\n\x06length\x18\x0b \x01(\x02\x12\r\n\x05width\x18\x0c \x01(\x02\x12\x10\n\x08\x63hainage\x18\r \x01(\x02\x12\x16\n\x0estructure_type\x18\x0e \x01(\t\x12\x10\n\x08material\x18\x0f \x01(\t\x12\x1b\n\x13protection_upstream\x18\x1a \x01(\t\x12\x1d\n\x15protection_downstream\x18\x1b \x01(\t\x12\x12\n\nriver_name\x18\x1c \x01(\t\x12\x14\n\x0cnumber_spans\x18\x1d \x01(\x05\x12\x13\n\x0bspan_length\x18\x1e \x01(\x02"\xdc\x03\n\x07\x43ulvert\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07road_id\x18\x02 \x01(\r\x12\x30\n\x0c\x64\x61te_created\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rlast_modified\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x0estructure_code\x18\x05 \x01(\t\x12\x16\n\x0estructure_name\x18\x06 \x01(\t\x12\x17\n\x0fstructure_class\x18\x07 \x01(\t\x12\x1b\n\x13\x61\x64ministrative_area\x18\x08 \x01(\t\x12\x11\n\troad_code\x18\t \x01(\t\x12\x19\n\x11\x63onstruction_year\x18\n \x01(\x05\x12\x0e\n\x06length\x18\x0b \x01(\x02\x12\r\n\x05width\x18\x0c \x01(\x02\x12\x10\n\x08\x63hainage\x18\r \x01(\x02\x12\x16\n\x0estructure_type\x18\x0e \x01(\t\x12\x10\n\x08material\x18\x0f \x01(\t\x12\x1b\n\x13protection_upstream\x18\x1a \x01(\t\x12\x1d\n\x15protection_downstream\x18\x1b \x01(\t\x12\x0e\n\x06height\x18\x1c \x01(\x02\x12\x14\n\x0cnumber_cells\x18\x1d \x01(\x05\x62\x06proto3'
    ),
    dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,],
)


_STRUCTURES = _descriptor.Descriptor(
    name="Structures",
    full_name="assets.Structures",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="bridges",
            full_name="assets.Structures.bridges",
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
        ),
        _descriptor.FieldDescriptor(
            name="culverts",
            full_name="assets.Structures.culverts",
            index=1,
            number=2,
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
    serialized_end=140,
)


_BRIDGE = _descriptor.Descriptor(
    name="Bridge",
    full_name="assets.Bridge",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="assets.Bridge.id",
            index=0,
            number=1,
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
            name="road_id",
            full_name="assets.Bridge.road_id",
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
            name="date_created",
            full_name="assets.Bridge.date_created",
            index=2,
            number=3,
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
            name="last_modified",
            full_name="assets.Bridge.last_modified",
            index=3,
            number=4,
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
            name="structure_code",
            full_name="assets.Bridge.structure_code",
            index=4,
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
            name="structure_name",
            full_name="assets.Bridge.structure_name",
            index=5,
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
            name="structure_class",
            full_name="assets.Bridge.structure_class",
            index=6,
            number=7,
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
            name="administrative_area",
            full_name="assets.Bridge.administrative_area",
            index=7,
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
            name="road_code",
            full_name="assets.Bridge.road_code",
            index=8,
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
            name="construction_year",
            full_name="assets.Bridge.construction_year",
            index=9,
            number=10,
            type=5,
            cpp_type=1,
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
            name="length",
            full_name="assets.Bridge.length",
            index=10,
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
            name="width",
            full_name="assets.Bridge.width",
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
            name="chainage",
            full_name="assets.Bridge.chainage",
            index=12,
            number=13,
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
            name="structure_type",
            full_name="assets.Bridge.structure_type",
            index=13,
            number=14,
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
            name="material",
            full_name="assets.Bridge.material",
            index=14,
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
            name="protection_upstream",
            full_name="assets.Bridge.protection_upstream",
            index=15,
            number=26,
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
            name="protection_downstream",
            full_name="assets.Bridge.protection_downstream",
            index=16,
            number=27,
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
            name="river_name",
            full_name="assets.Bridge.river_name",
            index=17,
            number=28,
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
            name="number_spans",
            full_name="assets.Bridge.number_spans",
            index=18,
            number=29,
            type=5,
            cpp_type=1,
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
            name="span_length",
            full_name="assets.Bridge.span_length",
            index=19,
            number=30,
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
    serialized_start=143,
    serialized_end=643,
)


_CULVERT = _descriptor.Descriptor(
    name="Culvert",
    full_name="assets.Culvert",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="assets.Culvert.id",
            index=0,
            number=1,
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
            name="road_id",
            full_name="assets.Culvert.road_id",
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
            name="date_created",
            full_name="assets.Culvert.date_created",
            index=2,
            number=3,
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
            name="last_modified",
            full_name="assets.Culvert.last_modified",
            index=3,
            number=4,
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
            name="structure_code",
            full_name="assets.Culvert.structure_code",
            index=4,
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
            name="structure_name",
            full_name="assets.Culvert.structure_name",
            index=5,
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
            name="structure_class",
            full_name="assets.Culvert.structure_class",
            index=6,
            number=7,
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
            name="administrative_area",
            full_name="assets.Culvert.administrative_area",
            index=7,
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
            name="road_code",
            full_name="assets.Culvert.road_code",
            index=8,
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
            name="construction_year",
            full_name="assets.Culvert.construction_year",
            index=9,
            number=10,
            type=5,
            cpp_type=1,
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
            name="length",
            full_name="assets.Culvert.length",
            index=10,
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
            name="width",
            full_name="assets.Culvert.width",
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
            name="chainage",
            full_name="assets.Culvert.chainage",
            index=12,
            number=13,
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
            name="structure_type",
            full_name="assets.Culvert.structure_type",
            index=13,
            number=14,
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
            name="material",
            full_name="assets.Culvert.material",
            index=14,
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
            name="protection_upstream",
            full_name="assets.Culvert.protection_upstream",
            index=15,
            number=26,
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
            name="protection_downstream",
            full_name="assets.Culvert.protection_downstream",
            index=16,
            number=27,
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
            name="height",
            full_name="assets.Culvert.height",
            index=17,
            number=28,
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
            name="number_cells",
            full_name="assets.Culvert.number_cells",
            index=18,
            number=29,
            type=5,
            cpp_type=1,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=646,
    serialized_end=1122,
)

_STRUCTURES.fields_by_name["bridges"].message_type = _BRIDGE
_STRUCTURES.fields_by_name["culverts"].message_type = _CULVERT
_BRIDGE.fields_by_name[
    "date_created"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_BRIDGE.fields_by_name[
    "last_modified"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CULVERT.fields_by_name[
    "date_created"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CULVERT.fields_by_name[
    "last_modified"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name["Structures"] = _STRUCTURES
DESCRIPTOR.message_types_by_name["Bridge"] = _BRIDGE
DESCRIPTOR.message_types_by_name["Culvert"] = _CULVERT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Structures = _reflection.GeneratedProtocolMessageType(
    "Structures",
    (_message.Message,),
    {
        "DESCRIPTOR": _STRUCTURES,
        "__module__": "structure_pb2"
        # @@protoc_insertion_point(class_scope:assets.Structures)
    },
)
_sym_db.RegisterMessage(Structures)

Bridge = _reflection.GeneratedProtocolMessageType(
    "Bridge",
    (_message.Message,),
    {
        "DESCRIPTOR": _BRIDGE,
        "__module__": "structure_pb2"
        # @@protoc_insertion_point(class_scope:assets.Bridge)
    },
)
_sym_db.RegisterMessage(Bridge)

Culvert = _reflection.GeneratedProtocolMessageType(
    "Culvert",
    (_message.Message,),
    {
        "DESCRIPTOR": _CULVERT,
        "__module__": "structure_pb2"
        # @@protoc_insertion_point(class_scope:assets.Culvert)
    },
)
_sym_db.RegisterMessage(Culvert)


# @@protoc_insertion_point(module_scope)

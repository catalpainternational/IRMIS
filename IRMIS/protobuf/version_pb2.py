# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: version.proto

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
    name="version.proto",
    package="assets",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\rversion.proto\x12\x06\x61ssets\x1a\x1fgoogle/protobuf/timestamp.proto"f\n\x07Version\x12\n\n\x02pk\x18\x01 \x01(\r\x12\x30\n\x0c\x64\x61te_created\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04user\x18\x03 \x01(\t\x12\x0f\n\x07\x63omment\x18\x04 \x01(\t"-\n\x08Versions\x12!\n\x08versions\x18\x01 \x03(\x0b\x32\x0f.assets.Versionb\x06proto3'
    ),
    dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,],
)


_VERSION = _descriptor.Descriptor(
    name="Version",
    full_name="assets.Version",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="pk",
            full_name="assets.Version.pk",
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
            name="date_created",
            full_name="assets.Version.date_created",
            index=1,
            number=2,
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
            name="user",
            full_name="assets.Version.user",
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
            name="comment",
            full_name="assets.Version.comment",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=58,
    serialized_end=160,
)


_VERSIONS = _descriptor.Descriptor(
    name="Versions",
    full_name="assets.Versions",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="versions",
            full_name="assets.Versions.versions",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=162,
    serialized_end=207,
)

_VERSION.fields_by_name[
    "date_created"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_VERSIONS.fields_by_name["versions"].message_type = _VERSION
DESCRIPTOR.message_types_by_name["Version"] = _VERSION
DESCRIPTOR.message_types_by_name["Versions"] = _VERSIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Version = _reflection.GeneratedProtocolMessageType(
    "Version",
    (_message.Message,),
    dict(
        DESCRIPTOR=_VERSION,
        __module__="version_pb2"
        # @@protoc_insertion_point(class_scope:assets.Version)
    ),
)
_sym_db.RegisterMessage(Version)

Versions = _reflection.GeneratedProtocolMessageType(
    "Versions",
    (_message.Message,),
    dict(
        DESCRIPTOR=_VERSIONS,
        __module__="version_pb2"
        # @@protoc_insertion_point(class_scope:assets.Versions)
    ),
)
_sym_db.RegisterMessage(Versions)


# @@protoc_insertion_point(module_scope)

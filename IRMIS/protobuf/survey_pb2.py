# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: survey.proto

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
    name="survey.proto",
    package="assets",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x0csurvey.proto\x12\x06\x61ssets\x1a\x1fgoogle/protobuf/timestamp.proto"\xfd\x01\n\x06Survey\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04road\x18\x02 \x01(\t\x12\x0c\n\x04user\x18\x03 \x01(\r\x12\x0e\n\x06source\x18\t \x01(\t\x12\x30\n\x0c\x64\x61te_updated\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rdate_surveyed\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x0e\x63hainage_start\x18\x05 \x01(\x02\x12\x14\n\x0c\x63hainage_end\x18\x06 \x01(\x02\x12\x0e\n\x06values\x18\x07 \x01(\t\x12\x18\n\x10last_revision_id\x18\n \x01(\r"*\n\x07Surveys\x12\x1f\n\x07surveys\x18\x01 \x03(\x0b\x32\x0e.assets.Surveyb\x06proto3'
    ),
    dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR],
)


_SURVEY = _descriptor.Descriptor(
    name="Survey",
    full_name="assets.Survey",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="assets.Survey.id",
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
            name="road",
            full_name="assets.Survey.road",
            index=1,
            number=2,
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
            name="user",
            full_name="assets.Survey.user",
            index=2,
            number=3,
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
            name="source",
            full_name="assets.Survey.source",
            index=3,
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
            name="date_updated",
            full_name="assets.Survey.date_updated",
            index=4,
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
            name="date_surveyed",
            full_name="assets.Survey.date_surveyed",
            index=5,
            number=8,
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
            name="chainage_start",
            full_name="assets.Survey.chainage_start",
            index=6,
            number=5,
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
            name="chainage_end",
            full_name="assets.Survey.chainage_end",
            index=7,
            number=6,
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
            name="values",
            full_name="assets.Survey.values",
            index=8,
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
            name="last_revision_id",
            full_name="assets.Survey.last_revision_id",
            index=9,
            number=10,
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
    serialized_end=311,
)


_SURVEYS = _descriptor.Descriptor(
    name="Surveys",
    full_name="assets.Surveys",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="surveys",
            full_name="assets.Surveys.surveys",
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
    serialized_start=313,
    serialized_end=355,
)

_SURVEY.fields_by_name[
    "date_updated"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_SURVEY.fields_by_name[
    "date_surveyed"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_SURVEYS.fields_by_name["surveys"].message_type = _SURVEY
DESCRIPTOR.message_types_by_name["Survey"] = _SURVEY
DESCRIPTOR.message_types_by_name["Surveys"] = _SURVEYS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Survey = _reflection.GeneratedProtocolMessageType(
    "Survey",
    (_message.Message,),
    {
        "DESCRIPTOR": _SURVEY,
        "__module__": "survey_pb2"
        # @@protoc_insertion_point(class_scope:assets.Survey)
    },
)
_sym_db.RegisterMessage(Survey)

Surveys = _reflection.GeneratedProtocolMessageType(
    "Surveys",
    (_message.Message,),
    {
        "DESCRIPTOR": _SURVEYS,
        "__module__": "survey_pb2"
        # @@protoc_insertion_point(class_scope:assets.Surveys)
    },
)
_sym_db.RegisterMessage(Surveys)


# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: plan.proto

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
    name="plan.proto",
    package="assets",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\nplan.proto\x12\x06\x61ssets\x1a\x1fgoogle/protobuf/timestamp.proto"z\n\x08Snapshot\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04year\x18\x02 \x01(\r\x12\x0e\n\x06\x62udget\x18\x03 \x01(\x02\x12\x0e\n\x06length\x18\x04 \x01(\x02\x12\x13\n\x0b\x61sset_class\x18\x05 \x01(\t\x12\x11\n\twork_type\x18\x06 \x01(\t\x12\x0c\n\x04plan\x18\x07 \x01(\r"\xb7\x02\n\x04Plan\x12\n\n\x02id\x18\x01 \x01(\r\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0c\n\x04\x66ile\x18\x03 \x01(\x0c\x12\x0c\n\x04user\x18\x04 \x01(\r\x12\x10\n\x08\x61\x64\x64\x65\x64_by\x18\x05 \x01(\t\x12\x31\n\rlast_modified\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0c\x64\x61te_created\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08\x61pproved\x18\x08 \x01(\x08\x12\x13\n\x0b\x61sset_class\x18\t \x01(\t\x12!\n\x07summary\x18\n \x03(\x0b\x32\x10.assets.Snapshot\x12\x0b\n\x03url\x18\x0b \x01(\t\x12\x11\n\tfile_name\x18\x0c \x01(\t\x12\x17\n\x0fplanning_period\x18\r \x01(\t"$\n\x05Plans\x12\x1b\n\x05plans\x18\x01 \x03(\x0b\x32\x0c.assets.Plan"4\n\rPlanSnapshots\x12#\n\tsnapshots\x18\x01 \x03(\x0b\x32\x10.assets.Snapshotb\x06proto3'
    ),
    dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,],
)


_SNAPSHOT = _descriptor.Descriptor(
    name="Snapshot",
    full_name="assets.Snapshot",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="assets.Snapshot.id",
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
            name="year",
            full_name="assets.Snapshot.year",
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
            name="budget",
            full_name="assets.Snapshot.budget",
            index=2,
            number=3,
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
            name="length",
            full_name="assets.Snapshot.length",
            index=3,
            number=4,
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
            name="asset_class",
            full_name="assets.Snapshot.asset_class",
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
            name="work_type",
            full_name="assets.Snapshot.work_type",
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
            name="plan",
            full_name="assets.Snapshot.plan",
            index=6,
            number=7,
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
    serialized_start=55,
    serialized_end=177,
)


_PLAN = _descriptor.Descriptor(
    name="Plan",
    full_name="assets.Plan",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="assets.Plan.id",
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
            name="title",
            full_name="assets.Plan.title",
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
            name="file",
            full_name="assets.Plan.file",
            index=2,
            number=3,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
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
            full_name="assets.Plan.user",
            index=3,
            number=4,
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
            name="added_by",
            full_name="assets.Plan.added_by",
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
            name="last_modified",
            full_name="assets.Plan.last_modified",
            index=5,
            number=6,
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
            name="date_created",
            full_name="assets.Plan.date_created",
            index=6,
            number=7,
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
            name="approved",
            full_name="assets.Plan.approved",
            index=7,
            number=8,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="asset_class",
            full_name="assets.Plan.asset_class",
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
            name="summary",
            full_name="assets.Plan.summary",
            index=9,
            number=10,
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
            name="url",
            full_name="assets.Plan.url",
            index=10,
            number=11,
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
            name="file_name",
            full_name="assets.Plan.file_name",
            index=11,
            number=12,
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
            name="planning_period",
            full_name="assets.Plan.planning_period",
            index=12,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=180,
    serialized_end=491,
)


_PLANS = _descriptor.Descriptor(
    name="Plans",
    full_name="assets.Plans",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="plans",
            full_name="assets.Plans.plans",
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
    serialized_start=493,
    serialized_end=529,
)


_PLANSNAPSHOTS = _descriptor.Descriptor(
    name="PlanSnapshots",
    full_name="assets.PlanSnapshots",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="snapshots",
            full_name="assets.PlanSnapshots.snapshots",
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
    serialized_start=531,
    serialized_end=583,
)

_PLAN.fields_by_name[
    "last_modified"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_PLAN.fields_by_name[
    "date_created"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_PLAN.fields_by_name["summary"].message_type = _SNAPSHOT
_PLANS.fields_by_name["plans"].message_type = _PLAN
_PLANSNAPSHOTS.fields_by_name["snapshots"].message_type = _SNAPSHOT
DESCRIPTOR.message_types_by_name["Snapshot"] = _SNAPSHOT
DESCRIPTOR.message_types_by_name["Plan"] = _PLAN
DESCRIPTOR.message_types_by_name["Plans"] = _PLANS
DESCRIPTOR.message_types_by_name["PlanSnapshots"] = _PLANSNAPSHOTS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Snapshot = _reflection.GeneratedProtocolMessageType(
    "Snapshot",
    (_message.Message,),
    dict(
        DESCRIPTOR=_SNAPSHOT,
        __module__="plan_pb2"
        # @@protoc_insertion_point(class_scope:assets.Snapshot)
    ),
)
_sym_db.RegisterMessage(Snapshot)

Plan = _reflection.GeneratedProtocolMessageType(
    "Plan",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PLAN,
        __module__="plan_pb2"
        # @@protoc_insertion_point(class_scope:assets.Plan)
    ),
)
_sym_db.RegisterMessage(Plan)

Plans = _reflection.GeneratedProtocolMessageType(
    "Plans",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PLANS,
        __module__="plan_pb2"
        # @@protoc_insertion_point(class_scope:assets.Plans)
    ),
)
_sym_db.RegisterMessage(Plans)

PlanSnapshots = _reflection.GeneratedProtocolMessageType(
    "PlanSnapshots",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PLANSNAPSHOTS,
        __module__="plan_pb2"
        # @@protoc_insertion_point(class_scope:assets.PlanSnapshots)
    ),
)
_sym_db.RegisterMessage(PlanSnapshots)


# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: photo.proto

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
    name="photo.proto",
    package="assets",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x0bphoto.proto\x12\x06\x61ssets\x1a\x1fgoogle/protobuf/timestamp.proto"\'\n\x06Photos\x12\x1d\n\x06photos\x18\x01 \x03(\x0b\x32\r.assets.Photo"\xab\x01\n\x05Photo\x12\n\n\x02id\x18\x01 \x01(\r\x12\x30\n\x0c\x64\x61te_created\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rlast_modified\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0b\n\x03url\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x0f\n\x07\x66k_link\x18\x06 \x01(\tb\x06proto3'
    ),
    dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,],
)


_PHOTOS = _descriptor.Descriptor(
    name="Photos",
    full_name="assets.Photos",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="photos",
            full_name="assets.Photos.photos",
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
    serialized_start=56,
    serialized_end=95,
)


_PHOTO = _descriptor.Descriptor(
    name="Photo",
    full_name="assets.Photo",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="assets.Photo.id",
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
            full_name="assets.Photo.date_created",
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
            name="last_modified",
            full_name="assets.Photo.last_modified",
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
            name="url",
            full_name="assets.Photo.url",
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
            name="description",
            full_name="assets.Photo.description",
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
            name="fk_link",
            full_name="assets.Photo.fk_link",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=98,
    serialized_end=269,
)

_PHOTOS.fields_by_name["photos"].message_type = _PHOTO
_PHOTO.fields_by_name[
    "date_created"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_PHOTO.fields_by_name[
    "last_modified"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name["Photos"] = _PHOTOS
DESCRIPTOR.message_types_by_name["Photo"] = _PHOTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Photos = _reflection.GeneratedProtocolMessageType(
    "Photos",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PHOTOS,
        __module__="photo_pb2"
        # @@protoc_insertion_point(class_scope:assets.Photos)
    ),
)
_sym_db.RegisterMessage(Photos)

Photo = _reflection.GeneratedProtocolMessageType(
    "Photo",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PHOTO,
        __module__="photo_pb2"
        # @@protoc_insertion_point(class_scope:assets.Photo)
    ),
)
_sym_db.RegisterMessage(Photo)


# @@protoc_insertion_point(module_scope)

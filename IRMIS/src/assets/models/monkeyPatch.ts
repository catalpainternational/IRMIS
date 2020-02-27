// The protobuf method `jspb.Message.getWrapperField` is used to return nested Messages
// It is currently returning the data of the Message (in the correct 'shape')
// but not the actual Message itself.
// This means that functions like `serializeBinaryToWriter` will fail.

// All protobuf monkey patching goes into this file.

// We've found this problem as far back as protoc v3.7
// Please review everytime the protoc gets updated
// and delete this file if no longer required

import * as jspb from "google-protobuf";

// The affected 'nested' Messages
import { Timestamp } from "google-protobuf/google/protobuf/timestamp_pb";
import { Projection } from "../../../protobuf/roads_pb";
import { Point } from "../../../protobuf/structure_pb";

/**
 * Serializes the given Message data (not the Message object)
 * to binary data (in protobuf wire format), writing to the given BinaryWriter.
 * @param {!google_protobuf_timestamp_pb.Timestamp} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
function serializeTimestampBinaryToWriter(message: Timestamp | any, writer: jspb.BinaryWriter): void {
    let n: number | undefined;
    n = message.getSeconds ? message.getSeconds() : message.array[0];
    if (n !== 0) {
        writer.writeInt64(1, n);
    }
    n = message.getNanos ? message.getNanos() : message.array[1];
    if (n !== 0) {
        writer.writeInt32(2, n);
    }
}

/**
 * Serializes the given Message data (not the Message object)
 * to binary data (in protobuf wire format), writing to the given BinaryWriter.
 * @param {!proto.assets.Point} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
function serializePointBinaryToWriter(message: Point | any, writer: jspb.BinaryWriter): void {
    let f: number | undefined;
    f = message.getX ? message.getX() : message.array[0];
    if (f !== 0.0) {
        writer.writeFloat(1, f);
    }
    f = message.getY ? message.getY() : message.array[1];
    if (f !== 0.0) {
        writer.writeFloat(2, f);
    }
}

/**
 * Serializes the given Message data (not the Message object)
 * to binary data (in protobuf wire format), writing to the given BinaryWriter.
 * @param {!proto.assets.Projection} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
function serializeProjectionBinaryToWriter(message: Projection | any, writer: jspb.BinaryWriter): void {
    let f: number | undefined;
    f = message.getX ? message.getX() : message.array[0];
    if (f !== 0.0) {
        writer.writeFloat(1, f);
    }
    f = message.getY ? message.getY() : message.array[1];
    if (f !== 0.0) {
        writer.writeFloat(2, f);
    }
}

// Here's the actual monkey-patches
(window as any).proto.google.protobuf.Timestamp.serializeBinaryToWriter = serializeTimestampBinaryToWriter;
(window as any).proto.assets.Point.serializeBinaryToWriter = serializePointBinaryToWriter;
(window as any).proto.assets.Projection.serializeBinaryToWriter = serializeProjectionBinaryToWriter;

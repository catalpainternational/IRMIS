// package: assets
// file: version.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Version extends jspb.Message {
  getPk(): number;
  setPk(value: number): void;

  hasDateCreated(): boolean;
  clearDateCreated(): void;
  getDateCreated(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateCreated(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getUser(): string;
  setUser(value: string): void;

  getComment(): string;
  setComment(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Version.AsObject;
  static toObject(includeInstance: boolean, msg: Version): Version.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Version, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Version;
  static deserializeBinaryFromReader(message: Version, reader: jspb.BinaryReader): Version;
}

export namespace Version {
  export type AsObject = {
    pk: number,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    user: string,
    comment: string,
  }
}

export class Versions extends jspb.Message {
  clearVersionsList(): void;
  getVersionsList(): Array<Version>;
  setVersionsList(value: Array<Version>): void;
  addVersions(value?: Version, index?: number): Version;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Versions.AsObject;
  static toObject(includeInstance: boolean, msg: Versions): Versions.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Versions, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Versions;
  static deserializeBinaryFromReader(message: Versions, reader: jspb.BinaryReader): Versions;
}

export namespace Versions {
  export type AsObject = {
    versionsList: Array<Version.AsObject>,
  }
}


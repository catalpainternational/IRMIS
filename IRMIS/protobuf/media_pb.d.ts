// package: assets
// file: media.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Medias extends jspb.Message {
  clearMediasList(): void;
  getMediasList(): Array<Media>;
  setMediasList(value: Array<Media>): void;
  addMedias(value?: Media, index?: number): Media;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Medias.AsObject;
  static toObject(includeInstance: boolean, msg: Medias): Medias.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Medias, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Medias;
  static deserializeBinaryFromReader(message: Medias, reader: jspb.BinaryReader): Medias;
}

export namespace Medias {
  export type AsObject = {
    mediasList: Array<Media.AsObject>,
  }
}

export class Media extends jspb.Message {
  getId(): number;
  setId(value: number): void;

  hasDateCreated(): boolean;
  clearDateCreated(): void;
  getDateCreated(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateCreated(value?: google_protobuf_timestamp_pb.Timestamp): void;

  hasLastModified(): boolean;
  clearLastModified(): void;
  getLastModified(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setLastModified(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getUrl(): string;
  setUrl(value: string): void;

  getDescription(): string;
  setDescription(value: string): void;

  getFkLink(): string;
  setFkLink(value: string): void;

  getUser(): number;
  setUser(value: number): void;

  getAddedBy(): string;
  setAddedBy(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Media.AsObject;
  static toObject(includeInstance: boolean, msg: Media): Media.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Media, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Media;
  static deserializeBinaryFromReader(message: Media, reader: jspb.BinaryReader): Media;
}

export namespace Media {
  export type AsObject = {
    id: number,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    lastModified?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    url: string,
    description: string,
    fkLink: string,
    user: number,
    addedBy: string,
  }
}


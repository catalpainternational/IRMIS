// package: assets
// file: photo.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Photos extends jspb.Message {
  clearPhotosList(): void;
  getPhotosList(): Array<Photo>;
  setPhotosList(value: Array<Photo>): void;
  addPhotos(value?: Photo, index?: number): Photo;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Photos.AsObject;
  static toObject(includeInstance: boolean, msg: Photos): Photos.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Photos, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Photos;
  static deserializeBinaryFromReader(message: Photos, reader: jspb.BinaryReader): Photos;
}

export namespace Photos {
  export type AsObject = {
    photosList: Array<Photo.AsObject>,
  }
}

export class Photo extends jspb.Message {
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

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Photo.AsObject;
  static toObject(includeInstance: boolean, msg: Photo): Photo.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Photo, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Photo;
  static deserializeBinaryFromReader(message: Photo, reader: jspb.BinaryReader): Photo;
}

export namespace Photo {
  export type AsObject = {
    id: number,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    lastModified?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    url: string,
    description: string,
    fkLink: string,
  }
}


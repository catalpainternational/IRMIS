// package: assets
// file: report.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Report extends jspb.Message {
  getFilter(): string;
  setFilter(value: string): void;

  getLengths(): string;
  setLengths(value: string): void;

  clearAttributesList(): void;
  getAttributesList(): Array<Attribute>;
  setAttributesList(value: Array<Attribute>): void;
  addAttributes(value?: Attribute, index?: number): Attribute;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Report.AsObject;
  static toObject(includeInstance: boolean, msg: Report): Report.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Report, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Report;
  static deserializeBinaryFromReader(message: Report, reader: jspb.BinaryReader): Report;
}

export namespace Report {
  export type AsObject = {
    filter: string,
    lengths: string,
    attributesList: Array<Attribute.AsObject>,
  }
}

export class Attribute extends jspb.Message {
  getRoadId(): number;
  setRoadId(value: number): void;

  getRoadCode(): string;
  setRoadCode(value: string): void;

  getPrimaryAttribute(): string;
  setPrimaryAttribute(value: string): void;

  getChainageStart(): number;
  setChainageStart(value: number): void;

  getChainageEnd(): number;
  setChainageEnd(value: number): void;

  getSurveyId(): number;
  setSurveyId(value: number): void;

  getUserId(): number;
  setUserId(value: number): void;

  hasDateSurveyed(): boolean;
  clearDateSurveyed(): void;
  getDateSurveyed(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateSurveyed(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getAddedBy(): string;
  setAddedBy(value: string): void;

  getValue(): string;
  setValue(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Attribute.AsObject;
  static toObject(includeInstance: boolean, msg: Attribute): Attribute.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Attribute, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Attribute;
  static deserializeBinaryFromReader(message: Attribute, reader: jspb.BinaryReader): Attribute;
}

export namespace Attribute {
  export type AsObject = {
    roadId: number,
    roadCode: string,
    primaryAttribute: string,
    chainageStart: number,
    chainageEnd: number,
    surveyId: number,
    userId: number,
    dateSurveyed?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    addedBy: string,
    value: string,
  }
}


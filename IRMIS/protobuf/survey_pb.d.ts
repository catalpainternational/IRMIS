// package: assets
// file: survey.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Survey extends jspb.Message {
  getId(): number;
  setId(value: number): void;

  getRoadId(): number;
  setRoadId(value: number): void;

  getRoadCode(): string;
  setRoadCode(value: string): void;

  getUser(): number;
  setUser(value: number): void;

  getSource(): string;
  setSource(value: string): void;

  hasDateUpdated(): boolean;
  clearDateUpdated(): void;
  getDateUpdated(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateUpdated(value?: google_protobuf_timestamp_pb.Timestamp): void;

  hasDateSurveyed(): boolean;
  clearDateSurveyed(): void;
  getDateSurveyed(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateSurveyed(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getChainageStart(): number;
  setChainageStart(value: number): void;

  getChainageEnd(): number;
  setChainageEnd(value: number): void;

  getValues(): string;
  setValues(value: string): void;

  getAddedBy(): string;
  setAddedBy(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Survey.AsObject;
  static toObject(includeInstance: boolean, msg: Survey): Survey.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Survey, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Survey;
  static deserializeBinaryFromReader(message: Survey, reader: jspb.BinaryReader): Survey;
}

export namespace Survey {
  export type AsObject = {
    id: number,
    roadId: number,
    roadCode: string,
    user: number,
    source: string,
    dateUpdated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    dateSurveyed?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    chainageStart: number,
    chainageEnd: number,
    values: string,
    addedBy: string,
  }
}

export class Surveys extends jspb.Message {
  clearSurveysList(): void;
  getSurveysList(): Array<Survey>;
  setSurveysList(value: Array<Survey>): void;
  addSurveys(value?: Survey, index?: number): Survey;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Surveys.AsObject;
  static toObject(includeInstance: boolean, msg: Surveys): Surveys.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Surveys, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Surveys;
  static deserializeBinaryFromReader(message: Surveys, reader: jspb.BinaryReader): Surveys;
}

export namespace Surveys {
  export type AsObject = {
    surveysList: Array<Survey.AsObject>,
  }
}


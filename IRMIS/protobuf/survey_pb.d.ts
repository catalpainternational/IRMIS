// package: assets
// file: survey.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Survey extends jspb.Message {
  getId(): number;
  setId(value: number): void;

  getRoad(): string;
  setRoad(value: string): void;

  getUser(): number;
  setUser(value: number): void;

  hasDateUpdated(): boolean;
  clearDateUpdated(): void;
  getDateUpdated(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateUpdated(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getChainageStart(): number;
  setChainageStart(value: number): void;

  getChainageEnd(): number;
  setChainageEnd(value: number): void;

  getValuesMap(): jspb.Map<string, string>;
  clearValuesMap(): void;
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
    road: string,
    user: number,
    dateUpdated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    chainageStart: number,
    chainageEnd: number,
    valuesMap: Array<[string, string]>,
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


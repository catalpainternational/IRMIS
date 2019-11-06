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

  getLastRevisionId(): number;
  setLastRevisionId(value: number): void;

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
    road: string,
    user: number,
    source: string,
    dateUpdated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    dateSurveyed?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    chainageStart: number,
    chainageEnd: number,
    values: string,
    lastRevisionId: number,
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

export class Report extends jspb.Message {
  getRoadCode(): string;
  setRoadCode(value: string): void;

  getReportChainageStart(): number;
  setReportChainageStart(value: number): void;

  getReportChainageEnd(): number;
  setReportChainageEnd(value: number): void;

  getCounts(): string;
  setCounts(value: string): void;

  getPercentages(): string;
  setPercentages(value: string): void;

  clearTableList(): void;
  getTableList(): Array<TableEntry>;
  setTableList(value: Array<TableEntry>): void;
  addTable(value?: TableEntry, index?: number): TableEntry;

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
    roadCode: string,
    reportChainageStart: number,
    reportChainageEnd: number,
    counts: string,
    percentages: string,
    tableList: Array<TableEntry.AsObject>,
  }
}

export class TableEntry extends jspb.Message {
  getChainageStart(): number;
  setChainageStart(value: number): void;

  getChainageEnd(): number;
  setChainageEnd(value: number): void;

  getValues(): string;
  setValues(value: string): void;

  getSurveyId(): number;
  setSurveyId(value: number): void;

  hasDateSurveyed(): boolean;
  clearDateSurveyed(): void;
  getDateSurveyed(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateSurveyed(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getAddedBy(): string;
  setAddedBy(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): TableEntry.AsObject;
  static toObject(includeInstance: boolean, msg: TableEntry): TableEntry.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: TableEntry, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): TableEntry;
  static deserializeBinaryFromReader(message: TableEntry, reader: jspb.BinaryReader): TableEntry;
}

export namespace TableEntry {
  export type AsObject = {
    chainageStart: number,
    chainageEnd: number,
    values: string,
    surveyId: number,
    dateSurveyed?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    addedBy: string,
  }
}


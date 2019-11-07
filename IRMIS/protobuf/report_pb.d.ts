// package: assets
// file: report.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Report extends jspb.Message {
  getFilter(): string;
  setFilter(value: string): void;

  getCounts(): string;
  setCounts(value: string): void;

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
    filter: string,
    counts: string,
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


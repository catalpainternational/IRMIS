// package: assets
// file: report.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Report extends jspb.Message {
  getFilter(): string;
  setFilter(value: string): void;

  getLengths(): string;
  setLengths(value: string): void;

  clearAttributeTablesList(): void;
  getAttributeTablesList(): Array<AttributeTable>;
  setAttributeTablesList(value: Array<AttributeTable>): void;
  addAttributeTables(value?: AttributeTable, index?: number): AttributeTable;

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
    attributeTablesList: Array<AttributeTable.AsObject>,
  }
}

export class AttributeTable extends jspb.Message {
  getPrimaryAttribute(): string;
  setPrimaryAttribute(value: string): void;

  clearSecondaryAttributeList(): void;
  getSecondaryAttributeList(): Array<string>;
  setSecondaryAttributeList(value: Array<string>): void;
  addSecondaryAttribute(value: string, index?: number): string;

  clearAttributeEntriesList(): void;
  getAttributeEntriesList(): Array<AttributeEntry>;
  setAttributeEntriesList(value: Array<AttributeEntry>): void;
  addAttributeEntries(value?: AttributeEntry, index?: number): AttributeEntry;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): AttributeTable.AsObject;
  static toObject(includeInstance: boolean, msg: AttributeTable): AttributeTable.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: AttributeTable, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): AttributeTable;
  static deserializeBinaryFromReader(message: AttributeTable, reader: jspb.BinaryReader): AttributeTable;
}

export namespace AttributeTable {
  export type AsObject = {
    primaryAttribute: string,
    secondaryAttributeList: Array<string>,
    attributeEntriesList: Array<AttributeEntry.AsObject>,
  }
}

export class AttributeEntry extends jspb.Message {
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

  getPrimaryAttribute(): string;
  setPrimaryAttribute(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): AttributeEntry.AsObject;
  static toObject(includeInstance: boolean, msg: AttributeEntry): AttributeEntry.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: AttributeEntry, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): AttributeEntry;
  static deserializeBinaryFromReader(message: AttributeEntry, reader: jspb.BinaryReader): AttributeEntry;
}

export namespace AttributeEntry {
  export type AsObject = {
    chainageStart: number,
    chainageEnd: number,
    values: string,
    surveyId: number,
    dateSurveyed?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    addedBy: string,
    primaryAttribute: string,
  }
}


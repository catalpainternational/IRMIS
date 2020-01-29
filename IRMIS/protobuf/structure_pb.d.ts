// package: assets
// file: structure.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Bridge extends jspb.Message {
  getId(): number;
  setId(value: number): void;

  getRoadId(): number;
  setRoadId(value: number): void;

  hasDateCreated(): boolean;
  clearDateCreated(): void;
  getDateCreated(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateCreated(value?: google_protobuf_timestamp_pb.Timestamp): void;

  hasLastModified(): boolean;
  clearLastModified(): void;
  getLastModified(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setLastModified(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getStructureCode(): string;
  setStructureCode(value: string): void;

  getStructureName(): string;
  setStructureName(value: string): void;

  getStructureClass(): string;
  setStructureClass(value: string): void;

  getAdministrativeArea(): string;
  setAdministrativeArea(value: string): void;

  getRoadCode(): string;
  setRoadCode(value: string): void;

  getConstructionYear(): number;
  setConstructionYear(value: number): void;

  getLength(): number;
  setLength(value: number): void;

  getWidth(): number;
  setWidth(value: number): void;

  getChainage(): number;
  setChainage(value: number): void;

  getStructureType(): string;
  setStructureType(value: string): void;

  getRiverName(): string;
  setRiverName(value: string): void;

  getNumberSpans(): number;
  setNumberSpans(value: number): void;

  getSpanLength(): number;
  setSpanLength(value: number): void;

  getMaterial(): string;
  setMaterial(value: string): void;

  getProtectionUpstream(): string;
  setProtectionUpstream(value: string): void;

  getProtectionDownstream(): string;
  setProtectionDownstream(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Bridge.AsObject;
  static toObject(includeInstance: boolean, msg: Bridge): Bridge.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Bridge, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Bridge;
  static deserializeBinaryFromReader(message: Bridge, reader: jspb.BinaryReader): Bridge;
}

export namespace Bridge {
  export type AsObject = {
    id: number,
    roadId: number,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    lastModified?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    structureCode: string,
    structureName: string,
    structureClass: string,
    administrativeArea: string,
    roadCode: string,
    constructionYear: number,
    length: number,
    width: number,
    chainage: number,
    structureType: string,
    riverName: string,
    numberSpans: number,
    spanLength: number,
    material: string,
    protectionUpstream: string,
    protectionDownstream: string,
  }
}

export class Bridges extends jspb.Message {
  clearBridgesList(): void;
  getBridgesList(): Array<Bridge>;
  setBridgesList(value: Array<Bridge>): void;
  addBridges(value?: Bridge, index?: number): Bridge;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Bridges.AsObject;
  static toObject(includeInstance: boolean, msg: Bridges): Bridges.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Bridges, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Bridges;
  static deserializeBinaryFromReader(message: Bridges, reader: jspb.BinaryReader): Bridges;
}

export namespace Bridges {
  export type AsObject = {
    bridgesList: Array<Bridge.AsObject>,
  }
}

export class Culvert extends jspb.Message {
  getId(): number;
  setId(value: number): void;

  getRoadId(): number;
  setRoadId(value: number): void;

  hasDateCreated(): boolean;
  clearDateCreated(): void;
  getDateCreated(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateCreated(value?: google_protobuf_timestamp_pb.Timestamp): void;

  hasLastModified(): boolean;
  clearLastModified(): void;
  getLastModified(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setLastModified(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getStructureCode(): string;
  setStructureCode(value: string): void;

  getStructureName(): string;
  setStructureName(value: string): void;

  getStructureClass(): string;
  setStructureClass(value: string): void;

  getAdministrativeArea(): string;
  setAdministrativeArea(value: string): void;

  getRoadCode(): string;
  setRoadCode(value: string): void;

  getConstructionYear(): number;
  setConstructionYear(value: number): void;

  getLength(): number;
  setLength(value: number): void;

  getWidth(): number;
  setWidth(value: number): void;

  getChainage(): number;
  setChainage(value: number): void;

  getStructureType(): string;
  setStructureType(value: string): void;

  getHeight(): number;
  setHeight(value: number): void;

  getNumberCells(): number;
  setNumberCells(value: number): void;

  getMaterial(): string;
  setMaterial(value: string): void;

  getProtectionUpstream(): string;
  setProtectionUpstream(value: string): void;

  getProtectionDownstream(): string;
  setProtectionDownstream(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Culvert.AsObject;
  static toObject(includeInstance: boolean, msg: Culvert): Culvert.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Culvert, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Culvert;
  static deserializeBinaryFromReader(message: Culvert, reader: jspb.BinaryReader): Culvert;
}

export namespace Culvert {
  export type AsObject = {
    id: number,
    roadId: number,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    lastModified?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    structureCode: string,
    structureName: string,
    structureClass: string,
    administrativeArea: string,
    roadCode: string,
    constructionYear: number,
    length: number,
    width: number,
    chainage: number,
    structureType: string,
    height: number,
    numberCells: number,
    material: string,
    protectionUpstream: string,
    protectionDownstream: string,
  }
}

export class Culverts extends jspb.Message {
  clearCulvertsList(): void;
  getCulvertsList(): Array<Culvert>;
  setCulvertsList(value: Array<Culvert>): void;
  addCulverts(value?: Culvert, index?: number): Culvert;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Culverts.AsObject;
  static toObject(includeInstance: boolean, msg: Culverts): Culverts.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Culverts, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Culverts;
  static deserializeBinaryFromReader(message: Culverts, reader: jspb.BinaryReader): Culverts;
}

export namespace Culverts {
  export type AsObject = {
    culvertsList: Array<Culvert.AsObject>,
  }
}


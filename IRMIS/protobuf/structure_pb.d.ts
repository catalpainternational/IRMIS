// package: assets
// file: structure.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";
import * as media_pb from "./media_pb";
import * as roads_pb from "./roads_pb";

export class Structures extends jspb.Message {
  clearBridgesList(): void;
  getBridgesList(): Array<Bridge>;
  setBridgesList(value: Array<Bridge>): void;
  addBridges(value?: Bridge, index?: number): Bridge;

  clearCulvertsList(): void;
  getCulvertsList(): Array<Culvert>;
  setCulvertsList(value: Array<Culvert>): void;
  addCulverts(value?: Culvert, index?: number): Culvert;

  clearDriftsList(): void;
  getDriftsList(): Array<Drift>;
  setDriftsList(value: Array<Drift>): void;
  addDrifts(value?: Drift, index?: number): Drift;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Structures.AsObject;
  static toObject(includeInstance: boolean, msg: Structures): Structures.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Structures, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Structures;
  static deserializeBinaryFromReader(message: Structures, reader: jspb.BinaryReader): Structures;
}

export namespace Structures {
  export type AsObject = {
    bridgesList: Array<Bridge.AsObject>,
    culvertsList: Array<Culvert.AsObject>,
    driftsList: Array<Drift.AsObject>,
  }
}

export class Bridge extends jspb.Message {
  getId(): string;
  setId(value: string): void;

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

  getAssetClass(): string;
  setAssetClass(value: string): void;

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

  getMaterial(): string;
  setMaterial(value: string): void;

  getProtectionUpstream(): string;
  setProtectionUpstream(value: string): void;

  getProtectionDownstream(): string;
  setProtectionDownstream(value: string): void;

  hasGeomPoint(): boolean;
  clearGeomPoint(): void;
  getGeomPoint(): roads_pb.Projection | undefined;
  setGeomPoint(value?: roads_pb.Projection): void;

  getGeojsonId(): number;
  setGeojsonId(value: number): void;

  getAssetCondition(): string;
  setAssetCondition(value: string): void;

  getConditionDescription(): string;
  setConditionDescription(value: string): void;

  clearInventoryMediaList(): void;
  getInventoryMediaList(): Array<media_pb.Media>;
  setInventoryMediaList(value: Array<media_pb.Media>): void;
  addInventoryMedia(value?: media_pb.Media, index?: number): media_pb.Media;

  clearSurveyMediaList(): void;
  getSurveyMediaList(): Array<media_pb.Media>;
  setSurveyMediaList(value: Array<media_pb.Media>): void;
  addSurveyMedia(value?: media_pb.Media, index?: number): media_pb.Media;

  getRiverName(): string;
  setRiverName(value: string): void;

  getNumberSpans(): number;
  setNumberSpans(value: number): void;

  getSpanLength(): number;
  setSpanLength(value: number): void;

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
    id: string,
    roadId: number,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    lastModified?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    structureCode: string,
    structureName: string,
    assetClass: string,
    administrativeArea: string,
    roadCode: string,
    constructionYear: number,
    length: number,
    width: number,
    chainage: number,
    structureType: string,
    material: string,
    protectionUpstream: string,
    protectionDownstream: string,
    geomPoint?: roads_pb.Projection.AsObject,
    geojsonId: number,
    assetCondition: string,
    conditionDescription: string,
    inventoryMediaList: Array<media_pb.Media.AsObject>,
    surveyMediaList: Array<media_pb.Media.AsObject>,
    riverName: string,
    numberSpans: number,
    spanLength: number,
  }
}

export class Culvert extends jspb.Message {
  getId(): string;
  setId(value: string): void;

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

  getAssetClass(): string;
  setAssetClass(value: string): void;

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

  getMaterial(): string;
  setMaterial(value: string): void;

  getProtectionUpstream(): string;
  setProtectionUpstream(value: string): void;

  getProtectionDownstream(): string;
  setProtectionDownstream(value: string): void;

  hasGeomPoint(): boolean;
  clearGeomPoint(): void;
  getGeomPoint(): roads_pb.Projection | undefined;
  setGeomPoint(value?: roads_pb.Projection): void;

  getGeojsonId(): number;
  setGeojsonId(value: number): void;

  getAssetCondition(): string;
  setAssetCondition(value: string): void;

  getConditionDescription(): string;
  setConditionDescription(value: string): void;

  clearInventoryMediaList(): void;
  getInventoryMediaList(): Array<media_pb.Media>;
  setInventoryMediaList(value: Array<media_pb.Media>): void;
  addInventoryMedia(value?: media_pb.Media, index?: number): media_pb.Media;

  clearSurveyMediaList(): void;
  getSurveyMediaList(): Array<media_pb.Media>;
  setSurveyMediaList(value: Array<media_pb.Media>): void;
  addSurveyMedia(value?: media_pb.Media, index?: number): media_pb.Media;

  getHeight(): number;
  setHeight(value: number): void;

  getNumberCells(): number;
  setNumberCells(value: number): void;

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
    id: string,
    roadId: number,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    lastModified?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    structureCode: string,
    structureName: string,
    assetClass: string,
    administrativeArea: string,
    roadCode: string,
    constructionYear: number,
    length: number,
    width: number,
    chainage: number,
    structureType: string,
    material: string,
    protectionUpstream: string,
    protectionDownstream: string,
    geomPoint?: roads_pb.Projection.AsObject,
    geojsonId: number,
    assetCondition: string,
    conditionDescription: string,
    inventoryMediaList: Array<media_pb.Media.AsObject>,
    surveyMediaList: Array<media_pb.Media.AsObject>,
    height: number,
    numberCells: number,
  }
}

export class Drift extends jspb.Message {
  getId(): string;
  setId(value: string): void;

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

  getAssetClass(): string;
  setAssetClass(value: string): void;

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

  getMaterial(): string;
  setMaterial(value: string): void;

  getProtectionUpstream(): string;
  setProtectionUpstream(value: string): void;

  getProtectionDownstream(): string;
  setProtectionDownstream(value: string): void;

  hasGeomPoint(): boolean;
  clearGeomPoint(): void;
  getGeomPoint(): roads_pb.Projection | undefined;
  setGeomPoint(value?: roads_pb.Projection): void;

  getGeojsonId(): number;
  setGeojsonId(value: number): void;

  getAssetCondition(): string;
  setAssetCondition(value: string): void;

  getConditionDescription(): string;
  setConditionDescription(value: string): void;

  clearInventoryMediaList(): void;
  getInventoryMediaList(): Array<media_pb.Media>;
  setInventoryMediaList(value: Array<media_pb.Media>): void;
  addInventoryMedia(value?: media_pb.Media, index?: number): media_pb.Media;

  clearSurveyMediaList(): void;
  getSurveyMediaList(): Array<media_pb.Media>;
  setSurveyMediaList(value: Array<media_pb.Media>): void;
  addSurveyMedia(value?: media_pb.Media, index?: number): media_pb.Media;

  getThickness(): number;
  setThickness(value: number): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Drift.AsObject;
  static toObject(includeInstance: boolean, msg: Drift): Drift.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Drift, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Drift;
  static deserializeBinaryFromReader(message: Drift, reader: jspb.BinaryReader): Drift;
}

export namespace Drift {
  export type AsObject = {
    id: string,
    roadId: number,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    lastModified?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    structureCode: string,
    structureName: string,
    assetClass: string,
    administrativeArea: string,
    roadCode: string,
    constructionYear: number,
    length: number,
    width: number,
    chainage: number,
    structureType: string,
    material: string,
    protectionUpstream: string,
    protectionDownstream: string,
    geomPoint?: roads_pb.Projection.AsObject,
    geojsonId: number,
    assetCondition: string,
    conditionDescription: string,
    inventoryMediaList: Array<media_pb.Media.AsObject>,
    surveyMediaList: Array<media_pb.Media.AsObject>,
    thickness: number,
  }
}


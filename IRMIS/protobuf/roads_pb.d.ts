// package: assets
// file: roads.proto

import * as jspb from "google-protobuf";
import * as media_pb from "./media_pb";

export class Projection extends jspb.Message {
  getX(): number;
  setX(value: number): void;

  getY(): number;
  setY(value: number): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Projection.AsObject;
  static toObject(includeInstance: boolean, msg: Projection): Projection.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Projection, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Projection;
  static deserializeBinaryFromReader(message: Projection, reader: jspb.BinaryReader): Projection;
}

export namespace Projection {
  export type AsObject = {
    x: number,
    y: number,
  }
}

export class Road extends jspb.Message {
  getId(): number;
  setId(value: number): void;

  getGeojsonId(): number;
  setGeojsonId(value: number): void;

  getRoadCode(): string;
  setRoadCode(value: string): void;

  getRoadName(): string;
  setRoadName(value: string): void;

  getAssetClass(): string;
  setAssetClass(value: string): void;

  getRoadStatus(): string;
  setRoadStatus(value: string): void;

  getLinkCode(): string;
  setLinkCode(value: string): void;

  getLinkStartName(): string;
  setLinkStartName(value: string): void;

  getLinkStartChainage(): number;
  setLinkStartChainage(value: number): void;

  getLinkEndName(): string;
  setLinkEndName(value: string): void;

  getLinkEndChainage(): number;
  setLinkEndChainage(value: number): void;

  getLinkLength(): number;
  setLinkLength(value: number): void;

  getSurfaceType(): string;
  setSurfaceType(value: string): void;

  getAssetCondition(): string;
  setAssetCondition(value: string): void;

  getPavementClass(): string;
  setPavementClass(value: string): void;

  getCarriagewayWidth(): number;
  setCarriagewayWidth(value: number): void;

  getTotalWidth(): number;
  setTotalWidth(value: number): void;

  getAdministrativeArea(): string;
  setAdministrativeArea(value: string): void;

  getProject(): string;
  setProject(value: string): void;

  getFundingSource(): string;
  setFundingSource(value: string): void;

  getTechnicalClass(): string;
  setTechnicalClass(value: string): void;

  getMaintenanceNeed(): string;
  setMaintenanceNeed(value: string): void;

  getTrafficLevel(): string;
  setTrafficLevel(value: string): void;

  hasProjectionStart(): boolean;
  clearProjectionStart(): void;
  getProjectionStart(): Projection | undefined;
  setProjectionStart(value?: Projection): void;

  hasProjectionEnd(): boolean;
  clearProjectionEnd(): void;
  getProjectionEnd(): Projection | undefined;
  setProjectionEnd(value?: Projection): void;

  getNumberLanes(): number;
  setNumberLanes(value: number): void;

  getRainfallMaximum(): number;
  setRainfallMaximum(value: number): void;

  getRainfallMinimum(): number;
  setRainfallMinimum(value: number): void;

  getConstructionYear(): number;
  setConstructionYear(value: number): void;

  getPopulation(): number;
  setPopulation(value: number): void;

  getCore(): number;
  setCore(value: number): void;

  clearServedFacilitiesList(): void;
  getServedFacilitiesList(): Array<number>;
  setServedFacilitiesList(value: Array<number>): void;
  addServedFacilities(value: number, index?: number): number;

  clearServedEconomicAreasList(): void;
  getServedEconomicAreasList(): Array<number>;
  setServedEconomicAreasList(value: Array<number>): void;
  addServedEconomicAreas(value: number, index?: number): number;

  clearServedConnectionTypesList(): void;
  getServedConnectionTypesList(): Array<number>;
  setServedConnectionTypesList(value: Array<number>): void;
  addServedConnectionTypes(value: number, index?: number): number;

  clearInventoryMediaList(): void;
  getInventoryMediaList(): Array<media_pb.Media>;
  setInventoryMediaList(value: Array<media_pb.Media>): void;
  addInventoryMedia(value?: media_pb.Media, index?: number): media_pb.Media;

  clearSurveyMediaList(): void;
  getSurveyMediaList(): Array<media_pb.Media>;
  setSurveyMediaList(value: Array<media_pb.Media>): void;
  addSurveyMedia(value?: media_pb.Media, index?: number): media_pb.Media;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Road.AsObject;
  static toObject(includeInstance: boolean, msg: Road): Road.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Road, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Road;
  static deserializeBinaryFromReader(message: Road, reader: jspb.BinaryReader): Road;
}

export namespace Road {
  export type AsObject = {
    id: number,
    geojsonId: number,
    roadCode: string,
    roadName: string,
    assetClass: string,
    roadStatus: string,
    linkCode: string,
    linkStartName: string,
    linkStartChainage: number,
    linkEndName: string,
    linkEndChainage: number,
    linkLength: number,
    surfaceType: string,
    assetCondition: string,
    pavementClass: string,
    carriagewayWidth: number,
    totalWidth: number,
    administrativeArea: string,
    project: string,
    fundingSource: string,
    technicalClass: string,
    maintenanceNeed: string,
    trafficLevel: string,
    projectionStart?: Projection.AsObject,
    projectionEnd?: Projection.AsObject,
    numberLanes: number,
    rainfallMaximum: number,
    rainfallMinimum: number,
    constructionYear: number,
    population: number,
    core: number,
    servedFacilitiesList: Array<number>,
    servedEconomicAreasList: Array<number>,
    servedConnectionTypesList: Array<number>,
    inventoryMediaList: Array<media_pb.Media.AsObject>,
    surveyMediaList: Array<media_pb.Media.AsObject>,
  }
}

export class Roads extends jspb.Message {
  clearRoadsList(): void;
  getRoadsList(): Array<Road>;
  setRoadsList(value: Array<Road>): void;
  addRoads(value?: Road, index?: number): Road;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Roads.AsObject;
  static toObject(includeInstance: boolean, msg: Roads): Roads.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Roads, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Roads;
  static deserializeBinaryFromReader(message: Roads, reader: jspb.BinaryReader): Roads;
}

export namespace Roads {
  export type AsObject = {
    roadsList: Array<Road.AsObject>,
  }
}


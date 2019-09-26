// package: assets
// file: roads.proto

import * as jspb from "google-protobuf";

export class Road extends jspb.Message {
  getId(): number;
  setId(value: number): void;

  getGeojsonId(): number;
  setGeojsonId(value: number): void;

  getRoadCode(): string;
  setRoadCode(value: string): void;

  getRoadName(): string;
  setRoadName(value: string): void;

  getRoadType(): string;
  setRoadType(value: string): void;

  getRoadStatus(): string;
  setRoadStatus(value: string): void;

  getLinkCode(): string;
  setLinkCode(value: string): void;

  getLinkName(): string;
  setLinkName(value: string): void;

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

  getSurfaceCondition(): string;
  setSurfaceCondition(value: string): void;

  getPavementClass(): string;
  setPavementClass(value: string): void;

  getCarriagewayWidth(): number;
  setCarriagewayWidth(value: number): void;

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

  getLastRevisionId(): number;
  setLastRevisionId(value: number): void;

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
    roadType: string,
    roadStatus: string,
    linkCode: string,
    linkName: string,
    linkStartName: string,
    linkStartChainage: number,
    linkEndName: string,
    linkEndChainage: number,
    linkLength: number,
    surfaceType: string,
    surfaceCondition: string,
    pavementClass: string,
    carriagewayWidth: number,
    administrativeArea: string,
    project: string,
    fundingSource: string,
    technicalClass: string,
    maintenanceNeed: string,
    trafficLevel: string,
    lastRevisionId: number,
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


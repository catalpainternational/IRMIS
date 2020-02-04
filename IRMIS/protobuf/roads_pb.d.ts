// package: assets
// file: roads.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Version extends jspb.Message {
  getPk(): number;
  setPk(value: number): void;

  hasDateCreated(): boolean;
  clearDateCreated(): void;
  getDateCreated(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateCreated(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getUser(): string;
  setUser(value: string): void;

  getComment(): string;
  setComment(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Version.AsObject;
  static toObject(includeInstance: boolean, msg: Version): Version.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Version, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Version;
  static deserializeBinaryFromReader(message: Version, reader: jspb.BinaryReader): Version;
}

export namespace Version {
  export type AsObject = {
    pk: number,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    user: string,
    comment: string,
  }
}

export class Versions extends jspb.Message {
  clearVersionsList(): void;
  getVersionsList(): Array<Version>;
  setVersionsList(value: Array<Version>): void;
  addVersions(value?: Version, index?: number): Version;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Versions.AsObject;
  static toObject(includeInstance: boolean, msg: Versions): Versions.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Versions, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Versions;
  static deserializeBinaryFromReader(message: Versions, reader: jspb.BinaryReader): Versions;
}

export namespace Versions {
  export type AsObject = {
    versionsList: Array<Version.AsObject>,
  }
}

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

  getRainfall(): number;
  setRainfall(value: number): void;

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
    surfaceCondition: string,
    pavementClass: string,
    carriagewayWidth: number,
    administrativeArea: string,
    project: string,
    fundingSource: string,
    technicalClass: string,
    maintenanceNeed: string,
    trafficLevel: string,
    projectionStart?: Projection.AsObject,
    projectionEnd?: Projection.AsObject,
    numberLanes: number,
    rainfall: number,
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


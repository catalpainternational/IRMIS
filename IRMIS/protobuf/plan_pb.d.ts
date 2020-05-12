// package: assets
// file: plan.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Snapshot extends jspb.Message {
  getId(): number;
  setId(value: number): void;

  getYear(): number;
  setYear(value: number): void;

  getBudget(): number;
  setBudget(value: number): void;

  getLength(): number;
  setLength(value: number): void;

  getAssetClass(): string;
  setAssetClass(value: string): void;

  getWorkType(): string;
  setWorkType(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Snapshot.AsObject;
  static toObject(includeInstance: boolean, msg: Snapshot): Snapshot.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Snapshot, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Snapshot;
  static deserializeBinaryFromReader(message: Snapshot, reader: jspb.BinaryReader): Snapshot;
}

export namespace Snapshot {
  export type AsObject = {
    id: number,
    year: number,
    budget: number,
    length: number,
    assetClass: string,
    workType: string,
  }
}

export class Plan extends jspb.Message {
  getId(): number;
  setId(value: number): void;

  getTitle(): string;
  setTitle(value: string): void;

  getFile(): Uint8Array | string;
  getFile_asU8(): Uint8Array;
  getFile_asB64(): string;
  setFile(value: Uint8Array | string): void;

  getUser(): number;
  setUser(value: number): void;

  getAddedBy(): string;
  setAddedBy(value: string): void;

  hasLastModified(): boolean;
  clearLastModified(): void;
  getLastModified(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setLastModified(value?: google_protobuf_timestamp_pb.Timestamp): void;

  hasDateCreated(): boolean;
  clearDateCreated(): void;
  getDateCreated(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setDateCreated(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getApproved(): boolean;
  setApproved(value: boolean): void;

  getAssetClass(): string;
  setAssetClass(value: string): void;

  clearSummaryList(): void;
  getSummaryList(): Array<Snapshot>;
  setSummaryList(value: Array<Snapshot>): void;
  addSummary(value?: Snapshot, index?: number): Snapshot;

  getUrl(): string;
  setUrl(value: string): void;

  getFileName(): string;
  setFileName(value: string): void;

  getPlanningPeriod(): string;
  setPlanningPeriod(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Plan.AsObject;
  static toObject(includeInstance: boolean, msg: Plan): Plan.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Plan, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Plan;
  static deserializeBinaryFromReader(message: Plan, reader: jspb.BinaryReader): Plan;
}

export namespace Plan {
  export type AsObject = {
    id: number,
    title: string,
    file: Uint8Array | string,
    user: number,
    addedBy: string,
    lastModified?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    dateCreated?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    approved: boolean,
    assetClass: string,
    summaryList: Array<Snapshot.AsObject>,
    url: string,
    fileName: string,
    planningPeriod: string,
  }
}

export class Plans extends jspb.Message {
  clearPlansList(): void;
  getPlansList(): Array<Plan>;
  setPlansList(value: Array<Plan>): void;
  addPlans(value?: Plan, index?: number): Plan;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Plans.AsObject;
  static toObject(includeInstance: boolean, msg: Plans): Plans.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Plans, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Plans;
  static deserializeBinaryFromReader(message: Plans, reader: jspb.BinaryReader): Plans;
}

export namespace Plans {
  export type AsObject = {
    plansList: Array<Plan.AsObject>,
  }
}

export class PlanSnapshots extends jspb.Message {
  clearSnapshotsList(): void;
  getSnapshotsList(): Array<Snapshot>;
  setSnapshotsList(value: Array<Snapshot>): void;
  addSnapshots(value?: Snapshot, index?: number): Snapshot;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): PlanSnapshots.AsObject;
  static toObject(includeInstance: boolean, msg: PlanSnapshots): PlanSnapshots.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: PlanSnapshots, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): PlanSnapshots;
  static deserializeBinaryFromReader(message: PlanSnapshots, reader: jspb.BinaryReader): PlanSnapshots;
}

export namespace PlanSnapshots {
  export type AsObject = {
    snapshotsList: Array<Snapshot.AsObject>,
  }
}


import { Plan, Plans, Snapshot, PlanSnapshots } from "../../protobuf/plan_pb";
import { EstradaPlan, makeEstradaPlan, makeEstradaSnapshot } from "./models/plan";

import { ConfigAPI } from "./configAPI";

/** getPlansMetadata
 *
 * Retrieves ALL the Plans metadata from the server
 *
 * @returns a map {id: plan_object}
 */
export function getPlansMetadata() {
    const planTypeUrlFragment = "protobuf_plans";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${planTypeUrlFragment}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Plans.deserializeBinary(uintArray).getPlansList().map(makeEstradaPlan);
        });
}

/** getPlanMetadata
 *
 * Retrieves the metadata for a single plan from the server
 *
 * @returns a plan_object
 */
export function getPlanMetadata(planId: string | number) {
    const planTypeUrlFragment = "protobuf_plan";

    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${planTypeUrlFragment}/${planId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaPlan(Plan.deserializeBinary(uintArray));
        });
}

/** postPlanData
 *
 * Post data for a single Plan to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function postPlanData(plan: EstradaPlan) {
    const assetTypeUrlFragment = "plan_create";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("POST");
    postAssetInit.body = plan.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Plan creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaPlan(Plan.deserializeBinary(uintArray));
        });
}

/** putPlanData
 *
 * Put data for a single Plan to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function putPlanData(plan: EstradaPlan) {
    const assetTypeUrlFragment = "plan_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = plan.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Plan creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaPlan(Plan.deserializeBinary(uintArray));
        });
}

/** approvePlanData
 *
 * Put data for a single Plan to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function approvePlanData(plan: EstradaPlan) {
    const assetTypeUrlFragment = "plan_approve";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${plan.id}`;
    const postAssetInit = ConfigAPI.requestInit("PUT");

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Plan creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaPlan(Plan.deserializeBinary(uintArray));
        });
}

/** deletePlanData
 *
 * Delete data for a single Plan on the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function deletePlanData(planId: number | string) {
    const assetTypeUrlFragment = "plan_delete";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${planId}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Plan deletion failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaPlan(Plan.deserializeBinary(uintArray));
        });
}

/** getPlanSnapshotsMetadata
 *
 * Retrieves ALL the PlanSnapshots metadata from the server
 *
 * @returns a map {id: PlanSnapshot_object}
 */
export function getPlanSnapshotsMetadata() {
    const snapshotTypeUrlFragment = "protobuf_plansnapshots";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${snapshotTypeUrlFragment}`;
    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return PlanSnapshots.deserializeBinary(uintArray).getSnapshotsList().map(makeEstradaSnapshot);
        });
}

/** getPlanSnapshotMetadata
 *
 * Retrieves the metadata for a single PlanSnapshot from the server
 *
 * @returns a PlanSnapshot_object
 */
export function getPlanSnapshotMetadata(planSnapshotId: string | number) {
    const shapshotTypeUrlFragment = "protobuf_planshapshot";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${shapshotTypeUrlFragment}/${planSnapshotId}`;
    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaSnapshot(Snapshot.deserializeBinary(uintArray));
        });
}

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
    const { metadataUrl, requestInit } = buildRequestInit("protobuf_plan", planId);
    return performPlanFetch(metadataUrl, requestInit, "metadata retrieval");
}

/** postPlanData
 *
 * Post data for a single Plan to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function postPlanData(plan: EstradaPlan) {
    const { metadataUrl, requestInit } = buildRequestInit("plan_create", undefined, "POST", plan);
    return performPlanFetch(metadataUrl, requestInit, "creation");
}

/** putPlanData
 *
 * Put data for a single Plan to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function putPlanData(plan: EstradaPlan) {
    const { metadataUrl, requestInit } = buildRequestInit("plan_update", undefined, "PUT", plan);
    return performPlanFetch(metadataUrl, requestInit, "update");
}

/** approvePlanData
 *
 * Put data for a single Plan to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function approvePlanData(plan: EstradaPlan) {
    const { metadataUrl, requestInit } = buildRequestInit("plan_approve", plan.id, "PUT", plan);
    return performPlanFetch(metadataUrl, requestInit, "approval");
}

/** deletePlanData
 *
 * Delete data for a single Plan on the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function deletePlanData(planId: number | string) {
    const { metadataUrl, requestInit } = buildRequestInit("plan_delete", planId, "PUT");
    return performPlanFetch(metadataUrl, requestInit, "deletion");
}

function buildRequestInit(
    assetTypeUrlFragment: string, planId: number | string | undefined, method?: any, plan?: EstradaPlan) {
    const metadataUrl = !planId
        ? `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`
        : `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${planId}`;

    const requestInit = ConfigAPI.requestInit(method);
    if (plan && (method === "PUT" || method === "POST")) {
        requestInit.body = plan.serializeBinary();
    }

    return { metadataUrl, requestInit };
}

function performPlanFetch(metadataUrl: RequestInfo, requestInit: RequestInit, failureMessage: string) {
    return fetch(metadataUrl, requestInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) {
                return metadataResponse.arrayBuffer();
            }
            throw new Error(`Plan ${failureMessage} failed: ${metadataResponse.statusText}`);
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

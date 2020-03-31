import { getPlanMetadata, getPlansMetadata, postPlanData, putPlanData, deletePlanData, getPlanSnapshotsMetadata, getPlanSnapshotMetadata } from "./assets/planAPI";

let plans = {};
let snapshots = {};

export function getPlan(id) {
    let plan = plans[id];
    if (plan) return Promise.resolve(plan);
    return getPlanMetadata(id);
}

export function getPlans() {
    return Promise.resolve(getPlansMetadata())
        .then(plans => {
            return plans;
        });
}

export function createPlan(plan) {
    return Promise.resolve(postPlanData(plan))
        .then(plan => {
            return plan;
        });
}

export function updatePlan(plan) {
    return Promise.resolve(putPlanData(plan))
        .then(plan => {
            return plan;
        });
}

export function deletePlan(planId) {
    return Promise.resolve(deletePlanData(planId))
        .then(plan => {
            return plan;
        });
}

export function getPlanSnapshot(id) {
    let snapshot = snapshots[id];
    if (snapshot) return Promise.resolve(snapshot);
    return getPlanSnapshotMetadata(id);
}

export function getSnapshots() {
    return Promise.resolve(getPlanSnapshotsMetadata())
        .then(snapshots => {
            return snapshots;
        });
}

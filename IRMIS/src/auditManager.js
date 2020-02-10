import { getRoadAuditData } from "./assets/auditAPI";
// import { dispatch } from "./assets/utilities";

export function getRoadAudit(roadId) {
    return Promise.resolve(getRoadAuditData(roadId))
        .then((auditList) => {
            // dispatch("estrada.auditTable.roadAuditDataAdded", { detail: { auditList } });
            return auditList;
        });
}

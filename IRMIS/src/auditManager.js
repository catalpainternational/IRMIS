import { getRoadAuditData, getStructureAuditData } from "./assets/auditAPI";

export function getRoadAudit(roadId) {
    return Promise.resolve(getRoadAuditData(roadId))
        .then((auditList) => {
            return auditList;
        });
}

export function getStructureAudit(structureId) {
    return Promise.resolve(getStructureAuditData(structureId))
        .then((auditList) => {
            return auditList;
        });
}

import { Versions } from "../../protobuf/version_pb";
import { makeEstradaAudit } from "./models/audit";

import { ConfigAPI } from "./configAPI";

/** getRoadAuditData
 *
 * Retrieves the Audit changes data for a single road from the server
 *
 * @returns a list of version objects
 */
export function getRoadAuditData(roadId: string | number) {
    const assetTypeUrlFragment = "protobuf_road_audit";

    const auditDataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${roadId}`;

    return fetch(auditDataUrl, ConfigAPI.requestInit())
        .then((auditDataResponse) => (auditDataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Versions.deserializeBinary(uintArray).getVersionsList().map(makeEstradaAudit);
        });
}

/** getStructureAuditData
 *
 * Retrieves the Audit changes data for a single structure from the server
 *
 * @returns a list of version objects
 */
export function getStructureAuditData(structureId: string) {
    const structureTypeUrlFragment = "protobuf_structure_audit";
    const auditDataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${structureId}`;

    return fetch(auditDataUrl, ConfigAPI.requestInit())
        .then((auditDataResponse) => (auditDataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Versions.deserializeBinary(uintArray).getVersionsList().map(makeEstradaAudit);
        });
}

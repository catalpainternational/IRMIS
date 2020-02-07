import { Versions } from "../../protobuf/roads_pb";
import { makeEstradaAudit } from "./models/audit";

import { ConfigAPI } from "./configAPI";

/** getRoadAuditData
 *
 * Retrieves the Audit changes data for a single road from the server
 *
 * @returns a list of version objects
 */
export function getRoadAuditData(roadId) {
    const assetTypeUrlFragment = "protobuf_road_audit";

    const auditDataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${roadId}`;

    return fetch(auditDataUrl, ConfigAPI.requestInit())
        .then((auditDataResponse) => (auditDataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Versions.deserializeBinary(uintArray).getVersionsList().map(makeEstradaAudit);
        });
}

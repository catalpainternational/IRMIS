import { Road, Roads, Versions } from "../../protobuf/roads_pb";
import { EstradaRoad } from "./models/road";
import { EstradaAudit } from "./models/audit";

import { ConfigAPI } from "./configAPI";
import { makeEstradaObject } from "./protoBufUtilities";

/** getRoadsMetadataChunks
 *
 * Retrieves the details for the road metadata chunks from the server
 *
 * @returns a map {id: road_object}
 */
export function getRoadsMetadataChunks() {
    const assetTypeUrlFragment = "road_chunks";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((jsonResponse) => (jsonResponse.json()));
}

/** getRoadsMetadata
 *
 * Retrieves the road metadata from the server
 *
 * @returns a map {id: road_object}
 */
export function getRoadsMetadata(chunkName) {
    const assetTypeUrlFragment = "protobuf_roads";
    chunkName = chunkName || "";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${chunkName}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Roads.deserializeBinary(uintArray).getRoadsList().map(makeEstradaRoad);
        });
}

/** getRoadMetadata
 *
 * Retrieves the metadata for a single road from the server
 *
 * @returns a road_object
 */
export function getRoadMetadata(roadId) {
    const assetTypeUrlFragment = "protobuf_road";

    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${roadId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaRoad(Road.deserializeBinary(uintArray));
        });
}

/** putRoadMetadata
 *
 * Post metadata for a single road to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function putRoadMetadata(road) {
    const assetTypeUrlFragment = "road_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = road.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then(metadataResponse => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Road update failed: ${metadataResponse.statusText}`);
        })
        .then(protobufBytes => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaRoad(Road.deserializeBinary(uintArray));
        });
}

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

function makeEstradaRoad(pbroad) {
    return makeEstradaObject(EstradaRoad, pbroad);
}

export function makeEstradaAudit(pbversion) {
    return makeEstradaObject(EstradaAudit, pbversion);
}

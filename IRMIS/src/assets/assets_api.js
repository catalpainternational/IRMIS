import { Road, Roads, Versions } from "../../protobuf/roads_pb";
import { EstradaRoad } from "./models/road";
import { EstradaAudit } from "./models/audit";

// Placeholders, purely as reminders of 
// import { Structure, Structures } from "../../protobuf/structures_pb";
// import { EstradaStructure } from "./models/structure";

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

/** getStructuresMetadataChunks
 *
 * Retrieves the details for the structure metadata chunks from the server
 *
 * @returns a map {id: structure_object}
 */
export function getStructuresMetadataChunks() {
    const assetTypeUrlFragment = "structure_chunks";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((jsonResponse) => {
            if (jsonResponse.ok) {
                return jsonResponse.json();
            } else {
                // Dummy data
                return [{ "asset_type": "BRIDGE", "asset_type__count": 0 }, { "asset_type": "CULVERT", "asset_type__count": 0 }];
            }
        })
}

/** getStructuresMetadata
 *
 * Retrieves the structure metadata from the server
 *
 * @returns a map {id: structure_object}
 */
export function getStructuresMetadata(chunkName) {
    const assetTypeUrlFragment = "protobuf_structures";
    chunkName = chunkName || "";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${chunkName}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => {
            if (metadataResponse.ok) {
                return metadataResponse.arrayBuffer();
            } else {
                // Dummy data
                return Promise.resolve([]);
            }
        })
        .then((protobufBytes) => {
            return [];
            // const uintArray = new Uint8Array(protobufBytes);
            // return Structures.deserializeBinary(uintArray).getStructuresList().map(makeEstradaStructure);
        });
}

/** getStructureMetadata
 *
 * Retrieves the metadata for a single structure from the server
 *
 * @returns a structure_object
 */
export function getStructureMetadata(structureId) {
    const assetTypeUrlFragment = "protobuf_structure";

    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${structureId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return {};
            // return makeEstradaStructure(Structure.deserializeBinary(uintArray));
        });
}

/** putStructureMetadata
 *
 * Post metadata for a single structure to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function putStructureMetadata(structure) {
    const assetTypeUrlFragment = "structure_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = structure.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then(metadataResponse => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Structure update failed: ${metadataResponse.statusText}`);
        })
        .then(protobufBytes => {
            const uintArray = new Uint8Array(protobufBytes);
            return {};
            // return makeEstradaStructure(Structure.deserializeBinary(uintArray));
        });
}

/** getStructureAuditData
 *
 * Retrieves the Audit changes data for a single structure from the server
 *
 * @returns a list of version objects
 */
export function getStructureAuditData(structureId) {
    const assetTypeUrlFragment = "protobuf_structure_audit";

    const auditDataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${structureId}`;

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

function makeEstradaStructure(pbstructure) {
    return {};
    // return makeEstradaObject(EstradaStructure, pbstructure);
}

function makeEstradaAudit(pbversion) {
    return makeEstradaObject(EstradaAudit, pbversion);
}

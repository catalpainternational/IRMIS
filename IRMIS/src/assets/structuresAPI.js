import { Bridge, Bridges, Culvert, Culverts } from "../../protobuf/structure_pb";
import { EstradaBridge, EstradaCulvert } from "./models/structures";
import { makeEstradaAudit } from "./assets_api";
import { ConfigAPI } from "./configAPI";
import { makeEstradaObject } from "./protoBufUtilities";

/** getStructuresMetadata
 *
 * Retrieves the structures metadata from the server
 *
 * @returns a map {id: bridge_object}
 */
export function getStructuresMetadata(structureType) {
    const structureTypeUrlFragment = (structureType === "bridge") ? "protobuf_bridges" : "protobuf_culverts";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            if (structureType === "bridge") {
                return Bridges.deserializeBinary(uintArray).getBridgesList().map(makeEstradaBridge);
            } else {
                return Culverts.deserializeBinary(uintArray).getCulvertsList().map(makeEstradaCulvert);
            }
        });
}

/** getStructureMetaData
 *
 * Retrieves the metadata for a single structure from the server
 *
 * @returns a structure_object
 */
export function getStructureMetadata(structureId, structureType) {
    const structureTypeUrlFragment = (structureType === "bridge") ? "protobuf_bridge" : "protobuf_culvert";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${structureId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            if (structureType === "bridge") {
                return makeEstradaBridge(Bridge.deserializeBinary(uintArray));
            } else {
                return makeEstradaCulvert(Culvert.deserializeBinary(uintArray));
            }
        });
}

/** getStructuresMetadata
 *
 * Retrieves the structures metadata from the server
 *
 * @returns a map {id: bridge_object}
 */
export function getRoadStructuresMetadata(roadId, structureType) {
    const structureTypeUrlFragment = (structureType === "bridge") ? "protobuf_road_bridges" : "protobuf_road_culverts";
    roadId = roadId || "";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${roadId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            if (structureType === "bridge") {
                return Bridges.deserializeBinary(uintArray).getBridgesList().map(makeEstradaBridge);
            } else {
                return Culverts.deserializeBinary(uintArray).getCulvertsList().map(makeEstradaCulvert);
            }
        });
}

/** postStructureData
 *
 * Post data for a single Structure to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function postStructureData(structure, structureType) {
    const structureTypeUrlFragment = (structureType === "bridge") ? "bridge_create" : "culvert_create";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("POST");
    postAssetInit.body = structure.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then(metadataResponse => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Structure creation failed: ${metadataResponse.statusText}`);
        })
        .then(protobufBytes => {
            const uintArray = new Uint8Array(protobufBytes);
            if (structureType === "bridge") {
                return makeEstradaBridge(Bridge.deserializeBinary(uintArray));
            } else {
                return makeEstradaCulvert(Culvert.deserializeBinary(uintArray));
            }
        });
}

/** putStructureData
 *
 * Put data for a single Structure to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function putStructureData(structure, structureType) {
    const structureTypeUrlFragment = (structureType === "bridge") ? "bridge_update" : "culvert_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = structure.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then(metadataResponse => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Structure creation failed: ${metadataResponse.statusText}`);
        })
        .then(protobufBytes => {
            const uintArray = new Uint8Array(protobufBytes);
            if (structureType === "bridge") {
                return makeEstradaBridge(Bridge.deserializeBinary(uintArray));
            } else {
                return makeEstradaCulvert(Culvert.deserializeBinary(uintArray));
            }
        });
}

/** getStructureAuditData
 *
 * Retrieves the Audit changes data for a single structure from the server
 *
 * @returns a list of version objects
 */
export function getStructureAuditData(structureId, structureType) {
    const structureTypeUrlFragment = (structureType === "bridge") ? "protobuf_bridge_audit" : "protobuf_culvert_audit";
    const auditDataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${structureId}`;

    return fetch(auditDataUrl, ConfigAPI.requestInit())
        .then((auditDataResponse) => (auditDataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Versions.deserializeBinary(uintArray).getVersionsList().map(makeEstradaAudit);
        });
}

function makeEstradaBridge(pbbridge) {
    return makeEstradaObject(EstradaBridge, pbbridge);
}

function makeEstradaCulvert(pbculvert) {
    return makeEstradaObject(EstradaCulvert, pbculvert);
}

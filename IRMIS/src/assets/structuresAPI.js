import { Bridge, Culvert, Structures } from "../../protobuf/structure_pb";
import { makeEstradaAudit } from "./models/audit";
import { EstradaBridge, EstradaCulvert, EstradaStructures } from "./models/structures";
import { ConfigAPI } from "./configAPI";
import { makeEstradaObject } from "./protoBufUtilities";

/** getStructuresMetadata
 *
 * Retrieves the structures metadata from the server
 *
 * @returns a map {id: structure_object}
 */
export function getStructuresMetadata() {
    const structureTypeUrlFragment = "protobuf_structures";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}`;
    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaStructures(Structures.deserializeBinary(uintArray));
        });
}

/** getStructureMetaData
 *
 * Retrieves the metadata for a single structure from the server
 *
 * @returns a structure_object
 */
export function getStructureMetadata(structureId) {
    const structureTypeUrlFragment = "protobuf_structure";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${structureId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            if (structureId.includes("BRDG")) {
                return makeEstradaBridge(Bridge.deserializeBinary(uintArray));
            } else {
                return makeEstradaCulvert(Culvert.deserializeBinary(uintArray));
            }
        });
}

/** getRoadStructuresMetadata
 *
 * Retrieves the structures metadata from the server
 *
 * @returns a map {id: bridge_object}
 */
export function getRoadStructuresMetadata(roadId) {
    const structureTypeUrlFragment = "protobuf_road_structures";
    roadId = roadId || "";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${roadId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaStructures(Structures.deserializeBinary(uintArray));
        });
}

/** postStructureData
 *
 * Post data for a single Structure to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function postStructureData(structure, structureType) {
    const structureTypeUrlFragment = "structure_create";
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
            if (structureType === "BRDG") {
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
    const structureTypeUrlFragment = "structure_update";
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
            if (structureType === "BRDG") {
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
export function getStructureAuditData(structureId) {
    const structureTypeUrlFragment = "protobuf_structure_audit";
    const auditDataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${structureId}`;

    return fetch(auditDataUrl, ConfigAPI.requestInit())
        .then((auditDataResponse) => (auditDataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Versions.deserializeBinary(uintArray).getVersionsList().map(makeEstradaAudit);
        });
}

function makeEstradaStructures(pbstructures) {
    return makeEstradaObject(EstradaStructures, pbstructures);
}

function makeEstradaBridge(pbbridge) {
    return makeEstradaObject(EstradaBridge, pbbridge);
}

function makeEstradaCulvert(pbculvert) {
    return makeEstradaObject(EstradaCulvert, pbculvert);
}

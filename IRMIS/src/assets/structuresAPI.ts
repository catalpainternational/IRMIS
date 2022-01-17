import { Bridge, Culvert, Drift, Structures } from "../../protobuf/structure_pb";

import {
    EstradaBridge, EstradaCulvert, EstradaDrift,
    makeEstradaBridge, makeEstradaCulvert, makeEstradaDrift,
    makeEstradaStructures,
} from "./models/structures";

import { ConfigAPI } from "./configAPI";

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
export function getStructureMetadata(structureId: string) {
    const structureTypeUrlFragment = "protobuf_structure";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${structureId}/`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            const structures = makeEstradaStructures(Structures.deserializeBinary(uintArray));
            if (structureId.includes("BRDG")) {
                return structures.bridges[0];
            } else if (structureId.includes("CULV")) {
                return structures.culverts[0];
            } else {
                return structures.drifts[0];
            }
        });
}

/** getRoadStructuresMetadata
 *
 * Retrieves the structures metadata from the server
 *
 * @returns a map {id: bridge_object}
 */
export function getRoadStructuresMetadata(roadId: string | number) {
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
export function postStructureData(structure: EstradaBridge | EstradaCulvert | EstradaDrift, structureType: string) {
    const structureTypeUrlFragment = "structure_create";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${structureType}/`;

    const postAssetInit = ConfigAPI.requestInit("POST");
    postAssetInit.body = structure.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Structure creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            switch (structureType) {
                case "BRDG":
                    return makeEstradaBridge(Bridge.deserializeBinary(uintArray));
                case "CULV":
                    return makeEstradaCulvert(Culvert.deserializeBinary(uintArray));
                case "DRFT":
                    return makeEstradaDrift(Drift.deserializeBinary(uintArray));
                default:
                    // Ending up here is a programmer error
                    throw new Error(`Structure conversion failed for assetType: ${structureType}`);
            }
        });
}

/** putStructureData
 *
 * Put data for a single Structure to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function putStructureData(structure: EstradaBridge | EstradaCulvert | EstradaDrift) {
    const structureTypeUrlFragment = "structure_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${structure.id}`;

    const putAssetInit = ConfigAPI.requestInit("PUT");
    putAssetInit.body = structure.serializeBinary();

    return fetch(metadataUrl, putAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) {
                return metadataResponse.arrayBuffer();
            }
            throw new Error(`Structure creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            switch (structure.assetType) {
                case "BRDG":
                    return makeEstradaBridge(Bridge.deserializeBinary(uintArray));
                case "CULV":
                    return makeEstradaCulvert(Culvert.deserializeBinary(uintArray));
                case "DRFT":
                    return makeEstradaDrift(Drift.deserializeBinary(uintArray));
                default:
                    // Ending up here is a programmer error
                    throw new Error(`Structure conversion failed for assetType: ${structure.assetType}`);
            }
        });
}

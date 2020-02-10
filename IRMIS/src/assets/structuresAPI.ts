import { Bridge, Culvert, Structures } from "../../protobuf/structure_pb";

import { EstradaBridge, EstradaCulvert, makeEstradaBridge, makeEstradaCulvert, makeEstradaStructures } from "./models/structures";
import { makeEstradaObject } from "./protoBufUtilities";

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
export function postStructureData(structure: EstradaBridge | EstradaCulvert, structureType: string) {
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
export function putStructureData(structure: EstradaBridge | EstradaCulvert) {
    const structureTypeUrlFragment = "structure_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${structureTypeUrlFragment}/${structure.id}`;

    const putAssetInit = ConfigAPI.requestInit("PUT");
    putAssetInit.body = structure.serializeBinary();

    return fetch(metadataUrl, putAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Structure creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            try {
                return makeEstradaBridge(Bridge.deserializeBinary(uintArray));
            } catch (err) {
                return makeEstradaCulvert(Culvert.deserializeBinary(uintArray));
            }
        });
}

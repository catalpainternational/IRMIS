import { Road, Roads } from "../../protobuf/roads_pb";
import { ConfigAPI } from "./configAPI";

/** getRoadsMetadataChunks
 *
 * Retrieves the details for the road metadata chunks from the server
 *
 * @returns a map {id: road_object}
 */
export function getRoadsMetadataChunks() {
    const assetTypeUrlFragment = "road_chunks";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    return fetch(metadataUrl, ConfigAPI.requestAssetInit())
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

    return fetch(metadataUrl, ConfigAPI.requestAssetInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Roads.deserializeBinary(uintArray).getRoadsList();
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

    return fetch(metadataUrl, ConfigAPI.requestAssetInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Road.deserializeBinary(uintArray);
        });
}

/** putRoadMetadata
 *
 * Post metadata for a single road to the server
 *
 * @returns 204 (success) or 400 (failure)
 */
export function putRoadMetadata(roadData) {
    const assetTypeUrlFragment = "road_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/`;

    let request = ConfigAPI.requestAssetInit("PUT");
    request.body = roadData;
    return fetch(metadataUrl, request)
        .then(metadataResponse => {
            let status_code = metadataResponse.status;
            if (status_code === 204) { return true; }
            else { return false; }
        });
}

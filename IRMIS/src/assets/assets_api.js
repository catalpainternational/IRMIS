import { ConfigAPI } from "./configAPI";

// protobuf does not support es6 imports, commonjs works
const roadMessages = require("../../protobuf/roads_pb");

/** getRoadsMetadataChunks
 *
 * Retrieves the details for the road metadata chunks from the server
 *
 * @returns a map {id: road_object}
 */
export function getRoadsMetadataChunks() {
    const assetTypeUrlFragment = "road_chunks";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    return fetch(metadataUrl, ConfigAPI.requestAssetInit)
        .then(jsonResponse => (jsonResponse.json()));
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

    return fetch(metadataUrl, ConfigAPI.requestAssetInit)
        .then(metadataResponse => (metadataResponse.arrayBuffer()))
        .then(protobufBytes => {
            // build a map to access roads by id
            var list = roadMessages.Roads.deserializeBinary(protobufBytes).getRoadsList();
            return list.reduce(
                (roadsLookup, roadMetadata) => {
                    roadsLookup[roadMetadata.getId()] = roadMetadata;
                    return roadsLookup;
                },
                {},
            );
        });
}


export function getRoadMetadata(roadId) {
    const assetTypeUrlFragment = "road";
    const assetTypeDataRequirement = "meta";

    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${roadId}?${assetTypeDataRequirement}`;

    return fetch(metadataUrl, ConfigAPI.requestAssetInit)
        .then(metadataResponse => (metadataResponse.arrayBuffer()))
        .then(protobufBytes => (roadMessages.Road.deserializeBinary(protobufBytes)));
}


export function setRoadMetadata() {
    const assetTypeUrlFragment = "road_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;
    const postAssetInit = ConfigAPI.requestAssetInit;
    postAssetInit.method = "POST";
    postAssetInit.headers["Content-Type"] = "application/octet-stream";
    // postAssetInit.body = JSON.stringify(data); // data can be `string` or {object}!

    return fetch(metadataUrl, requestAssetInit)
        .then(metadataResponse => (metadataResponse.arrayBuffer()))
        .then(protobufBytes => (roadMessages.Road.deserializeBinary(protobufBytes)));
}

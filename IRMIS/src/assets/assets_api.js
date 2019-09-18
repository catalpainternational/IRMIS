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
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    let roadProtoArray = [];
    roadProtoArray.push(roadData.id); // Id
    roadProtoArray.push(roadData.geojsonId); // geojsonId
    roadProtoArray.push(roadData.roadCode); // roadCode
    roadProtoArray.push(roadData.roadName); // roadName
    roadProtoArray.push(roadData.linkCode); // linkCode
    roadProtoArray.push(null); // linkName
    roadProtoArray.push(roadData.linkLength); // linkLength
    roadProtoArray.push(roadData.surfaceType); // surfaceType
    roadProtoArray.push(roadData.surfaceCondition); // surfaceCondition
    roadProtoArray.push(roadData.roadType); // roadType
    roadProtoArray.push(roadData.linkStartChainage); // linkStartChainage
    roadProtoArray.push(roadData.linkEndChainage); // linkEndChainage
    roadProtoArray.push(roadData.pavementClass); // pavementClass
    roadProtoArray.push(roadData.carriagewayWidth); // carriagewayWidth
    roadProtoArray.push(roadData.administrativeArea); // administrativeArea
    roadProtoArray.push(roadData.linkStartName); // linkStartName
    roadProtoArray.push(roadData.linkEndName); // linkEndName
    roadProtoArray.push(roadData.project); // project
    roadProtoArray.push(roadData.fundingSource); // fundingSource
    roadProtoArray.push(roadData.roadStatus); // roadStatus
    roadProtoArray.push(roadData.technicalClass); // technicalClass
    roadProtoArray.push(roadData.maintenanceNeed); // maintenanceNeed
    roadProtoArray.push(roadData.trafficLevel); // trafficLevel
    roadProtoArray.push(roadData.lastRevisionId); // lastRevisionId

    let road = new Road(roadProtoArray);
    const postAssetInit = ConfigAPI.requestAssetInit("PUT");
    postAssetInit.body = road.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((postResponse) => {
            postResponse.road_pb = road;
            return postResponse;
        });
}

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

    return fetch(metadataUrl, ConfigAPI.requestAssetInit())
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

    return fetch(metadataUrl, ConfigAPI.requestAssetInit())
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
    const assetTypeUrlFragment = "roads";
    const assetTypeDataRequirement = "meta";

    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${roadId}?${assetTypeDataRequirement}`;

    return fetch(metadataUrl, ConfigAPI.requestAssetInit())
        .then(jsonResponse => (jsonResponse.json()));
}


export function setRoadMetadata(roadData) {
    const assetTypeUrlFragment = "road_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    // Convert the roadData object into an array we can use to set up the protobuf
    // I think this means we should use https://github.com/protobufjs/protobuf.js
    // instead of protoc for the JS protobuf interface
    let roadProtoArray = [];
    roadProtoArray.push(roadData.id);
    roadProtoArray.push(roadData.geojson_file); // geojsonId
    roadProtoArray.push(roadData.road_code); // roadCode
    roadProtoArray.push(roadData.road_name); // roadName
    roadProtoArray.push(roadData.link_code); // linkCode
    roadProtoArray.push(null); // linkName
    roadProtoArray.push(roadData.link_length); // linkLength
    roadProtoArray.push(roadData.surface_type); // surfaceType
    roadProtoArray.push(roadData.surface_condition); // surfaceCondition
    roadProtoArray.push(roadData.road_type); // roadType
    roadProtoArray.push(roadData.link_start_chainage); // linkStartChainage
    roadProtoArray.push(roadData.link_end_chainage); // linkEndChainage
    roadProtoArray.push(roadData.pavement_class); // pavementClass
    roadProtoArray.push(roadData.carriageway_width); // carriagewayWidth
    roadProtoArray.push(roadData.administrative_area); // administrativeArea
    roadProtoArray.push(roadData.link_start_name); // linkStartName
    roadProtoArray.push(roadData.link_end_name); // linkEndName
    roadProtoArray.push(roadData.project); // project
    roadProtoArray.push(roadData.funding_source); // fundingSource
    roadProtoArray.push(roadData.road_status); // roadStatus
    roadProtoArray.push(roadData.technical_class); // technicalClass
    roadProtoArray.push(roadData.maintenance_need); // maintenanceNeed
    roadProtoArray.push(roadData.traffic_level); // trafficLevel

    let road = new roadMessages.Road(roadProtoArray);

    const postAssetInit = ConfigAPI.requestAssetInit("PUT");
    postAssetInit.body = road.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then(postResponse => (postResponse));
}

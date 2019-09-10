import { ConfigAPI } from "./configAPI";

// protobuf does not support es6 imports, commonjs works
const roadMessages = require("../../protobuf/roads_pb");

/** getRoadsMetadata
 *
 * Retrieves the road metadata from the server
 *
 * @returns a map {id: road_object}
 */
export function getRoadsMetadata() {
    const assetTypeUrlFragment = "protobuf_roads";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

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


export function getRoadMetadata() {
    const assetTypeUrlFragment = "road_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

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

    body: JSON.stringify(data), // data can be `string` or {object}!


    return fetch(metadataUrl, requestAssetInit)
        .then(metadataResponse => (metadataResponse.arrayBuffer()))
        .then(protobufBytes => (roadMessages.Road.deserializeBinary(protobufBytes)));
}

/** populateGeoJsonProperties
 *
 * for each feature in a geojson FeatureCollection,
 * use the property `pk` to access the relevant metadata from the propertiesLookup
 * and add it to the feature properties.
 *
 * also ensure that each feature.properties has a validly set `featureType`
 *
 * @param geoJson - the GeoJSON that needs its feature.properties populated
 * @param propertiesLookup - the source of the properties data referenced by properties.pk
 */
export function populateGeoJsonProperties(geoJson, propertiesLookup) {
    geoJson.features.forEach(feature => {
        const propertySet = propertiesLookup[feature.properties.pk];
        if (propertySet) {
            Object.assign(feature.properties, propertySet.toObject());
        } else {
            throw new Error(`assets_api.populateGeoJsonProperties could not find property '${feature.properties.pk}'.`);
        }

        // Special handling for the mandatory property `featureType`
        if (!feature.properties.featureType) {
            if (feature.properties.roadType) {
                feature.properties.featureType = "Road";
            }
        }
    });
}

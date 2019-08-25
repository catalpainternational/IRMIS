import { decode } from "geobuf";
import Pbf from "pbf";

// protobuf does not support es6 imports, commonjs works
const roadMessages = require("../../protobuf/roads_pb");

const requestAssetUrl = `${window.location.origin}/assets`;
const requestAssetInit = {
    headers: { "Content-Type": "application/json" },
    method: "GET",
    mode: "no-cors",
};
const requestMediaUrl = `${window.location.origin}/media`;

export function getRoadMetadata() {
    // retrieves the road metadata from the server
    // returns a map {id: road_object}

    const metadataUrl = `${requestAssetUrl}/protobuf_roads`;

    return fetch(metadataUrl, requestAssetInit).then(metadataResponse => {
        return metadataResponse.arrayBuffer();
    }).then(protobufBytes => {
        // build a map to access roads by id
        var list =  roadMessages.Roads.deserializeBinary(protobufBytes).getRoadsList();
        return list.reduce(
            (roadsLookup, road) => {
                roadsLookup[road.getId()] = road;
                return roadsLookup;
            },
            {},
        );
    });
}

export function getGeoJsonDetails() {
    // get the details for the collated geojson files

    const geojsonDetailsUrl = `${requestAssetUrl}/geojson_details`;
    return fetch(geojsonDetailsUrl, requestAssetInit).then(geojsonDetailsResponse => {
        return geojsonDetailsResponse.json();
    });
}

export function getGeoJson(geoJsonDetail) {
    // gets geojson from a collated geometry file

    const geoJsonUrl = `${requestMediaUrl}/${geoJsonDetail.geobuf_file}`;
    return fetch(
        geoJsonUrl, requestAssetInit,
    ).then(geobufResponse => {
        return geobufResponse.arrayBuffer();
    }).then(geobufBytes => {
        var pbf = new Pbf(geobufBytes);
        return decode(pbf);
    });
}

export function populateGeoJsonProperties(geoJson, roadsLookup) {
    // for each feature in a geojson FetureCollection, use the property pk to access the road metadata
    // and add it to the feature properties

    geoJson.features.forEach(feature => {
        const road = roadsLookup[feature.properties.pk];
        Object.assign(feature.properties, road.toObject());
    });
}

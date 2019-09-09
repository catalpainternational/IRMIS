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

/** getRoadsMetadata
 *
 * Retrieves the road metadata from the server
 *
 * @returns a map {id: road_object}
 */
export function getRoadsMetadata() {
    const assetTypeUrlFragment = "protobuf_roads";
    const metadataUrl = `${requestAssetUrl}/${assetTypeUrlFragment}`;

    return fetch(metadataUrl, requestAssetInit).then(metadataResponse => {
        return metadataResponse.arrayBuffer();
    }).then(protobufBytes => {
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
        if (geobufResponse.ok) {
            return geobufResponse.arrayBuffer();
        } else {
            throw new Error(`${geobufResponse.statusText}. Geobuf response status not OK`);
        }
    }).then(geobufBytes => {
        var pbf = new Pbf(geobufBytes);
        return decode(pbf);
    });
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
            throw new Error(`assets_api.populateGeoJsonProperties could not find property '${feature.properties.pk}'.`
                + "Is there are problem with the model used by protobuf?");
        }

        // Special handling for the mandatory property `featureType`
        if (!feature.properties.featureType) {
            if (feature.properties.roadType) {
                feature.properties.featureType = "Road";
            }
        }
    });
}

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

/** getRoadsMetadataChunks
 *
 * Retrieves the details for the road metadata chunks from the server
 *
 * @returns a map {id: road_object}
 */
export function getRoadsMetadataChunks() {
    const assetTypeUrlFragment = "road_chunks";
    const metadataUrl = `${requestAssetUrl}/${assetTypeUrlFragment}`;

    return fetch(metadataUrl, requestAssetInit)
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
    const metadataUrl = `${requestAssetUrl}/${assetTypeUrlFragment}/${chunkName}`;

    return fetch(metadataUrl, requestAssetInit)
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

/** Get the details for the collated geojson files */
export function getGeoJsonDetails() {
    const geojsonDetailsUrl = `${requestAssetUrl}/geojson_details`;

    return fetch(geojsonDetailsUrl, requestAssetInit)
        .then(geojsonDetailsResponse => (geojsonDetailsResponse.json()));
}

/** Gets geojson from a collated geometry file */
export function getGeoJson(geoJsonDetail) {
    const geoJsonUrl = `${requestMediaUrl}/${geoJsonDetail.geobuf_file}`;

    return fetch(geoJsonUrl, requestAssetInit)
        .then(geobufResponse => {
            if (geobufResponse.ok) {
                return geobufResponse.arrayBuffer();
            } else {
                throw new Error(`${geobufResponse.statusText}. Geobuf response status not OK`);
            }
        })
        .then(geobufBytes => (decode(new Pbf(geobufBytes))));
}

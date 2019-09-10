import { decode } from "geobuf";
import Pbf from "pbf";

import { ConfigAPI } from "./configAPI";

export function getGeoJsonDetails() {
    // get the details for the collated geojson files

    const geojsonDetailsUrl = `${ConfigAPI.requestAssetUrl}/geojson_details`;
    return fetch(geojsonDetailsUrl, ConfigAPI.requestAssetInit)
        .then((geojsonDetailsResponse) => geojsonDetailsResponse.json());
}

export function getGeoJson(geoJsonDetail) {
    // gets geojson from a collated geometry file

    const geoJsonUrl = `${ConfigAPI.requestMediaUrl}/${geoJsonDetail.geobuf_file}`;
    return fetch(geoJsonUrl, ConfigAPI.requestAssetInit)
        .then((geobufResponse) => {
            if (geobufResponse.ok) {
                return geobufResponse.arrayBuffer();
            } else {
                throw new Error(`${geobufResponse.statusText}. Geobuf response status not OK`);
            }
        })
        .then((geobufBytes) => decode(new Pbf(geobufBytes)));
}

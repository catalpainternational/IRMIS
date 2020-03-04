import { decode } from "geobuf";
import Pbf from "pbf";

import { ConfigAPI } from "./configAPI";

/** Get the details for the collated GeoJSON files */
export function getGeoJsonDetails() {
    const geojsonDetailsUrl = ConfigAPI.requestAssetUrl + "/geojson_details";

    return fetch(geojsonDetailsUrl, ConfigAPI.requestInit)
        .then((geojsonDetailsResponse) => geojsonDetailsResponse.json());
}

/** Gets GeoJSON from a collated geometry file */
export function getGeoJsonDetail(geoJsonDetail) {
    const geoJsonUrl = ConfigAPI.requestMediaUrl + "/" + geoJsonDetail.geobuf_file;

    return fetch(geoJsonUrl, ConfigAPI.requestInit)
        .then(geobufResponse => {
            if (geobufResponse.ok) {
                return geobufResponse.arrayBuffer();
            } else {
                throw new Error(geobufResponse.statusText + ". Geobuf response status not OK");
            }
        })
        .then(geobufBytes => (decode(new Pbf(geobufBytes))));
}

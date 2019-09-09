import "babel-polyfill";

import * as riot from "riot";

import Example from "./riot/example.riot";

import "./styles/irmis.scss";

import { getRoadsMetadata, getRoadsMetadataChunks, getGeoJsonDetails } from "./assets/assets_api.js";
import { processAllDataPromises } from "./processDataPromises";

import { Map } from "./map/map";
import { initializeDataTable } from "./table";

export { filterFeatures } from "./map/utilities/filterGeoJSON";
export { geoFeatureGroups } from "./map/utilities/displayGeoJSON";

export * from "./side_menu";

export function toggle_dropdown() {
    var dropdown = document.getElementById("dropdown-menu");
    dropdown.hidden = !dropdown.hidden;
}

window.onload = () => {
    // Set up the map and table - but without any data for either
    const estradaMap = new Map();
    estradaMap.loadMap();
    const estradaTable = initializeDataTable();

    // Get the road metadata in 'chunks' as an array of promises
    getRoadsMetadataChunks()
        .then(chunks => {
            // Get smaller chunks first
            // The smallest chunk should be National (NAT) roads
            chunks = chunks.sort((chunkA, chunkB) => (chunkA.road_type__count - chunkB.road_type__count));
            const roadsMetadataPromises = chunks.map(chunk => (getRoadsMetadata(chunk.road_type)));

            // And then add in the promise for all of the geoData (GeoJSON) as well
            roadsMetadataPromises.push(getGeoJsonDetails());

            processAllDataPromises(roadsMetadataPromises, estradaTable, estradaMap)
                .then(() => {
                    /* Map and Road data loading completed, leaflet and datatable may still be rendering though */
                });
        });
};

// riot mounting point
riot.component(Example)(document.getElementById('riot-edit'));

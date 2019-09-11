import "babel-polyfill";
import * as riot from "riot";

import Edit_Base from "./riot/edit_base.riot";

import "./styles/irmis.scss";

import { getRoadsMetadata, getRoadsMetadataChunks, getGeoJsonDetails } from "./assets/assets_api.js";
import { processAllDataPromises } from "./processDataPromises";

import { Map } from "./map/map";
import { initializeDataTable } from "./table";

export { filterFeatures } from "./map/utilities/filterGeoJSON";
export { geoFeatureGroups } from "./map/utilities/displayGeoJSON";

export * from "./side_menu";

export let estradaMap;

export function toggle_dropdown() {
    var dropdown = document.getElementById("dropdown-menu");
    dropdown.hidden = !dropdown.hidden;
}

export function editRoad(roadCode) {
    window.location.hash = "edit/" + roadCode + "/assetdetails";
}

window.onload = () => {
    // Set up the map and table - but without any data for either
    estradaMap = new Map();
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
                    hashCheck();
                });
        });

    riot.register('edit_base', Edit_Base);
};

window.onhashchange = () => {
    hashCheck();
};

function hashCheck() {
    if (location.hash.startsWith("#edit")) {
        const roadCode = location.hash.split('/')[1];
        riot.mount('edit_base', { roadCode: roadCode });
        document.getElementById('view-content').hidden = true;
    } else {
        riot.unmount('edit_base', true);
        document.getElementById('view-content').hidden = false;
    }
}
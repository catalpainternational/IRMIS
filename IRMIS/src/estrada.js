import "babel-polyfill";
import * as riot from "riot";

import Edit_Base from "./riot/edit_base.riot";

import "./styles/irmis.scss";

import { getRoadsMetadata, getRoadsMetadataChunks } from "./assets/assets_api.js";
import { getGeoJsonDetails } from "./assets/geoJsonAPI.js";
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

export function editRoad(roadId) {
    // debugger;
    window.edit_road_data = {
        roadId: roadId,
        roadCode: "007",
        roadType: "NAT",
        roadName: "Dili - Como",
        roadStatus: "Ongoing",
        linkCode: "A01-01",
        linkName: "null",
        linkStartName: "Dili (Junction A3A2)",
        linkStartChainage: "0.00",
        linkEndName: "Manatuto (Juction A09)",
        linkEndChainage: "0.00",
        linkLength: "62.41",
        surfaceType: "Bitumen",
        surfaceCondition: "Good",
        pavementClass: "Sealed",
    }
    window.location.hash = "edit/" + roadId + "/assetdetails";
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
        riot.mount('edit_base', { road: edit_road_data });
        document.getElementById('view-content').hidden = true;
    } else {
        riot.unmount('edit_base', true);
        document.getElementById('view-content').hidden = false;
    }
}

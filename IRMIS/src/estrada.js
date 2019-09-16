import "babel-polyfill";
import * as riot from "riot";

import Edit_Base from "./riot/edit_base.riot";

import "./styles/irmis.scss";

import { getRoadsMetadata, getRoadsMetadataChunks } from "./assets/assets_api";
import { getGeoJsonDetails, getGeoJsonDetail } from "./assets/geoJsonAPI.js";

import { Map } from "./map/map";
import { initializeDataTable } from "./table";
import { initializeSideMenu } from "./side_menu";
import { RoadManager } from "./roadManager";


export * from "./side_menu";
export let estradaMap;
export let roadManager = new RoadManager();
initializeSideMenu(roadManager);

export function toggle_dropdown() {
    var dropdown = document.getElementById("dropdown-menu");
    dropdown.hidden = !dropdown.hidden;
}

export function editRoad(roadId) {
    window.location.hash = `edit/${roadId}/assetdetails`;
}

window.onload = () => {
    // Set up the map and table - but without any data for either
    estradaMap = new Map({roadManager});
    estradaMap.loadMap();
    const estradaTable = initializeDataTable();

    // Get the road metadata chunk details
    getRoadsMetadataChunks()
        .then(chunks => {
            // Get smaller chunks first
            // The smallest chunk should be National (NAT) roads
            chunks = chunks.sort((chunkA, chunkB) => (chunkA.road_type__count - chunkB.road_type__count));

            // for each chunk, download the roads
            chunks.forEach(chunk => {
                getRoadsMetadata(chunk.road_type)
                    .then(roadList => {
                        // add the roads to the road manager
                        roadManager.add(roadList);
                        // add the roads to the table
                        estradaTable.rows.add(roadList).draw();
                    });
            });
        });
    
    // Get the geometry details
    getGeoJsonDetails()
        .then(geoJsonDetails => {
            // for each chunk, download the geojson
            geoJsonDetails.forEach(geoJsonDetail => {
                getGeoJsonDetail(geoJsonDetail)
                    .then(geoJson => {
                        // add to map
                        estradaMap.addMapData(geoJson);
                    });
            });
        });

    riot.register('edit_base', Edit_Base);
    hashCheck();
};

window.onhashchange = () => {
    hashCheck();
};

function hashCheck() {
    if (location.hash.startsWith("#edit")) {
        riot.mount('edit_base', { roadCode: 'A1-01' });
        document.getElementById('view-content').hidden = true;
    } else {
        riot.unmount('edit_base', true);
        document.getElementById('view-content').hidden = false;
    }
}

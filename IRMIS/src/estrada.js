import "babel-polyfill";

import * as riot from "riot";

import Example from "./riot/example.riot";

import "./styles/irmis.scss";

import { Map } from "./map/map";
import { getRoadsMetadata, getRoadsMetadataChunks, getGeoJsonDetails, getGeoJson, populateGeoJsonProperties } from "./assets/assets_api.js";
import { initializeDataTable } from "./table";

export { filterFeatures } from "./map/utilities/filterGeoJSON";
export { geoFeatureGroups } from "./map/utilities/displayGeoJSON";

export * from "./side_menu";
export let map;

export function toggle_dropdown() {
    var dropdown = document.getElementById("dropdown-menu");
    dropdown.hidden = !dropdown.hidden;
}

window.onload = () => {
    map = new Map();
    map.loadMap();

    // First retrieve the road 'chunks'
    getRoadsMetadataChunks()
        .then(chunks => {
            // Get smaller chunks first
            chunks = chunks.sort((chunkA, chunkB) => { return chunkA.road_type__count - chunkB.road_type__count; });
            const geoDataPromises = chunks.map(chunk => (getRoadsMetadata(chunk.road_type)));
            geoDataPromises.push(getGeoJsonDetails());

            Promise.all(geoDataPromises).then(values => {
                let geoJsonDetails = values.pop();
                let roadsLookup = values;
        
                // now we have our metadata we can intialize the data table
                initializeDataTable(Object.values(roadsLookup[0]).map(r => r.toObject()));
        
                // retrieve each geojson file
                return Promise.all(geoJsonDetails.map(geoJsonDetail => {
                    return getGeoJson(
                        geoJsonDetail
                    ).then(geoJson => {
                        // add in road metadata
                        roadsLookup.forEach(roadsMetadata => {
                            populateGeoJsonProperties(geoJson, roadsMetadata);
                        });
        
                        // add to map
                        map.addMapData(geoJson);
                    })
                }));
            }, err => console.log(err));

        });
};

// riot mounting point
riot.component(Example)(document.getElementById('riot-edit'));

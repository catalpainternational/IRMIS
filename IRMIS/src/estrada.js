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

let table;

function getAllTheRest(geoDataPromises, roadsLookup) {
    Promise.all(geoDataPromises).then(values => {
        let geoJsonDetails = values.pop();
        roadsLookup = roadsLookup.concat(values);

        // Add in the additional roads to the table
        values.forEach(roadValues => {
            const roadObjects = Object.values(roadValues).map(r => r.toObject());
            table.rows.add(roadObjects).draw();
        });

        // retrieve each geojson file
        return Promise.all(geoJsonDetails.map(geoJsonDetail => {
            return getGeoJson(
                geoJsonDetail
            ).then(geoJson => {
                // add in road metadata to the geoJson
                roadsLookup.forEach(roadsMetadata => {
                    populateGeoJsonProperties(geoJson, roadsMetadata);
                });

                // add to map
                map.addMapData(geoJson);
            })
        }));
    }, err => console.log(err));
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

            const firstMetadataChunk = geoDataPromises.shift();

            let roadsLookup = [];

            firstMetadataChunk.then(roads => {
                roadsLookup.push(roads);

                // now we have our metadata we can intialize the data table
                table = initializeDataTable(Object.values(roadsLookup[0]).map(r => r.toObject()));

                getAllTheRest(geoDataPromises, roadsLookup);
            });
        });
};

// riot mounting point
riot.component(Example)(document.getElementById('riot-edit'));

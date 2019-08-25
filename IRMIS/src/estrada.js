import "./styles/irmis.scss";

import { Map } from "./map/map";
import { getRoadMetadata, getGeoJsonDetails, getGeoJson, populateGeoJsonProperties } from "./assets/assets_api.js";
import { initializeDataTable } from "./table";
import { addToMap } from "./map/map_simple";

export * from "./table";
export * from "./side_menu";
export { filterFeatures } from "./map/map_simple";
export let map;


window.onload = () => {
    map = new Map();
    map.loadMap();

    // First retrieve the road metadata, and the urls of the geojson files
    Promise.all([
        getRoadMetadata(),
        getGeoJsonDetails(),
    ]).then(values => {
        let roadsLookup = values[0];
        let geoJsonDetails = values[1];

        // now we have our metadata we can intialize the data table
        initializeDataTable(Object.values(roadsLookup).map(r => r.toObject()));
        
        // retrieve each geojson file
        return Promise.all(geoJsonDetails.map(geoJsonDetail => { 
            return getGeoJson(
                geoJsonDetail
            ).then(geoJson => {
                // add in road metadata
                populateGeoJsonProperties(geoJson, roadsLookup);
                
                // add to map
                addToMap(geoJson, map.lMap);
            })
        }));
    }, err => console.log(err));

};

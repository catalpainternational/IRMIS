import "./styles/irmis.scss";

import { Map } from "./map/map";
import { getRoadsMetadata, getGeoJsonDetails, getGeoJson, populateGeoJsonProperties } from "./assets/assets_api.js";
import { initializeDataTable } from "./table";

export { filterFeatures } from "./map/utilities/filterGeoJSON";
export { geoFeatureGroups } from "./map/utilities/displayGeoJSON";

export * from "./table";
export * from "./side_menu";

export let map;


window.onload = () => {
    map = new Map();
    map.loadMap();

    // First retrieve the road metadata, and the urls of the geojson files
    Promise.all([
        getRoadsMetadata(),
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
                map.addMapData(geoJson);
            })
        }));
    }, err => console.log(err));

};

import "babel-polyfill";
import * as riot from "riot";

import Edit_Base from "./riot/edit_base.riot";

import "./styles/irmis.scss";

import { getGeoJsonDetails, getGeoJsonDetail } from "./assets/geoJsonAPI.js";

import { getRoad } from "./roadManager";
import "./table";
import "./side_menu";
import "./top_menu";
import { Map } from "./map/map";

const estradaMap = new Map();

window.onload = () => {
    // Set up the map and table - but without any data for either
    estradaMap.loadMap();
    
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
    let m = /#edit\/(\d*)/.exec(location.hash);
    if (m !== null) {
        var roadPromise = getRoad(m[1]);
        riot.mount('edit_base', { roadPromise });
        document.getElementById('view-content').hidden = true;
    } else {
        riot.unmount('edit_base', true);
        document.getElementById('view-content').hidden = false;
    }
}

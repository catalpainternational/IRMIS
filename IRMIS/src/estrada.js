import "babel-polyfill";
import * as riot from "riot";

import Data_Table from "./riot/data_table.riot";
import Edit_Base from "./riot/edit_base.riot";

import "./styles/estrada.scss";
import "./styles/vendor.scss";

import { getGeoJsonDetails, getGeoJsonDetail } from "./assets/geoJsonAPI.js";

import { getRoad } from "./roadManager";
import "./table";
import "./side_menu";
import "./top_menu";
import { Map } from "./map/map";

const estradaMap = new Map();

window.addEventListener("load", () => {
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

    riot.register("data_table", Data_Table);
    riot.register("edit_base", Edit_Base);
    window.goBack = () => {};
    hashCheck();
});

window.addEventListener("hashchange", () => {
    hashCheck();
});

function hashCheck() {
    let m = /#edit\/(\d*)\/(\w+)/.exec(location.hash);
    if (m !== null && !document.getElementById("edit-base")) {
        var roadPromise = getRoad(m[1]);
        riot.mount("edit_base", { roadPromise: roadPromise, page: m[2] });
        document.getElementById("view-content").hidden = true;
    } else if (m === null) {
        riot.unmount("edit_base", true);
        document.getElementById("view-content").hidden = false;
    }
}

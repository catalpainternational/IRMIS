import "babel-polyfill";
import * as riot from "riot";

import Reports_Base from "./riot/reports_base.riot";
import Edit_Base from "./riot/edit_base.riot";

import "./styles/estrada.scss";
import "./styles/vendor.scss";

import { getGeoJsonDetails, getGeoJsonDetail } from "./assets/geoJsonAPI.js";

import { getRoad } from "./roadManager";
import "./table";
import "./side_menu";
import "./top_menu";
import { Map } from "./map/map";

export const estradaMap = new Map();

import "./dayjs/dayjs";


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
                        // add in road metadata to the GeoJSON that we'll need
                        // for filtering and for styling
                        geoJson.features.forEach((feature) => {
                            feature.properties.id = Number(feature.properties.pk) || 0;
                            feature.properties.featureType = "Road";
                        });
                        
                        // add to map
                        estradaMap.addMapData(geoJson);
                    });
            });
        });

    riot.register("reports_base", Reports_Base);
    riot.register("edit_base", Edit_Base);

    window.goBack = () => {};

    hashCheck();
});

window.addEventListener("hashchange", () => {
    hashCheck();
});

function hashCheck() {
    const mainContent = document.getElementById("view-content");
    const reportsBase = document.getElementById("reports");
    const editBase = document.getElementById("edit-base");

    let reportsHash = /#reports/.exec(location.hash);
    let editHash = /#edit\/(\d*)\/(\w+)/.exec(location.hash);

    if (editHash !== null && !editBase) {
        var roadPromise = getRoad(editHash[1]);
        riot.unmount("reports_base", true);
        riot.mount("edit_base", { roadPromise: roadPromise, page: editHash[2] });
        mainContent.hidden = true;
    } else if (reportsHash !== null && !reportsBase) {
        riot.unmount("edit_base", true);
        riot.mount("reports_base");
        mainContent.hidden = true;
    } else if (editHash === null && reportsHash === null) {
        riot.unmount("reports_base", true);
        riot.unmount("edit_base", true);
        mainContent.hidden = false;
    }
}

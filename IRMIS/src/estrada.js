import "babel-polyfill";
import * as riot from "riot";

import Planning_Base from "./riot/planning_base.riot.html";
import Reports_Base from "./riot/reports_base.riot.html";
import Data_Table from "./riot/data_table.riot.html";
import Edit_Base from "./riot/edit_base.riot.html";

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
                const featureType = geoJsonDetail.key || "Road";
                getGeoJsonDetail(geoJsonDetail)
                    .then(geoJson => {
                        // add in road metadata to the GeoJSON that we'll need
                        // for filtering and for styling
                        geoJson.features.forEach((feature) => {
                            feature.properties.id = Number(feature.properties.pk) || 0;
                            feature.properties.featureType = featureType;
                        });

                        // add to map
                        estradaMap.addMapData(geoJson);
                    });
            });
        });

    riot.register("planning_base", Planning_Base);
    riot.register("reports_base", Reports_Base);
    riot.register("data_table", Data_Table);

    if (window.canEdit) {
        riot.register("edit_base", Edit_Base);
        // add listener since editing is allowed
        window.addEventListener("hashchange", () => {
            hashCheck();
        });
        hashCheck();
    }

    window.goBack = () => {};

    hashCheck();
});

window.addEventListener("hashchange", () => {
    hashCheck();
});

function hashCheck() {
    const mainContent = document.getElementById("view-content");
    const planningBase = document.getElementById("planning");
    const reportsBase = document.getElementById("reports");
    const editBase = document.getElementById("edit-base");

    let planningHash = /#planning/.exec(location.hash);
    let reportsHash = /#reports\/(\d?)/.exec(location.hash);
    let editHash = /#edit\/(\d*)\/(\w+)/.exec(location.hash);

    if (editHash !== null && !editBase) {
        const roadPromise = getRoad(editHash[1]);
        if (planningBase) riot.unmount("planning_base", true);
        if (reportsBase) riot.unmount("reports_base", true);
        riot.mount("edit_base", { roadPromise: roadPromise, page: editHash[2] });
        mainContent.hidden = true;
    } else if (reportsHash !== null && !reportsBase) {
        if (planningBase) riot.unmount("planning_base", true);
        if (editBase) riot.unmount("edit_base", true);
        riot.mount("reports_base", { page: reportsHash[1] });
        mainContent.hidden = true;
    } else if (planningHash !== null && !planningBase) {
        if (editBase) riot.unmount("edit_base", true);
        if (reportsBase) riot.unmount("reports_base", true);
        riot.mount("planning_base");
        mainContent.hidden = true;
    } else if (editHash === null && reportsHash === null && planningHash === null) {
        if (planningBase) riot.unmount("planning_base", true);
        if (reportsBase) riot.unmount("reports_base", true);
        if (editBase) riot.unmount("edit_base", true);
        mainContent.hidden = false;
    }
}

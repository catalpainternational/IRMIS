// polyfills - babel-polyfill is core-js
import "core-js/stable";
import "regenerator-runtime/runtime";
import "./polyfills/array_from";
import "./polyfills/nodelist_foreach";

import "./dayjs/dayjs";
import * as riot from "riot";

import Loading from "./riot/loading.riot";
import Planning_Base from "./riot/planning_base.riot";
import Reports_Base from "./riot/reports_base.riot";
import Data_Table from "./riot/data_table.riot";
import Edit_Base from "./riot/edit_base.riot";
import TrafficDataDetails from "./riot/traffic_data_details.riot";
import MediaDetailsBox from "./riot/media_details_box.riot";

import { getGeoJsonDetails, getGeoJsonDetail } from "./assets/geoJsonAPI.js";

import { getRoad } from "./roadManager";
import { getStructure } from "./structureManager";

import "./table";
import "./side_menu";
import "./top_menu";
import { Map } from "./map/map";

import "./translations";

import "./styles/estrada.scss";
import "./styles/vendor.scss";

// Import the monkey patches for the protobuf definitions
// Whenever updating protoc, please review the need for these monkey patches
import "./assets/models/monkeyPatch";

export const estradaMap = new Map();

riot.register("loading", Loading);
riot.mount("loading", { modalId: "assets-loading" });

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
                            feature.properties.featureType = featureType;
                            let idPrefix = "";
                            switch (featureType) {
                                case "bridge":
                                    idPrefix = "BRDG-";
                                    break;
                                case "culvert":
                                    idPrefix = "CULV-";
                                    break;
                                case "drift":
                                    idPrefix = "DRFT-";
                                    break;
                                default:
                                    idPrefix = "";
                                    break;
                            }
                            feature.properties.id = idPrefix + (Number(feature.properties.pk) || 0);
                        });

                        // add to map
                        estradaMap.addMapData(geoJson);
                    });
            });
        });

    riot.register("planning_base", Planning_Base);
    riot.register("reports_base", Reports_Base);
    riot.register("data_table", Data_Table);

    riot.register("traffic_data_details", TrafficDataDetails);
    riot.mount("traffic_data_details");

    riot.register("media_details_box", MediaDetailsBox);
    riot.mount("media_details_box");

    if (window.canEdit) {
        riot.register("edit_base", Edit_Base);
    }

    window.goBack = () => { };

    hashCheck();
});

window.addEventListener("hashchange", () => {
    hashCheck();
});

function hashCheck() {
    const mainContent = document.getElementById("view-content");
    const planningBase = document.getElementById("planning");
    const reportsBase = document.getElementById("dashboard") || document.getElementById("report-assets") || document.getElementById("report-contracts");
    const editBase = document.getElementById("edit-base");

    let planningHash = /#planning\/(.*)\/?/.exec(location.hash);
    let reportsHash = /#reports\/(\w+)\/(\d*)/.exec(location.hash);
    let editHash = /#edit\/(\w+)\/(\d*)\/(\w+)/.exec(location.hash);

    if (editHash !== null && !editBase) {
        if (planningBase) riot.unmount("planning_base", true);
        if (reportsBase) riot.unmount("reports_base", true);
        if (editHash[1] === "BRDG" || editHash[1] === "CULV" || editHash[1] === "DRFT") {
            const globalId = editHash[1] + "-" + editHash[2];
            const structurePromise = getStructure(globalId);
            riot.mount("edit_base", { structurePromise: structurePromise, assetType: editHash[1], page: editHash[3] });
        } else {
            const roadPromise = getRoad(editHash[2]);
            riot.mount("edit_base", { roadPromise: roadPromise, assetType: editHash[1], page: editHash[3] });
        }
        mainContent.hidden = true;
    } else if (reportsHash !== null && !reportsBase) {
        if (planningBase) riot.unmount("planning_base", true);
        if (editBase) riot.unmount("edit_base", true);
        riot.mount("reports_base", { page: reportsHash[1], pageId: reportsHash[2] });
        mainContent.hidden = true;
    } else if (planningHash !== null && !planningBase) {
        if (editBase) riot.unmount("edit_base", true);
        if (reportsBase) riot.unmount("reports_base", true);
        riot.mount("planning_base", { page: planningHash[1] });
        mainContent.hidden = true;
    } else if (editHash === null && reportsHash === null && planningHash === null) {
        if (planningBase) riot.unmount("planning_base", true);
        if (reportsBase) riot.unmount("reports_base", true);
        if (editBase) riot.unmount("edit_base", true);
        mainContent.hidden = false;
    }
}

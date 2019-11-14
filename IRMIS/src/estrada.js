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

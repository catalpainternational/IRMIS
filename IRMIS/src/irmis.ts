import "./styles/irmis.scss";

import { Map } from "./map/map";

export * from "./table";
export * from "./side_menu";
export * from "./assets/assets_api";

export let map: Map;

window.onload = () => {
    map = new Map();
    map.loadMap();

    // This is sample code to get a selection of available roads and display them
    // The only line that matters is
    // map.loadMapData(roadId)
    const minRoadIdInDB = 1;
    const maxRoadIdInDB = minRoadIdInDB + 182;
    for (let roadId = minRoadIdInDB; roadId <= maxRoadIdInDB; roadId++) {
        // This returns a Promise, which we currently don't care about
        map.loadMapData(roadId);
    }
};

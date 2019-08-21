import "./styles/irmis.scss";

export * from './roads/roads_api';

import { Map } from "./map/map";

window.onload = () => {
    const map = new Map();
    map.loadMap();

    const geoJsonSource = `${location.origin}/assets/roads/`;
    const maxRoadIdInDB = 182;
    for (let id = 1; id <= maxRoadIdInDB; id++) {
        // This returns a Promise, which we currently don't care about
        map.loadMapData(geoJsonSource, id);
    }
};

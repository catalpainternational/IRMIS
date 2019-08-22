import "./styles/irmis.scss";

import { Map } from "./map/map";

export * from './table';
export * from './side_menu';
export * from './roads/roads_api';

window.onload = () => {
    const map = new Map();
    map.loadMap();

    const geoJsonSource = `${location.origin}/assets/roads/`;
    const maxRoadIdInDB = 182;
    for (let id = 1; id <= maxRoadIdInDB; id++) {
        // This returns a Promise, which we currently do not care about
        map.loadMapData(geoJsonSource, id);
    }
};

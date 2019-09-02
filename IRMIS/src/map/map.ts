// tslint:disable-next-line: max-line-length
import { GeoJSON } from "geojson";
import * as L from "leaflet";

import { Config } from "./config";
import { BaseLayers } from "./layers/BaseLayers";
import { displayGeoJSON } from "./utilities/displayGeoJSON";

export class Map {
    private lMap = {} as L.Map;
    private zoomControl = {} as L.Control.Zoom;
    private layerControl = {} as L.Control.Layers;

    /** Call this in window.onload, or after */
    public loadMap(): L.Map {
        this.lMap = L.map("map-irmis", { maxBounds: Config.tlBounds, zoomControl: false, attributionControl: false }).setView(Config.tlCenter, 8);

        // Add back in the zoom control
        this.zoomControl = L.control.zoom({ position: "topright" });
        this.zoomControl.addTo(this.lMap);

        // Set up the baseLayers and the layer control
        const bl = BaseLayers.baseLayers;
        bl["Street OSM HOT"].addTo(this.lMap);
        this.layerControl = L.control.layers(bl, {});

        return this.lMap;
    }

    public addMapData(geoJSON: GeoJSON) {
        try {
            displayGeoJSON(this.lMap, this.layerControl, geoJSON);
            return Promise.resolve(true);
        } catch (error) {
            return Promise.reject(error);
        }
    }
}

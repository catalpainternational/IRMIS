// tslint:disable-next-line: max-line-length
import { GeoJSON } from "geojson";
import * as L from "leaflet";

import { Config } from "./config";
import { BaseLayers } from "./layers/BaseLayers";
import { displayGeoJSON } from "./utilities/displayGeoJSON";

export class Map {
    private lMap = {} as L.Map;
    private zoomControl = {} as L.Control.Zoom;
    private currentLayer = {} as L.TileLayer;

    /** Call this in window.onload, or after */
    public loadMap(): L.Map {
        this.lMap = L.map("map-irmis", { maxBounds: Config.tlBounds, zoomControl: false }).setView(Config.tlCenter, 8);

        // Add back in the zoom control
        this.zoomControl = L.control.zoom({ position: "topright" });
        this.zoomControl.addTo(this.lMap);

        // Set up the baseLayers and add the selected one to the map
        const bl = BaseLayers.baseLayers;
        this.currentLayer = bl[Config.preferredBaseLayerName];
        this.currentLayer.addTo(this.lMap);

        return this.lMap;
    }

    public addMapData(geoJSON: GeoJSON) {
        try {
            displayGeoJSON(geoJSON);
            return Promise.resolve(true);
        } catch (error) {
            return Promise.reject(error);
        }
    }
}

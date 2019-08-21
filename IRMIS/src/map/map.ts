// tslint:disable-next-line: max-line-length
import { Feature, FeatureCollection, GeoJSON, LineString, MultiLineString, MultiPoint, MultiPolygon, Point, Polygon } from "geojson";
import * as L from "leaflet";

import { Config } from "./config";
import { BaseLayers } from "./layers/BaseLayers";
import { displayGeoJSON, getGeoJSON } from "./utilities/getGeoJSON";

export class Map {
    private lMap = {} as L.Map;
    private zoomControl = {} as L.Control.Zoom;
    private layerControl = {} as L.Control.Layers;

    /** Call this in window.onload, or after */
    public loadMap(): L.Map {
        this.lMap = L.map("mapirmis", { maxBounds: Config.tlBounds, zoomControl: false }).setView(Config.tlCenter, 9);

        // Add back in the zoom control
        this.zoomControl = L.control.zoom({ position: "bottomleft" });
        this.zoomControl.addTo(this.lMap);

        // Set up the baseLayers and the layer control
        const bl = BaseLayers.baseLayers;
        bl["Street OSM Mapnik"].addTo(this.lMap);
        this.layerControl = L.control.layers(bl, {});
        this.layerControl.addTo(this.lMap);

        return this.lMap;
    }

    public async loadMapData(geoJsonSource: string, id?: number) {
        if (id) {
            try {
                const json = await getGeoJSON(geoJsonSource, id);
                if (json) {
                    const geoJSON = json as GeoJSON;
                    const firstCoords = this.getFirstCoords(geoJSON);
                    if (firstCoords[0] >= 0 && firstCoords[0] < 500) {
                        displayGeoJSON(this.lMap, this.layerControl, json);

                        return Promise.resolve(true);
                    }
                }

                return Promise.resolve(false);
            } catch (error) {
                return Promise.reject(error);
            }
        }

        // No id, so just get everything
        this.getGeoJSONRecursively(geoJsonSource, 1)
            .then(() => {
                // Handle 'zoom to extents' (AKA fitBounds) for each type of data
                this.lMap.addEventListener("overlayadd", (event: L.LeafletEvent) => {
                    const overlayEvent = event as L.LayersControlEvent;
                    const layerbounds = (overlayEvent.layer as L.FeatureGroup).getBounds();

                    try {
                        this.lMap.fitBounds(layerbounds);
                    } catch {
                        // throw it away
                    }
                });
            })
            .catch();
    }

    private getFirstCoords(geoJSON: GeoJSON): number[] {
        switch (geoJSON.type) {
            case "Feature":
                return this.getFirstCoords((geoJSON as Feature).geometry);
            case "FeatureCollection":
                return this.getFirstCoords((geoJSON as FeatureCollection).features[0].geometry);
            case "Point":
                return (geoJSON as Point).coordinates;
            case "LineString":
                return (geoJSON as LineString).coordinates[0];
            case "MultiPoint":
                return (geoJSON as MultiPoint).coordinates[0];
            case "Polygon":
                return (geoJSON as Polygon).coordinates[0][0];
            case "MultiLineString":
                return (geoJSON as MultiLineString).coordinates[0][0];
            case "MultiPolygon":
                return (geoJSON as MultiPolygon).coordinates[0][0][0];
        }

        return [-1, -1];
    }

    // tslint:disable-next-line: max-line-length
    private async getGeoJSONRecursively(geoJsonSource: string, id: number, errorCount: number = 0): Promise<any> {
        if (errorCount > 10) {
            return Promise.resolve(false);
        }

        try {
            const json = await getGeoJSON(geoJsonSource, id);
            if (json) {
                const geoJSON = json as GeoJSON;
                const firstCoords = this.getFirstCoords(geoJSON);
                if (firstCoords[0] >= 0 && firstCoords[0] < 500) {
                    displayGeoJSON(this.lMap, this.layerControl, json);
                }

                errorCount = 0;
            } else {
                errorCount++;
            }
            id++;
            return this.getGeoJSONRecursively(geoJsonSource, id, errorCount);
        } catch (error) {
            return Promise.resolve(false);
        }
    }
}

// tslint:disable-next-line: max-line-length
import { Feature, GeoJSON, Geometry } from "geojson";
import * as L from "leaflet";

import { Config } from "./config";
import { BaseLayers } from "./layers/BaseLayers";
import { KnownGeometries } from "./layers/KnownGeometries";
import { getFeatureType } from "./utilities/displayGeoJSON";
// tslint:disable-next-line: max-line-length
import { CreateOverlayControlName, FallbackLayerStyle, FixLayerStyleDefaults, styleGeometry, stylePoint } from "./utilities/leaflet-style";

export let geoFeatureGroups: { [name: string]: L.FeatureGroup } = {};
export let featureLookup: { [name: string]: Feature<Geometry, any> } = {};
export let layerLookup: { [name: string]: L.Layer } = {};

export class Map {
    private lMap = {} as L.Map;
    private zoomControl = {} as L.Control.Zoom;
    private currentLayer = {} as L.TileLayer;
    private roadManager = {} as any;

    constructor(options: any) {
        this.roadManager = options.roadManager;
    }

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
            this.displayGeoJSON(geoJSON);
            return Promise.resolve(true);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    public invalidateSize() {
        this.lMap.invalidateSize();
    }

    private displayGeoJSON(json: GeoJSON): Promise<any> {
        const featureType = getFeatureType(json);

        if (KnownGeometries.Excluded.indexOf(featureType) !== -1) {
            return Promise.resolve(true);
        }

        const geoFeatureGroupExists = !!geoFeatureGroups[featureType];
        const geoFeatureGroup = geoFeatureGroups[featureType] || new L.FeatureGroup();

        // Get the style
        const styleRecord = KnownGeometries.Known[featureType]
            ? KnownGeometries.Known[featureType]
            : FallbackLayerStyle(featureType);
        FixLayerStyleDefaults(styleRecord);
        const mapPane = "" + (styleRecord.mapPane || styleRecord.featureType);

        // Assemble the presentation options & styling
        const geoJsonOptions: L.GeoJSONOptions = {
            onEachFeature: registerFeature,
            pane: mapPane === "undefined" ? undefined : mapPane,
            pointToLayer: (feature: GeoJSON.Feature<GeoJSON.Point>, latlng: L.LatLng) =>
                stylePoint(feature, latlng, styleRecord.pointToLayer),
            style: (feature?: GeoJSON.Feature<GeoJSON.GeometryObject, any>): L.PathOptions =>
                styleGeometry(feature, styleRecord),
        };

        // Actually build the GeoJSON layer
        const geoLayer = L.geoJSON(json, geoJsonOptions).bindPopup(this.getPopupMethod());

        // Add it to the feature group
        geoFeatureGroup.addLayer(geoLayer);

        if (!geoFeatureGroupExists) {
            // New feature group - add it to the map
            geoFeatureGroup.addTo(this.lMap);
            geoFeatureGroups[featureType] = geoFeatureGroup;
        }

        return Promise.resolve(true);
    }

    private getPopupMethod() {
        const roadManager = this.roadManager;
        return function(this: Map, layer: any): string {
            const id = parseInt(layer.feature.properties.pk, 10);
            return roadManager.roadPopup(id);
        };
    }
}

function registerFeature(feature: Feature<Geometry, any>, layer: L.Layer) {
    featureLookup[feature.properties.pk] = feature;
    layerLookup[feature.properties.pk] = layer;
}

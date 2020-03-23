import bbox from "@turf/bbox";
import envelope from "@turf/envelope";
import { AllGeoJSON } from "@turf/helpers";
import { FeatureCollection } from "geojson";

import { Feature, GeoJSON, Geometry } from "geojson";
import * as L from "leaflet";

import { Config } from "./config";

import { BaseLayers } from "./layers/BaseLayers";
import { KnownGeometries } from "./layers/KnownGeometries";
import { getFilterStyles } from "./utilities/filterGeoJSON";
import { getFeatureType } from "./utilities/propertiesGeoJSON";

import { FallbackLayerStyle, FixLayerStyleDefaults, styleGeometry, stylePoint } from "./utilities/leaflet-style";

import { GetDataForMapPopup } from "../table";

import { dispatch } from "../assets/utilities";

/** The collection of all GeoJSON elements currently added to the map,
 * organised by their featureType
 */
export let geoFeatureGroups: { [name: string]: L.FeatureGroup } = {};

export let featureLookup: { [name: string]: Feature<Geometry, any> } = {};
export let layerLookup: { [name: string]: L.Layer } = {};

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

        // Set the minimum zoom level
        this.lMap.setMinZoom(this.lMap.getZoom());

        // Set up the baseLayers and add the selected one to the map
        const bl = BaseLayers.baseLayers;
        this.currentLayer = bl[Config.preferredBaseLayerName];
        this.currentLayer.addTo(this.lMap);

        document.addEventListener("estrada.road.sideMenu.viewChanged", () => {
            this.lMap.invalidateSize();
        });

        document.addEventListener("estrada.structure.sideMenu.viewChanged", () => {
            this.lMap.invalidateSize();
        });

        document.addEventListener("estrada.road.filter.applied", (data: Event) => {
            this.handleFilter(data);
        });

        document.addEventListener("estrada.structure.filter.applied", (data: Event) => {
            this.handleFilter(data);
        });

        document.addEventListener("estrada.map.idFilter.applied", (data: Event) => {
            this.handleFilter(data);
        });

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

    private handleFilter(data: Event) {
        const featureZoomSet: FeatureCollection = { type: "FeatureCollection", features: [] };
        const featureTypeSet: any = {};
        Object.values(featureLookup).forEach((feature: any) => {
            const featureId: string = feature.properties.id;
            const geoLayer = layerLookup[featureId] as L.GeoJSON;

            const switchStyle = !!(data as CustomEvent).detail.idMap[featureId];
            if (switchStyle) {
                featureZoomSet.features.push(feature);
            }

            const featureType: string = feature.properties.featureType || "Road";
            if (!featureTypeSet[featureType]) {
                featureTypeSet[featureType] = getFilterStyles(featureType);
            }
            const layerFilterStyles = featureTypeSet[featureType];
            feature.properties.switchStyle = switchStyle;
            geoLayer.setStyle(switchStyle ? layerFilterStyles.styleOn : layerFilterStyles.styleOff);
        });

        let bb = Config.tlBBox;
        if (featureZoomSet.features.length) {
            const allCoords = featureZoomSet.features.forEach((feature) => {
                feature.type
            })
            const bounds = envelope(featureZoomSet as AllGeoJSON);
            bb = bbox(bounds) as number[];
        }

        // Don't use flyToBounds
        // - it sounds nice, but screws up tile and geoJSON alignment when the zoom level remains the same
        this.lMap.fitBounds(new L.LatLngBounds([bb[1], bb[0]], [bb[3], bb[2]]));
    }

    private registerFeature(feature: Feature<Geometry, any>, layer: L.Layer) {
        featureLookup[feature.properties.id] = feature;
        layerLookup[feature.properties.id] = layer;
        layer.on("click", (e) => {
            const clickedFeature = e.target.feature;
            const featureId = clickedFeature.properties.id;
            const featureType = clickedFeature.properties.featureType || "";

            if (typeof clickedFeature.properties.switchStyle === "undefined") {
                clickedFeature.properties.switchStyle = true;
            }

            if (clickedFeature.properties.switchStyle) {
                // This feature will be in the table
                const assetType = ["bridge", "culvert"].includes(featureType) ? "STRC" : "ROAD";
                const eventName = assetType === "STRC"
                    ? "estrada.structureTable.rowSelected"
                    : "estrada.roadTable.rowSelected";
                dispatch(eventName, { detail: { rowId: featureId, featureType, assetType } });
            }
        });
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
            onEachFeature: this.registerFeature,
            pane: mapPane === "undefined" ? undefined : mapPane,
            pointToLayer: (feature: GeoJSON.Feature<GeoJSON.Point>, latlng: L.LatLng) =>
                stylePoint(feature, latlng, styleRecord.pointToLayer),
            style: (feature?: GeoJSON.Feature<GeoJSON.GeometryObject, any>): L.PathOptions =>
                styleGeometry(feature, styleRecord),
        };

        // Actually build the GeoJSON layer, and bind the popup behaviour
        const geoLayer = L.geoJSON(json, geoJsonOptions).bindPopup(this.getPopup);

        // Add it to the feature group
        geoFeatureGroup.addLayer(geoLayer);

        if (!geoFeatureGroupExists) {
            // New feature group - add it to the map
            geoFeatureGroup.addTo(this.lMap);
            geoFeatureGroups[featureType] = geoFeatureGroup;
        }

        return Promise.resolve(true);
    }

    private getPopup(layer: any): string {
        const id = layer.feature.properties.id;
        const featureType = layer.feature.properties.featureType || "";

        const popupData = GetDataForMapPopup(id, featureType);

        let html = "";

        popupData.forEach((popupDetail) => {
            html = `<span class="popup"><span class="popup label">${popupDetail.label}`;
            html += popupDetail.value
                ? `: </span><span class="popup value">${popupDetail.value}</span></span>`
                : "</span></span>";
        });

        return html;
    }
}

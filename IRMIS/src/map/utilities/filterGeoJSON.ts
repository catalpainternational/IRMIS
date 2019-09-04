import bbox from "@turf/bbox";
import envelope from "@turf/envelope";
import { AllGeoJSON } from "@turf/helpers";
import { FeatureCollection, GeoJsonProperties } from "geojson";
import * as L from "leaflet";

import { featureLookup, fitBounds, layerLookup } from "./displayGeoJSON";
import { FallbackLayerStyle, FixLayerStyleDefaults } from "./leaflet-style";

import { KnownGeometries } from "../layers/KnownGeometries";

function getFilterStyles(layerName: string): { [name: string]: L.PathOptions | L.StyleFunction<any> } {
    const layerNameOn = `${layerName}.on`;
    const layerNameOff = `${layerName}.off`;

    const styleOn = KnownGeometries.Known[layerNameOn] || KnownGeometries.Known[layerName]
        ? KnownGeometries.Known[layerNameOn] || KnownGeometries.Known[layerName]
        : FallbackLayerStyle(layerNameOn);
    FixLayerStyleDefaults(styleOn);

    const styleOff = KnownGeometries.Known[layerNameOff]
        ? KnownGeometries.Known[layerNameOff]
        : FallbackLayerStyle(layerNameOff);
    FixLayerStyleDefaults(styleOff);

    return {styleOn: styleOn.style, styleOff: styleOff.style};
}

/** Applies the relevant '.on' or '.off' style for this layer as defined in KnownGeometries
 * based upon the returned value from the supplied filter function
 */
export function filterFeatures(filterFunc: (properties: GeoJsonProperties) => boolean, featureType: string) {
    const layerName = featureType || "Road";
    const layerFilterStyles = getFilterStyles(layerName);

    const featureZoomSet: FeatureCollection = {type: "FeatureCollection", features: []};

    Object.values(featureLookup).forEach((feature: any) => {
        const geoProperties = feature.properties;
        const geoLayer = layerLookup[geoProperties.pk] as L.GeoJSON;

        const styleSwitch = filterFunc(geoProperties);
        const styleToSet = styleSwitch ? layerFilterStyles.styleOn : layerFilterStyles.styleOff;

        if (styleSwitch) {
            featureZoomSet.features.push(feature);
        }

        geoLayer.setStyle(styleToSet);
    });

    if (featureZoomSet.features.length) {
        const bounds = envelope(featureZoomSet as AllGeoJSON);
        const bb = bbox(bounds);
        fitBounds(new L.LatLngBounds([bb[1], bb[0]], [bb[3], bb[2]]));
    }
}

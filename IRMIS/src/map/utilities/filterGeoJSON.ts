import { GeoJsonProperties } from "geojson";
import * as L from "leaflet";

import { featureLookup, layerLookup } from "./displayGeoJSON";
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

    Object.values(featureLookup).forEach((feature: any) => {
        const geoProperties = feature.properties;
        const geoLayer = layerLookup[geoProperties.pk] as L.GeoJSON;

        geoLayer.setStyle(filterFunc(geoProperties) ? layerFilterStyles.styleOn : layerFilterStyles.styleOff);
    });
}

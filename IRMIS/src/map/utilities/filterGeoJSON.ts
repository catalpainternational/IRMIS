import * as L from "leaflet";

import { FallbackLayerStyle, FixLayerStyleDefaults } from "./leaflet-style";

import { KnownGeometries } from "../layers/KnownGeometries";

export function getFilterStyles(layerName: string): { [name: string]: L.PathOptions | L.StyleFunction<any> } {
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

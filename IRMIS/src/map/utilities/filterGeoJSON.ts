import * as L from "leaflet";

import { FallbackLayerStyle, FixLayerStyleDefaults } from "./leaflet-style";

import { KnownGeometries } from "../layers/KnownGeometries";
import { GeoDataStyle, PointToLayerStyle } from "models/geo-data-style";

export function getFilterStyles(layerName: string): { [name: string]: PointToLayerStyle } {
    const layerNameOn = `${layerName}.on`;
    const layerNameOff = `${layerName}.off`;

    const styleOn: GeoDataStyle = KnownGeometries.Known[layerNameOn] || KnownGeometries.Known[layerName]
        ? KnownGeometries.Known[layerNameOn] || KnownGeometries.Known[layerName]
        : FallbackLayerStyle(layerNameOn);
    FixLayerStyleDefaults(styleOn);

    const styleOff: GeoDataStyle = KnownGeometries.Known[layerNameOff]
        ? KnownGeometries.Known[layerNameOff]
        : FallbackLayerStyle(layerNameOff);
    FixLayerStyleDefaults(styleOff);

    return { styleOn: styleOn.style as PointToLayerStyle, styleOff: styleOff.style as PointToLayerStyle };
}

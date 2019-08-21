import * as L from "leaflet";

import { KnownGeometries } from "../layers/KnownGeometries";
// tslint:disable-next-line: max-line-length
import { CreateOverlayControlName, FallbackLayerStyle, FixLayerStyleDefaults, styleGeometry, stylePoint } from "../utilities/leaflet-style";

export let geoFeatureGroups: any = {};
export let geoJsonFiles = Array<string>();

export async function getGeoJSON(geoSourceUrl: string, id: number): Promise<any> {
    try {
        const response = await fetch(`${geoSourceUrl}${id}`, {mode: "no-cors"});
        if (!response.ok) {
            return Promise.resolve(undefined);
        }
        const responsejson = response.json();
        if (!responsejson) {
            // no json
            return Promise.resolve(undefined);
        }
        return Promise.resolve(responsejson);
    } catch (error) {
        // TODO: log this error, network error
        return Promise.reject(id);
    }
}

export function displayGeoJSON(mymap: L.Map, layerControl: L.Control.Layers, json: any): Promise<any> {
    const layerName = "not set"; // getLayerNameFromGeoJSONProperties(json);

    if (KnownGeometries.Excluded.indexOf(layerName) !== -1) {
        return Promise.resolve(true);
    }

    const geoFeatureGroupExists = !!geoFeatureGroups[layerName];
    const geoFeatureGroup = geoFeatureGroups[layerName] || new L.FeatureGroup();

    // Get the style
    const styleRecord = KnownGeometries.Known[layerName]
        ? KnownGeometries.Known[layerName]
        : FallbackLayerStyle(layerName);
    FixLayerStyleDefaults(styleRecord);
    const mapPane = "" + (styleRecord.map_pane || styleRecord.display_sequence || styleRecord.geo_type);

    // Assemble the presentation options & styling
    const geoJsonOptions: L.GeoJSONOptions = {
        pane: mapPane === "undefined" ? undefined : mapPane,
        pointToLayer: (feature: GeoJSON.Feature<GeoJSON.Point>, latlng: L.LatLng) =>
            stylePoint(feature, latlng, styleRecord.style.pointToLayer),
        style: (feature?: GeoJSON.Feature<GeoJSON.GeometryObject, any>): L.PathOptions =>
            styleGeometry(feature, styleRecord),
    };

    // Actually build the GeoJSON layer
    const geoLayer = L.geoJSON(json, geoJsonOptions)
        .bindPopup((layer: any) => {
            // Deep copy the properties for use in a simple popup
            const popUpProps = JSON.parse(JSON.stringify(layer.feature.properties));
            popUpProps.points = undefined;
            return JSON.stringify(popUpProps, undefined, 2);
        });

    // Add it to the feature group
    geoFeatureGroup.addLayer(geoLayer);

    if (!geoFeatureGroupExists) {
        // New feature group - add it to the map
        layerControl.addOverlay(geoFeatureGroup, CreateOverlayControlName(layerName, styleRecord));
        geoFeatureGroup.addTo(mymap);
        geoFeatureGroups[layerName] = geoFeatureGroup;
    }

    return Promise.resolve(true);
}

import { Feature, GeoJSON, GeoJsonProperties, Geometry } from "geojson";
import * as L from "leaflet";

import { KnownGeometries } from "../layers/KnownGeometries";
// tslint:disable-next-line: max-line-length
import { CreateOverlayControlName, FallbackLayerStyle, FixLayerStyleDefaults, styleGeometry, stylePoint } from "./leaflet-style";
import { rebuildProps } from "./rebuildProps";

/** The collection of all GeoJSON elements currently added to the map,
 * organised by their featureType
 */
export let geoFeatureGroups: { [name: string]: L.FeatureGroup } = {};

export let featureLookup: { [name: string]: Feature<Geometry, any> } = {};
export let layerLookup: { [name: string]: L.Layer } = {};

/** Gets the featureType from the GeoJSON properties.
 * Allows for a default featureType to be defined.
 * And if all else fails it will give us a value of "not set".
 */
export function getFeatureType(json: GeoJSON, defaultFeatureType: string = "Road"): string {
    let featureType;

    try {
        switch (json.type) {
            case "FeatureCollection":
                featureType = json.features![0]!.properties!.featureType;
                break;
            case "Feature":
                featureType = json!.properties!.featureType;
                break;
        }
    } catch {
        featureType = "";
    }

    return featureType || defaultFeatureType || "not set";
}

/** A 'simple' default popup
 *
 */
function definePopUp(layer: any) {
    // Prepare the properties for use in a simple popup
    const popUpProps = rebuildProps(layer.feature.properties as GeoJsonProperties);

    // For the MVP - reduce to a minimum set
    const popUpPropsMVP: { [name: string]: any } = {Code: popUpProps.link.Code || popUpProps.identifiers.Code};
    if (popUpProps.identifiers.Name || popUpProps.link.Name) {
        popUpPropsMVP.Name = popUpProps.identifiers.Name || popUpProps.link.Name;
    }

    function propToHTML(props: any): string {
        return Object.keys(props).map((propKey) => {
            if (Object.prototype.toString.call(props[propKey]) === "[object Object]") {
                const propLabel = `<span class="popup heading">${propKey}:</span>`;
                const propGroup = propToHTML(props[propKey]);
                return (`<br/>${propLabel}<br/>${propGroup}<br/>`);
            } else {
                const propLabel = `<span class="popup label">${propKey}:</span>`;
                const propValue = `<span class="popup value">${props[propKey]}</span>`;
                return (`<span class="popup">${propLabel}${propValue}</span> `);
            }
        }).join("");
    }

    // Put everything into the popup
    return propToHTML(popUpPropsMVP);
}

function registerFeature(feature: Feature<Geometry, any>, layer: L.Layer) {
    featureLookup[feature.properties.pk] = feature;
    layerLookup[feature.properties.pk] = layer;
}

export function displayGeoJSON(layerControl: L.Control.Layers, json: GeoJSON): Promise<any> {
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
    // Note: If we do not want popups in the MVP then the correct place to remove them is here
    const geoLayer = L.geoJSON(json, geoJsonOptions).bindPopup(definePopUp);

    // Add it to the feature group
    geoFeatureGroup.addLayer(geoLayer);

    if (!geoFeatureGroupExists) {
        // New feature group - add it to the map
        layerControl.addOverlay(geoFeatureGroup, CreateOverlayControlName(featureType, styleRecord));
        geoFeatureGroup.addTo((window as any).map.lMap);
        geoFeatureGroups[featureType] = geoFeatureGroup;
    }

    return Promise.resolve(true);
}

export function fitBounds(boundingBox: L.LatLngBounds) {
    (window as any).map.lMap.fitBounds(boundingBox);
}

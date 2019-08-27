import { GeoJSON } from "geojson";
import * as L from "leaflet";

import { KnownGeometries } from "../layers/KnownGeometries";
// tslint:disable-next-line: max-line-length
import { CreateOverlayControlName, FallbackLayerStyle, FixLayerStyleDefaults, styleGeometry, stylePoint } from "./leaflet-style";

/** The collection of all GeoJSON elements currently added to the map,
 * organised by their featureType
 */
export let geoFeatureGroups: { [name: string]: L.FeatureGroup } = {};

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

/** A simple default popup
 *
 * Feel free to remove / change later.
 */
function definePopUp(layer: any) {
    // Deep copy the properties for use in a simple popup
    const popUpProps = JSON.parse(JSON.stringify(layer.feature.properties));

    // Get rid of anything we know we don't want to show:
    delete popUpProps.points;
    delete popUpProps.pk;
    delete popUpProps.id;
    delete popUpProps.geojsonId;

    // Put everything else into the popup
    return Object.keys(popUpProps).map((propKey) => {
        const propName = propKey.replace("road", "");
        const propLabel = `<span class="popup label">${propName}:</span>`;
        const propValue = `<span class="popup value">${popUpProps[propKey]}</span>`;
        return (`${propLabel}${propValue} `);
    }).join("");
}

export function displayGeoJSON(mymap: L.Map, layerControl: L.Control.Layers, json: GeoJSON): Promise<any> {
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
    // Note: If we do not want popups in the MVP then the correct place to remove them is here
    const geoLayer = L.geoJSON(json, geoJsonOptions).bindPopup(definePopUp);

    // Add it to the feature group
    geoFeatureGroup.addLayer(geoLayer);

    if (!geoFeatureGroupExists) {
        // New feature group - add it to the map
        layerControl.addOverlay(geoFeatureGroup, CreateOverlayControlName(featureType, styleRecord));
        geoFeatureGroup.addTo(mymap);
        geoFeatureGroups[featureType] = geoFeatureGroup;
    }

    return Promise.resolve(true);
}

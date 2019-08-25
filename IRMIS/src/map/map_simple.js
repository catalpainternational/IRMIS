import * as L from "leaflet";

let featureLookup = {};
let layerLookup = {};

export function addToMap(geoJson, map) {

    return L.geoJSON(geoJson, {
        onEachFeature: registerFeature,
        style: getStyleFromFeature,
    }).addTo(map);
}

export function filterFeatures(testFunc, map) {
    Object.values(featureLookup).forEach(feature => {
        const layer = layerLookup[feature.properties.pk];

        let style = getStyleFromFeature(feature);
        if ( !testFunc(feature.properties) ) {
            style.opacity = 0.2;
        } else {
            style.opacity = 1.0;
        }
        layer.setStyle(style);
    });
}

function registerFeature(feature, layer) {
    featureLookup[feature.properties.pk] = feature;
    layerLookup[feature.properties.pk] = layer;
}

function getStyleFromFeature(feature) {
    // returns a style object from a feature being added to leaflet

    switch (feature.properties.roadType) {
        case "NAT":
            return {color: "#000000"};
        case "MUN":
            return {color: "#0000FF"};
        case "RUR":
            return {color: "#FF0000"};
        default:
            return {color: "Pink"};
    }
}

import * as L from "leaflet";

export function addToMap(geoJson, map) {
    L.geoJSON(geoJson, {style: getStyleFromFeature}).addTo(map);
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

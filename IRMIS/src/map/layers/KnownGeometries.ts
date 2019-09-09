import { GeoDataStyle } from "models/geo-data-style";

// tslint:disable: object-literal-sort-keys

export class KnownGeometries {
    /** A list of featureType names that we do NOT want presented in the map.
     *
     * Originally used to block some of the original shapefile derived data.
     * Still useful and integrated into displayGeoJSON
     */
    public static Excluded = [
        "SeaBathymetry", "SeaIndonesia", "seamask",
        "waterbodies", "watersheds", "Hydro_TL_UTM51S",
        "Regions", "District", "Subdistrict", "Suco", "Aldeia", "AileuSD"];

    /** A list of featureType names that we do want presented and styled in a specific way.
     *
     * Supports all SVG styling options
     */
    public static Known: {[name: string]: GeoDataStyle} = {
        // Shows a sample of how to set up marker styles, identified in leaflet as 'pointToLayer'
        // This styling would support areas, lines and points that have a featureType of 'Bridge'
        // "Bridge": {
        //     style: {color: "MAROON"},
        //     pointToLayer: {radius: 3, fillColor: "MAROON", color: "#111", weight: 2, opacity: 0.65, fillOpacity: 0.35},
        // },

        // New - as per the protobuf import
        // see assets_api.js populateGeoJsonProperties()
        "Road": { style: { color: "#F6CF65", opacity: 1 }},
        "Road.on": { style: { color: "#F6CF65", opacity: 1 }},
        "Road.off": { style: { color: "#F6CF65", opacity: 0.2 }},
    };
}

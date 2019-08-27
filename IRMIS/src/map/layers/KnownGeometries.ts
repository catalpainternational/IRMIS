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
    public static Known: any = {
        // Some of the data that came from the original shapefiles
        "SeaBoundary": { style: { style: {color: "SEAGREEN"}}},

        "Hydro_TL_Geographic": { style: { style: {color: "CORNFLOWERBLUE"}}},
        "rivers": { style: { style: {color: "CORNFLOWERBLUE"}}},
        "braiding riverbeds": { style: { style: {color: "CORNFLOWERBLUE"}}},

        // Shows a sample of how to set up marker styles, identified in leaflet as 'pointToLayer'
        // This styling would support areas, lines and points that have a featureType of 'Bridge'
        "Bridge": { style: {
            style: {color: "MAROON"},
            pointToLayer: {radius: 3, fillColor: "MAROON", color: "#111", weight: 2, opacity: 0.65, fillOpacity: 0.35}},
        },

        // New - as per the protobuf import
        // see assets_api.js populateGeoJsonProperties()
        "Road": { style: { style: {color: "#1e38ae"}}},
    };
}

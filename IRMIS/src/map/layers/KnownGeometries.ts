import { GeoDataStyle } from "../models/geo-data-style";

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
    public static Known: { [name: string]: GeoDataStyle } = {
        "bridge": { style: { color: "#447DA9", opacity: 1 } },
        "bridge.on": { style: { color: "#447DA9", opacity: 1 } },
        "bridge.off": { style: { color: "#447DA9", opacity: 0.2 } },
        "culvert": { style: { color: "#674194", opacity: 1 } },
        "culvert.on": { style: { color: "#674194", opacity: 1 } },
        "culvert.off": { style: { color: "#674194", opacity: 0.2 } },
        "drift": { style: { color: "#8A057F", opacity: 1 } },
        "drift.on": { style: { color: "#8A057F", opacity: 1 } },
        "drift.off": { style: { color: "#8A057F", opacity: 0.2 } },

        "highway": { style: { color: "#03A568", opacity: 1 } },
        "highway.on": { style: { color: "#03A568", opacity: 1 } },
        "highway.off": { style: { color: "#03A568", opacity: 0.2 } },
        "national": { style: { color: "#EC0007", opacity: 1 } },
        "national.on": { style: { color: "#EC0007", opacity: 1 } },
        "national.off": { style: { color: "#EC0007", opacity: 0.2 } },
        "municipal": { style: { color: "#985321", opacity: 1 } },
        "municipal.on": { style: { color: "#985321", opacity: 1 } },
        "municipal.off": { style: { color: "#985321", opacity: 0.2 } },
        "urban": { style: { color: "#FFDC00", opacity: 1 } },
        "urban.on": { style: { color: "#FFDC00", opacity: 1 } },
        "urban.off": { style: { color: "#FFDC00", opacity: 0.2 } },
        "rural": { style: { color: "#FF9400", opacity: 1 } },
        "rural.on": { style: { color: "#FF9400", opacity: 1 } },
        "rural.off": { style: { color: "#FF9400", opacity: 0.2 } },
        "Road": { style: { color: "#F6CF65", opacity: 1 } },
        "Road.on": { style: { color: "#F6CF65", opacity: 1 } },
        "Road.off": { style: { color: "#F6CF65", opacity: 0.2 } },
    };
}

// tslint:disable: object-literal-sort-keys

export class KnownGeometries {
    // waterbodies may be mostly aquifiers
    // watersheds are water catchment areas
    public static Excluded = [
        "SeaBathymetry", "SeaIndonesia", "seamask",
        "waterbodies", "watersheds", "Hydro_TL_UTM51S",
        "Regions", "District", "Subdistrict", "Suco", "Aldeia", "AileuSD"];

    public static Known: any = {
        "SeaBoundary": { style: { style: {color: "SEAGREEN"}}},

        "Hydro_TL_Geographic": { style: { style: {color: "CORNFLOWERBLUE"}}},
        "rivers": { style: { style: {color: "CORNFLOWERBLUE"}}},
        "braiding riverbeds": { style: { style: {color: "CORNFLOWERBLUE"}}},

        "Bridge": { style: {
            style: {color: "MAROON"},
            pointToLayer: {radius: 3, fillColor: "MAROON", color: "#111", weight: 2, opacity: 0.65, fillOpacity: 0.35}},
        },

        // The next two are for Ermera
        "Maintenance": { style: { style: {color: "LIGHTGRAY"}}},
        "Rehabilitation": { style: { style: {color: "LIGHTGRAY"}}},

        "Rural_Road_R4D_Timor_Leste": { style: { style: {color: "LIGHTGRAY"}}},
        "RRMPIS_2014": { style: { style: {color: "DARKGRAY"}}},
        "Municipal_Road": { style: { style: {color: "LIGHTSLATEGRAY"}}},
        "National_Road": { style: { style: {color: "DARKSLATEGRAY"}}},

        // Rehab projects
        "ADB Project": { style: { style: {color: "GOLDENROD"}}},
        "European Union": { style: { style: {color: "GOLDENROD"}}},
        "JICA Project": { style: { style: {color: "GOLDENROD"}}},
        "On the Tender Stage": { style: { style: {color: "GOLDENROD"}}},
        "WB Project": { style: { style: {color: "GOLDENROD"}}},
        "Rehabilitation by Timor leste Gov": { style: { style: {color: "GOLDENROD"}}},

        "Highway_Suai": { style: { style: {color: "YELLOW"}}},
    };
}

import { GeoJSON } from "geojson";

/** The collection of all GeoJSON elements currently added to the map,
 * organised by their featureType
 */

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

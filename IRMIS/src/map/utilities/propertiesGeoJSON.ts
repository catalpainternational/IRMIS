import { GeoJSON } from "geojson";

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

/** populateGeoJsonProperties
 *
 * for each feature in a geojson FeatureCollection,
 * use the property `id` to access the relevant metadata from the propertiesLookup
 * and add it to the feature properties.
 *
 * also ensure that each feature.properties has a validly set `featureType`
 *
 * @param geoJson - the GeoJSON that needs its feature.properties populated
 * @param propertiesLookup - the source of the properties data referenced by properties.id
 */
export function populateGeoJsonProperties(geoJson: GeoJSON, propertiesLookup: { [name: string]: any }) {
    if (geoJson.type !== "FeatureCollection") {
        return;
    }

    geoJson.features.forEach((feature) => {
        if (!feature.properties) {
            return;
        }

        const propertySet = propertiesLookup[feature.properties.id];
        if (!propertySet) {
            return;
        }

        Object.assign(feature.properties, propertySet.toObject());

        // Special handling for the mandatory property `featureType`
        if (!feature.properties.featureType) {
            if (feature.properties.roadType) {
                feature.properties.featureType = "Road";
            }
        }
    });
}

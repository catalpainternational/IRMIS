import { getGeoJson } from "./assets/assets_api.js";
import { prepareRoadEdit } from "./table.js";

/** populateGeoJsonProperties
 *
 * for each feature in a geojson FeatureCollection,
 * use the property `pk` to access the relevant metadata from the propertiesLookup
 * and add it to the feature properties.
 *
 * also ensure that each feature.properties has a validly set `featureType`
 *
 * @param geoJson - the GeoJSON that needs its feature.properties populated
 * @param propertiesLookup - the source of the properties data referenced by properties.pk
 */
function populateGeoJsonProperties(geoJson, propertiesLookup) {
    geoJson.features.forEach(feature => {
        const propertySet = propertiesLookup[feature.properties.pk];
        if (!propertySet) {
            throw new Error(`assets_api.populateGeoJsonProperties could not find property '${feature.properties.pk}'.`);
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

/** Process all of the metadata and geodata promises
 *
 * @param roadsMetadataPromises - an array of promises to retrieve roads metadata, plus one to retrieve geoData
 * @param estradaTable - reference to the UI datatable object
 * @param estradaMap - reference to the UI leaflet map object
 * 
 * @returns a simple Promise.resolve when loading has completed
 */
export function processAllDataPromises(roadsMetadataPromises, estradaTable, estradaMap) {
    let roadsLookup = [];

    return Promise.all(roadsMetadataPromises)
        .then(values => {
            // The final promise result is for all of the geobuf files
            let geoJsonDetails = values.pop();
            // All of the others are road metadata chunks
            roadsLookup = roadsLookup.concat(values);

            // Add in the additional roads to the table
            values.forEach(roadValues => {
                const roadObjects = Object.values(roadValues).map(r => r.toObject());
                prepareRoadEdit(roadObjects);
                estradaTable.rows.add(roadObjects).draw();
            });

            // retrieve each GeoJSON file
            return Promise.all(geoJsonDetails.map(geoJsonDetail => {
                return getGeoJson(geoJsonDetail)
                    .then(geoJson => {
                        // add in road metadata to the GeoJSON
                        roadsLookup.forEach(roadsMetadata => {
                            populateGeoJsonProperties(geoJson, roadsMetadata);
                        });

                        // add to map
                        estradaMap.addMapData(geoJson);
                        return Promise.resolve(true);
                    });
            }));
        }, err => console.log(err));
}


import { GeoJsonProperties } from "geojson";

/** Takes a set of GeoJsonProperties and produces an object that
 * is better suited for presentation in popUps etc.
 * The original set of GeoJsonProperties are not altered.
 *
 * This has turned into a bit of an 'everything including the kitchen sink'.
 *
 * But it does do exactly what we want in lieu of properly defining a preformatted block
 * of data in the GeoJSON properties.
 */
export function rebuildProps(properties: GeoJsonProperties) {
    // Deep copy the properties for use in a simple popup
    const popUpProps = JSON.parse(JSON.stringify(properties));

    /** A little class to let us shift stuff around */
    class PropShift {
        private propKey: string;

        constructor(propKey: string) {
            this.propKey = propKey;
        }

        public moveProp = (prefix: string, grouping: string) => {
            if (this.propKey.indexOf(prefix) === 0) {
                popUpProps[grouping] = popUpProps[grouping] || {};
                const propName = this.propKey.replace(prefix, "");
                popUpProps[grouping][propName] = popUpProps[this.propKey];
                delete popUpProps[this.propKey];

                this.propKey = "";
            }

            return this;
        }
    }

    // Get rid of anything we know we don't want to show:
    delete popUpProps.points;
    delete popUpProps.pk;
    delete popUpProps.id;
    delete popUpProps.geojsonId;
    Object.keys(popUpProps).forEach((propKey) => {
        if (!popUpProps[propKey]) {
            delete popUpProps[propKey];
        }
    });

    // Restructure a little
    Object.keys(popUpProps).forEach((propKey) => {
        const props = new PropShift(propKey);
        props
            .moveProp("road", "identifiers")
            .moveProp("link", "link")
            .moveProp("surface", "surface")
            .moveProp("pavement", "surface");
    });

    return popUpProps;
}

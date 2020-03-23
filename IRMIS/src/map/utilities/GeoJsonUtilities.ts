/**
 * Wraps a GeoJSON {@link Geometry} in a GeoJSON {@link Feature}.
 *
 * @name feature
 * @param {Geometry} geometry input geometry
 * @param {Object} [properties={}] an Object of key-value pairs to add as properties
 * @param {Object} [options={}] Optional Parameters
 * @param {Array<number>} [options.bbox] Bounding Box Array [west, south, east, north] associated with the Feature
 * @param {string|number} [options.id] Identifier associated with the Feature
 * @returns {Feature} a GeoJSON Feature
 * @example
 * var geometry = {
 *   "type": "Point",
 *   "coordinates": [110, 50]
 * };
 *
 * var feature = turf.feature(geometry);
 *
 * //=feature
 */
function feature(geom: {[name: string]: any}, options: {[name: string]: any}) {
    const feat: {[name: string]: any} = { type: "Feature" };
    if (options.bbox) {
        feat.bbox = options.bbox;
    }
    feat.properties = {};
    feat.geometry = geom;
    return feat;
}

/**
 * Creates a {@link Polygon} {@link Feature} from an Array of LinearRings.
 *
 * @name polygon
 * @param {Array<Array<Array<number>>>} coordinates an array of LinearRings
 * @param {Array<number>} [options.bbox] Bounding Box Array [west, south, east, north] associated with the Feature
 * @param {string|number} [options.id] Identifier associated with the Feature
 * @returns {Feature<Polygon>} Polygon Feature
 * @example
 * var polygon = turf.polygon([[[-5, 52], [-4, 56], [-2, 51], [-7, 54], [-5, 52]]], { name: 'poly1' });
 *
 * //=polygon
 */
function polygon(coordinates: number[][][], options: {[name: string]: any}) {
    for (let _i = 0, coordinatesA = coordinates; _i < coordinatesA.length; _i++) {
        const ring = coordinatesA[_i];
        if (ring.length < 4) {
            throw new Error("Each LinearRing of a Polygon must have 4 or more Positions.");
        }
        for (let j = 0; j < ring[ring.length - 1].length; j++) {
            // Check if first point of Polygon contains two numbers
            if (ring[ring.length - 1][j] !== ring[0][j]) {
                throw new Error("First and last Position are not equivalent.");
            }
        }
    }
    const geom = {
        type: "Polygon",
        coordinates,
    };
    return feature(geom, options);
}

/**
 * Takes a bbox and returns an equivalent polygon.
 *
 * @name bboxPolygon
 * @param {BBox} bbox extent in [minX, minY, maxX, maxY] order
 * @returns {Feature<Polygon>} a Polygon representation of the bounding box
 * @example
 * var bbox = [0, 0, 10, 10];
 */
function bboxPolygon(bbox: number[]) {
    // Convert BBox positions to Numbers
    const west = Number(bbox[0]);
    const south = Number(bbox[1]);
    const east = Number(bbox[2]);
    const north = Number(bbox[3]);

    const lowLeft = [west, south];
    const topLeft = [west, north];
    const topRight = [east, north];
    const lowRight = [east, south];

    return polygon([[
        lowLeft,
        lowRight,
        topRight,
        topLeft,
        lowLeft
    ]], {bbox});
}

/**
 * Takes a set of coordinates, calculates the bbox of all of them, and returns a bounding box.
 *
 * @name bbox
 * @param {number[][]} coords any array of coordinate pairs
 * @returns {BBox} bbox extent in [minX, minY, maxX, maxY] order
 */
function bbox(coords: number[][]) {
    const result = [Infinity, Infinity, -Infinity, -Infinity];
    coords.forEach((coord) => {
        if (result[0] > coord[0]) {
            result[0] = coord[0];
        }
        if (result[1] > coord[1]) {
            result[1] = coord[1];
        }
        if (result[2] < coord[0]) {
            result[2] = coord[0];
        }
        if (result[3] < coord[1]) {
            result[3] = coord[1];
        }
    });

    return result;
}

/** Get the first set of coordinates out of whatever type of GeoJSON we have.
 * We can then use this for quick and dirty coordinate space checking
 */
export function getFlatCoords(geoJSON: GeoJSON): number[] {
    switch (geoJSON.type) {
        case "Feature":
            return getFlatCoords((geoJSON as Feature).geometry);
        case "FeatureCollection":
            return getFlatCoords((geoJSON as FeatureCollection).features[0].geometry);
        case "GeometryCollection":
            return getFlatCoords((geoJSON as GeometryCollection).geometries[0]);
        case "Point":
            return (geoJSON as Point).coordinates;
        case "MultiPoint":
            return (geoJSON as MultiPoint).coordinates[0];
        case "LineString":
            return (geoJSON as LineString).coordinates[0];
        case "MultiLineString":
            return (geoJSON as MultiLineString).coordinates[0][0];
        case "Polygon":
            return (geoJSON as Polygon).coordinates[0][0];
        case "MultiPolygon":
            return (geoJSON as MultiPolygon).coordinates[0][0][0];
    }

    return [-1, -1];
}
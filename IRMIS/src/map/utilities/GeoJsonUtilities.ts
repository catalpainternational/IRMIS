import {
    Feature, FeatureCollection,
    GeoJSON, GeometryCollection,
    LineString, MultiLineString, MultiPoint, MultiPolygon, Point, Polygon
} from "geojson";

/**
 * Takes a set of coordinates, calculates the bbox of all of them, and returns a bounding box.
 *
 * @name bbox
 * @param {number[][]} coords any array of coordinate pairs
 * @returns {BBox} bbox extent in [minX, minY, maxX, maxY] order
 */
export function buildBBox(coords: number[][]) {
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

/** Get the set of coordinates out of whatever type of GeoJSON we have
 * as a simple flat list.
 * We can then use this for quick and dirty coordinate space checking
 */
export function getFlatCoords(geoJSON: GeoJSON): number[][] {
    switch (geoJSON.type) {
        case "Feature":
            return getFlatCoords((geoJSON as Feature).geometry);
        case "FeatureCollection":
            return getFlatCoords((geoJSON as FeatureCollection).features[0].geometry);
        case "GeometryCollection":
            return getFlatCoords((geoJSON as GeometryCollection).geometries[0]);
        case "Point":
            return [(geoJSON as Point).coordinates];
        case "MultiPoint":
            return (geoJSON as MultiPoint).coordinates;
        case "LineString":
            return (geoJSON as LineString).coordinates;
        case "MultiLineString":
            const mlsCoords = (geoJSON as MultiLineString).coordinates;
            return mlsCoords.reduce((acc, val) => acc.concat(val), []);
        case "Polygon":
            const pCoords = (geoJSON as Polygon).coordinates;
            return pCoords.reduce((acc, val) => acc.concat(val), []);
        case "MultiPolygon":
            const mpCoords = (geoJSON as MultiPolygon).coordinates;
            return mpCoords.reduce((acc, val) => acc.concat(val), []).reduce((acc, val) => acc.concat(val), []);
    }
}

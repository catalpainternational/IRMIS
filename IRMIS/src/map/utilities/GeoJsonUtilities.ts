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
 * @param {number[]} [bbox=[Infinity, Infinity, -Infinity, -Infinity]] an optional existing bounding box to work with
 * @returns {BBox} bbox extent in [minX, minY, maxX, maxY] [WSEN] order
 */
export function buildBBox(coords: number[][], bbox: number[] = [Infinity, Infinity, -Infinity, -Infinity]) {
    coords.forEach((coord) => {
        if (bbox[0] > coord[0]) {
            bbox[0] = coord[0];
        }
        if (bbox[1] > coord[1]) {
            bbox[1] = coord[1];
        }
        if (bbox[2] < coord[0]) {
            bbox[2] = coord[0];
        }
        if (bbox[3] < coord[1]) {
            bbox[3] = coord[1];
        }
    });

    return bbox;
}

/** Get the boundingbox out of whatever type of GeoJSON we have
 */
export function getBbox(geoJSON: GeoJSON, bbox: number[] = [Infinity, Infinity, -Infinity, -Infinity]): number[] {
    switch (geoJSON.type) {
        case "Feature":
            return getBbox((geoJSON as Feature).geometry, bbox);
        case "FeatureCollection":
            (geoJSON as FeatureCollection).features.forEach((feature) => {
                bbox = getBbox(feature.geometry, bbox);
            });
            return bbox;
        case "GeometryCollection":
            (geoJSON as GeometryCollection).geometries.forEach((geometry) => {
                bbox = getBbox(geometry, bbox);
            });
            return bbox;
        case "Point":
            return buildBBox([(geoJSON as Point).coordinates], bbox);
        case "MultiPoint":
            return buildBBox((geoJSON as MultiPoint).coordinates, bbox);
        case "LineString":
            return buildBBox((geoJSON as LineString).coordinates, bbox);
        case "MultiLineString":
            const mlsCoords = (geoJSON as MultiLineString).coordinates;
            return buildBBox(mlsCoords.reduce((acc, val) => acc.concat(val), []), bbox);
        case "Polygon":
            const pCoords = (geoJSON as Polygon).coordinates;
            return buildBBox(pCoords.reduce((acc, val) => acc.concat(val), []), bbox);
        case "MultiPolygon":
            const mpCoords = (geoJSON as MultiPolygon).coordinates;
            return buildBBox(mpCoords.reduce((acc, val) =>
                acc.concat(val), []).reduce((acc, val) => acc.concat(val), []), bbox);
    }
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
            let fcCoords: number[][] = [];
            (geoJSON as FeatureCollection).features.forEach((feature) => {
                fcCoords = fcCoords.concat(getFlatCoords(feature.geometry));
            });
            return fcCoords;
        case "GeometryCollection":
            let gcCoords: number[][] = [];
            (geoJSON as GeometryCollection).geometries.forEach((geometry) => {
                gcCoords = gcCoords.concat(getFlatCoords(geometry));
            });
            return gcCoords;
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

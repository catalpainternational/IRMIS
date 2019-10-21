import proj4 from "proj4";

// INPUT FORMAT: EPSG:32751 WGS 84 / UTM zone 51S - OUTPUT FORMAT: EPSG:4326 WGS 84
proj4.defs("EPSG:32751", "+proj=utm +zone=51 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs");
export const projToWGS84 = proj4("EPSG:32751", "WGS84");

/**
 * JS implementation of Python math -> modf() function
 *
 * Split a number into interger and remainder values.
 * Returned items have same sign as original number.
 *
 * @param value - numeric value to be split
 */
function modf(value) {
    return [value % 1, Math.trunc(value)];
}

function splitOutDms(coord) {
    const splitDeg = modf(coord);
    const degrees = Math.trunc(splitDeg[1]);
    const interm = modf(splitDeg[0] * 60);
    const minutes = Math.abs(Math.trunc(interm[1]));
    const seconds = Math.abs(Math.round((interm[0] * 60 + 0.00001) * 100) / 100);

    return [degrees, minutes, seconds];
}

export function toDms(latLon) {
    if (!latLon) {
        return "";
    }

    const xDms = splitOutDms(latLon[0]);
    const yDms = splitOutDms(latLon[1]);

    // calculate N/S (lat) & E/W (long)
    const NorS = (xDms[0] < 0) ? "S" : "N";
    const EorW = (yDms[0] < 0) ? "W" : "E";

    // return formatted DMS string
    return Math.abs(yDms[0]) + '\u00b0' + yDms[1] +"'" + yDms[2] + '"' + NorS + ' ' + Math.abs(xDms[0]) + '\u00b0' + xDms[1] +"'" + xDms[2] +'"' + EorW;
}

export function toUtm(latLon) {
    return latLon
        ? latLon[0].toFixed(5) + ', ' + latLon[1].toFixed(5)
        : "";
}

import * as L from "leaflet";
// tslint:disable: max-line-length

export class Config {
    /** Timor Leste Bounding Box strict - coordinates are arranged WSEN */
    public static tlBBoxStrict = [124.0416, -9.5042, 127.3428, -8.1268];

    /** Timor Leste Bounding Box rounded 'out' - coordinates are arranged WSEN */
    public static tlBBox = [123.7, -9.6, 127.7, -8];

    /** Timor Leste Geographic Center */
    public static tlCenter: L.LatLngExpression = [(Config.tlBBox[1] + Config.tlBBox[3]) / 2, (Config.tlBBox[0] + Config.tlBBox[2]) / 2];

    /** Timor Leste Geographic Bounds */
    public static tlBounds = L.latLngBounds([[Config.tlBBox[1], Config.tlBBox[0]], [Config.tlBBox[3], Config.tlBBox[2]]]);

    /** The preferred base layer name - as defined in BaseLayers.ts */
    public static preferredBaseLayerName: string = "Street OSM HOT";
}

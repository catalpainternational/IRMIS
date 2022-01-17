import { PathOptions } from "leaflet";

export interface IToLayerStyle {
  color: string;
  weight?: number;
}

export interface IPointToLayerBaseStyle extends IToLayerStyle {
  fillColor: string;
  opacity: number;
  fillOpacity: number;
  radius: number;
}

export interface IPointToLayerHtmlStyle {
  html: string;
}

export type PointToLayerStyle = IPointToLayerHtmlStyle | IPointToLayerBaseStyle;

export class GeoDataStyle {
  /** The actual geo_type this style is associated with */
  public featureType?: string;
  /** A string that identifies an arbitrary grouping that this layer belongs to */
  public mapPane?: string;
  public style: PathOptions = { color: "BLACK"};
  public pointToLayer?: PointToLayerStyle;
}

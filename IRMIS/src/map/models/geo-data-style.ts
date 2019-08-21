export interface IToLayerStyle {
  color: string;
  weight?: number;
}

export interface ILineToLayerStyle extends IToLayerStyle {
  fillColor?: string;
  opacity?: number;
  fillOpacity?: number;
  dashArray?: string;
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
  public geoType?: string;
  /** A string that identifies an arbitrary grouping that this layer belongs to */
  public mapPane?: string;
  public displaySequence?: number;
  /** Identifies which property in the GeoJSON is to be used to select a substyle definition */
  public styleProp?: string;
  public style?: {
    style: ILineToLayerStyle;
    pointToLayer?: PointToLayerStyle;
    /** Any additional style definitions referenced via style_prop - LineToLayerStyle is expected */
    [propName: string]: any;
  };
}

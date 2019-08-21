import * as L from "leaflet";
import { CircleMarkerOptions } from "leaflet";

import { GeoDataStyle, IPointToLayerHtmlStyle, PointToLayerStyle } from "../models/geo-data-style";

import { hashGeoTypeName } from "../utilities/text";

/** Generate a fall-back colour based on the geoType name */
export function FallbackLayerStyle(geoType: string): GeoDataStyle {
  // Generate a fall-back colour based on a hash of the geoType name
  // tslint:disable-next-line
  const geoTypeHash = hashGeoTypeName(geoType) >> 8;
  const fbColour = "#" + ("000000" + geoTypeHash.toString(16)).slice(-6);

  return { style: { style: { color: fbColour } } } as GeoDataStyle;
}

/** Ensure that default styles are set for points and lines */
export function FixLayerStyleDefaults(styleRecord: GeoDataStyle) {
  if (!styleRecord.style) {
    styleRecord.style = { style: { color: "BLACK"} };
  }
  if (!styleRecord.style.style.weight) {
    styleRecord.style.style.weight = 2;
  }

  if (!styleRecord.style.pointToLayer) {
    styleRecord.style.pointToLayer = {
      color: "#111",
      fillColor: styleRecord.style.style.color,
      fillOpacity: 0.35,
      opacity: 0.65,
      radius: 3,
      weight: 2,
    };
  }
}

/** Creates a name to use in the overlay control from the supplied name and stylerecord */
export function CreateOverlayControlName(layerName: string, styleRecord: GeoDataStyle): string {
  if (!styleRecord.style) {
    styleRecord.style = { style: { color: "BLACK"} };
  }

  const lineStyle = styleRecord.style.style;
  let lineStyleSvg = '<svg width="12" height="12"><g>';
  lineStyleSvg += `<path viewBox="0 0 12 12" fill-rule="evenodd" d="M0 0 L12 12" stroke="${lineStyle.color}"`;
  if (!!lineStyle.opacity) {
    lineStyleSvg += ` stroke-opacity=${lineStyle.opacity}`;
  }
  if (!!lineStyle.weight) {
    lineStyleSvg += ` stroke-width=${lineStyle.weight}`;
  }
  if (!!lineStyle.fillColor) {
    lineStyleSvg += ` fill=${lineStyle.fillColor}`;
  }
  if (!!lineStyle.fillOpacity) {
    lineStyleSvg += ` fill-opacity=${lineStyle.fillOpacity}`;
  }
  if (!!lineStyle.dashArray) {
    lineStyleSvg += ` stroke-dasharray=${lineStyle.dashArray}`;
  }
  lineStyleSvg += "</path></g></svg>";

  return `${layerName} ${lineStyleSvg}`;
}

export function styleGeometry(
  feature?: GeoJSON.Feature<GeoJSON.GeometryObject, any>,
  styleRecord?: GeoDataStyle): L.PathOptions {
  if (!styleRecord || !feature) {
    return {};
  }

  if (!styleRecord.style) {
    styleRecord.style = { style: { color: "BLACK"} };
  }

  if (!!styleRecord.styleProp) {
    const styleProp = styleRecord.styleProp;
    const featureStyleProp = "style" + feature.properties[styleProp];

    return (styleRecord.style[featureStyleProp]) ? styleRecord.style[featureStyleProp] : styleRecord.style.style;
  }

  return styleRecord.style.style;
}

export function stylePoint(
  feature: GeoJSON.Feature<GeoJSON.Point>,
  latlng: L.LatLng, pointStyle: PointToLayerStyle,
): L.Marker | L.CircleMarker {
  const templateMatches = /{{([a-zA-Z_0-9]*)}}/g;
  // Note that this escaped regex template does NOT handle nested arrays, and deliberately does not match objects
  // tslint:disable-next-line: max-line-length
  const jsonFieldMatch = '\\s*:\\s*(?:"((?:.|\\n)*?)"|(-?[0-9]+(?:\\.[0-9]+)?)|(true|false)|(\\[(?:.|\\n)*?\\]))\\s*(?:,|\\}|\\])';

  if ((pointStyle as IPointToLayerHtmlStyle).html) {
    const markerIcon = {} as L.MarkerOptions;

    const htmlStyle = (pointStyle as IPointToLayerHtmlStyle).html;
    let mappedHtmlStyle: any = htmlStyle;
    const featureJson = JSON.stringify(feature);

    // Do the token substitution
    let tokenMatches: RegExpExecArray | null;
    // tslint:disable-next-line: no-conditional-assignment
    while ((tokenMatches = templateMatches.exec(htmlStyle)) !== null) {
      const firstToken = tokenMatches[1];
      const featureMatch = `"${firstToken}"${jsonFieldMatch}`;
      const fre = new RegExp(featureMatch);
      const firstMatch = fre.exec(featureJson);

      if (firstMatch != null) {
        const matchId = firstMatch.slice(1).findIndex((m) => !!m) + 1;
        let substitute = firstMatch[matchId] as any;
        if (typeof (substitute) === "number") {
          substitute = substitute.toPrecision(1);
        }
        if (typeof (substitute) === "string") {
          const subNumber = Number(substitute);
          if (!isNaN(subNumber)) {
            substitute = subNumber.toFixed(1).replace(/\.?0+$/, "");
          }
        }
        mappedHtmlStyle = mappedHtmlStyle.replace("{{" + firstToken + "}}", substitute);
      } else {
        // If there's nothing found (to substitute with)
        // then replace the token with a dash
        mappedHtmlStyle = mappedHtmlStyle.replace("{{" + firstToken + "}}", "-");
      }
    }

    const myIcon = L.divIcon({
      // className: feature.properties['geo_type'],
      html: mappedHtmlStyle,
      iconSize: undefined, // Must do this or otherwise css styling is ignored
    });
    markerIcon.icon = myIcon;

    return L.marker(latlng, markerIcon);
  }

  const iconStyle = pointStyle as CircleMarkerOptions;

  return L.circleMarker(latlng, iconStyle);
}

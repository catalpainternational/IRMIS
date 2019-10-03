import * as L from "leaflet";
import { CircleMarkerOptions } from "leaflet";

import { GeoDataStyle, IPointToLayerBaseStyle, IPointToLayerHtmlStyle } from "../models/geo-data-style";

import { getFeatureType } from "./metaGeoJSON";
import { hashFeatureTypeName } from "./text";

/** Generate a fall-back colour based on the featureType name */
export function FallbackLayerStyle(featureType: string): GeoDataStyle {
  // Generate a fall-back colour based on a hash of the featureType name
  // tslint:disable-next-line
  const featureTypeHash = hashFeatureTypeName(featureType) >> 8;
  const fbColour = "#" + ("000000" + featureTypeHash.toString(16)).slice(-6);

  return { style: { color: fbColour } } as GeoDataStyle;
}

/** Ensure that default styles are set for points and lines */
export function FixLayerStyleDefaults(styleRecord: GeoDataStyle) {
  if (!styleRecord.style) {
    styleRecord.style = { color: "BLACK"};
  }
  if (!styleRecord.style.weight) {
    styleRecord.style.weight = 2;
  }

  if (!styleRecord.pointToLayer) {
    styleRecord.pointToLayer = {
      color: "#111",
      fillColor: styleRecord.style.color || "BLACK",
      fillOpacity: 0.35,
      opacity: 0.65,
      radius: 3,
      weight: 2,
    };
  }
}

/** Creates a symbology + name to use in the filter control
 * from the supplied name and stylerecord
 */
export function CreateOverlayControlName(layerName: string, styleRecord: GeoDataStyle): string {
  if (!styleRecord.style) {
    styleRecord.style = { color: "BLACK"};
  }

  function addSvgAttribute(value: any, attributeName: string): string {
    return (!!value) ? ` ${attributeName}=${value}` : "";
  }

  const lineStyle = styleRecord.style;
  let lineStyleSvg = '<svg width="12" height="12"><g>';
  lineStyleSvg += '<path viewBox="0 0 12 12" fill-rule="evenodd" d="M0 0 L12 12"';
  lineStyleSvg += addSvgAttribute(lineStyle.color, "stroke");
  lineStyleSvg += addSvgAttribute(lineStyle.opacity, "stroke-opacity");
  lineStyleSvg += addSvgAttribute(lineStyle.weight, "stroke-width");
  lineStyleSvg += addSvgAttribute(lineStyle.fillColor, "fill");
  lineStyleSvg += addSvgAttribute(lineStyle.fillOpacity, "fill-opacity");
  lineStyleSvg += addSvgAttribute(lineStyle.dashArray, "stroke-dasharray");
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
    styleRecord.style = { color: "BLACK"};
  }

  return styleRecord.style;
}

/** Defines everything needed to style points (markers) properly.
 *
 * Note: Do NOT delete this function EVER.
 * Even if you think we will never support markers.
 * This thing does an absolute bucket load of work properly,
 * and it's very hard to replicate from stackoverflow / leaflet docs
 */
export function stylePoint(
  feature: GeoJSON.Feature<GeoJSON.Point>,
  latlng: L.LatLng, pointStyle: IPointToLayerHtmlStyle | IPointToLayerBaseStyle | undefined,
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
      className: getFeatureType(feature),
      html: mappedHtmlStyle,
      iconSize: undefined, // Must do this or otherwise css styling is ignored
    });
    markerIcon.icon = myIcon;

    return L.marker(latlng, markerIcon);
  }

  const iconStyle = pointStyle as CircleMarkerOptions;

  return L.circleMarker(latlng, iconStyle);
}

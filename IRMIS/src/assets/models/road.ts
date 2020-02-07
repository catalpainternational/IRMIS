import { Road } from "../../../protobuf/roads_pb";

import { projToWGS84, toDms, toUtm } from "../crsUtilities";
import {
    choice_or_default,
    getFieldName,
    getHelpText,
    humanizeChoices,
    makeEstradaObject,
    projectionToCoordinates,
    toChainageFormat,
} from "../protoBufUtilities";

import { ADMINISTRATIVE_AREA_CHOICES, ASSET_CLASS_CHOICES, ASSET_CONDITION_CHOICES, IAsset } from "./asset";

const assetSchema = JSON.parse(document.getElementById("asset_schema")?.textContent || "");

export const MAINTENANCE_NEED_CHOICES = humanizeChoices(assetSchema, "maintenance_need", "code", "name");
export const PAVEMENT_CLASS_CHOICES = humanizeChoices(assetSchema, "pavement_class", "code", "name");
export const ROAD_STATUS_CHOICES = humanizeChoices(assetSchema, "road_status", "code", "name");
export const SURFACE_TYPE_CHOICES = humanizeChoices(assetSchema, "surface_type", "code", "name");
export const TECHNICAL_CLASS_CHOICES = humanizeChoices(assetSchema, "technical_class", "code", "name");
export const TRAFFIC_LEVEL_CHOICES = humanizeChoices(assetSchema, "traffic_level");
export const TERRAIN_CLASS_CHOICES = humanizeChoices(assetSchema, "terrain_class");

export class EstradaRoad extends Road implements IAsset {
    public static getFieldName(field: string) {
        return getFieldName(assetSchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(assetSchema, field);
    }

    private isSerialising: boolean;

    public constructor() {
        super();
        this.isSerialising = false;
    }

    get id() {
        return this.getId().toString();
    }

    /** The asset's type - the prefix part of its Id */
    get assetType() {
        return "ROAD";
    }

    get assetTypeName() {
        return (window as any).gettext("Road");
    }

    /** Return just the asset's Id without the assetType prefix */
    get assetId() {
        return this.id.startsWith(this.assetType)
            ? this.id.split("-")[1]
            : this.id;
    }

    get name() {
        return this.roadName;
    }

    get code() {
        return this.roadCode;
    }

    get roadName() {
        return this.getRoadName();
    }

    get roadCode() {
        return this.getRoadCode();
    }

    get linkName() {
        return `${this.getLinkStartName()} - ${this.getLinkEndName()}`;
    }

    get linkStartName() {
        return this.getLinkStartName();
    }

    get linkStartChainage() {
        return toChainageFormat(this.getNullableLinkStartChainage());
    }

    get linkEndName() {
        return this.getLinkEndName();
    }

    get linkEndChainage() {
        return toChainageFormat(this.getNullableLinkEndChainage());
    }

    get linkCode() {
        return this.getLinkCode();
    }

    get linkLength() {
        const linkLength = this.getNullableLinkLength();
        if (linkLength === null) {
            return linkLength;
        }

        return (linkLength * 1000).toFixed(3);
    }

    get status() {
        return choice_or_default(this.getRoadStatus(), ROAD_STATUS_CHOICES);
    }

    get assetClass() {
        return choice_or_default(this.getAssetClass(), ASSET_CLASS_CHOICES);
    }

    get surfaceType() {
        return choice_or_default(this.getSurfaceType(), SURFACE_TYPE_CHOICES);
    }

    get assetCondition() {
        return choice_or_default(this.getAssetCondition(), ASSET_CONDITION_CHOICES);
    }

    get pavementClass() {
        return choice_or_default(this.getPavementClass(), PAVEMENT_CLASS_CHOICES);
    }

    get administrativeArea() {
        return choice_or_default(this.getAdministrativeArea(), ADMINISTRATIVE_AREA_CHOICES);
    }

    get carriagewayWidth() {
        const carriagewayWidth = this.getNullableCarriagewayWidth();
        if (carriagewayWidth === null) {
            return carriagewayWidth;
        }

        return (carriagewayWidth).toFixed(1);
    }

    get project() {
        return this.getProject();
    }

    get fundingSource() {
        return this.getFundingSource();
    }

    get technicalClass() {
        return choice_or_default(this.getTechnicalClass(), TECHNICAL_CLASS_CHOICES);
    }

    // get terrainClass() {
    //     return choice_or_default(this.getTerrainClass(), TERRAIN_CLASS_CHOICES);
    // }

    get maintenanceNeed() {
        return choice_or_default(this.getMaintenanceNeed(), MAINTENANCE_NEED_CHOICES);
    }

    get trafficLevel() {
        return choice_or_default(this.getTrafficLevel(), TRAFFIC_LEVEL_CHOICES);
    }

    get projectionStart() {
        return this.getProjectionStart();
    }

    get rainfall() {
        return this.getNullableRainfall();
    }

    get projectionEnd() {
        return this.getProjectionEnd();
    }

    get startDMS() {
        const projection = this.getProjectionStart();
        return projection ? toDms(projToWGS84.forward(projectionToCoordinates(projection))) : "";
    }

    get endDMS() {
        const projection = this.getProjectionEnd();
        return projection ? toDms(projToWGS84.forward(projectionToCoordinates(projection))) : "";
    }

    get startUTM() {
        const projection = this.getProjectionStart();
        return projection ? toUtm(projToWGS84.forward(projectionToCoordinates(projection))) : "";
    }

    get endUTM() {
        const projection = this.getProjectionEnd();
        return projection ? toUtm(projToWGS84.forward(projectionToCoordinates(projection))) : "";
    }

    get numberLanes() {
        return this.getNullableNumberLanes();
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableRainfall() {
        const rainfall = super.getRainfall();
        return (rainfall >= 0 || this.isSerialising) ? rainfall : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableLinkStartChainage() {
        const linkStartChainage = super.getLinkStartChainage();
        return (linkStartChainage >= 0 || this.isSerialising) ? linkStartChainage : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableLinkEndChainage() {
        const linkEndChainage = super.getLinkEndChainage();
        return (linkEndChainage >= 0 || this.isSerialising) ? linkEndChainage : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableLinkLength() {
        const linkLength = super.getLinkLength();
        return (linkLength >= 0 || this.isSerialising) ? linkLength : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableCarriagewayWidth() {
        const carriagewayWidth = super.getCarriagewayWidth();
        return (carriagewayWidth >= 0 || this.isSerialising) ? carriagewayWidth : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableNumberLanes() {
        const numberLanes = super.getNumberLanes();
        return (numberLanes >= 0 || this.isSerialising) ? numberLanes : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public setLinkStartChainage(value: number | undefined | null) {
        super.setLinkStartChainage(this.nullToNegative(value));
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public setLinkEndChainage(value: number | undefined | null) {
        super.setLinkEndChainage(this.nullToNegative(value));
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public setLinkLength(value: number | undefined | null) {
        super.setLinkLength(this.nullToNegative(value));
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public setCarriagewayWidth(value: number | undefined | null) {
        super.setCarriagewayWidth(this.nullToNegative(value));
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public setNumberLanes(value: number | undefined | null) {
        super.setNumberLanes(this.nullToNegative(value));
    }

    public serializeBinary() {
        // prepare the nullable numerics for serialisation
        this.isSerialising = true;
        const wireFormat = super.serializeBinary();
        this.isSerialising = false;

        return wireFormat;
    }

    private nullToNegative(value: number | undefined | null) {
        if (typeof value === "undefined" || value === null) {
            value = -1;
        }
        return value;
    }
}

export function makeEstradaRoad(pbattribute: { [name: string]: any }): EstradaRoad {
    return makeEstradaObject(EstradaRoad, pbattribute) as EstradaRoad;
}

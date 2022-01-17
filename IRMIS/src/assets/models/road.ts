import { Road } from "../../../protobuf/roads_pb";
import { IAsset } from "./estradaBase";
import { EstradaMedia, makeEstradaMedia, Media } from "./media";
import { makeEstradaProjection } from "./projection";

import {
    choice_or_default,
    getFieldName,
    getHelpText,
    makeEstradaObject,
    toChainageFormat,
} from "../protoBufUtilities";

import {
    ADMINISTRATIVE_AREA_CHOICES, ASSET_CLASS_CHOICES, ASSET_CONDITION_CHOICES,
    MAINTENANCE_NEED_CHOICES, PAVEMENT_CLASS_CHOICES, ROAD_STATUS_CHOICES,
    SURFACE_TYPE_CHOICES, TECHNICAL_CLASS_CHOICES, TRAFFIC_LEVEL_CHOICES,
    FACILITY_TYPE_CHOICES, ECONOMIC_AREA_CHOICES,
    CONNECTION_TYPE_CHOICES, CORE_CHOICES,
    // TERRAIN_CLASS_CHOICES, // Not currently used
} from "./choices";

const assetSchema = JSON.parse(document.getElementById("asset_schema")?.textContent || "");

// tslint:disable: max-classes-per-file

export class EstradaRoad extends Road implements IAsset {
    public static getFieldName(field: string) {
        // handle survey only fields
        switch (field) {
            case "total_width":
                return "Total Width";
        }

        return getFieldName(assetSchema, field);
    }

    public getFieldName(field: string) {
        return EstradaRoad.getFieldName(field);
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
    static get assetType() {
        return "ROAD";
    }

    get assetType() {
        return EstradaRoad.assetType;
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

    /** Please use `name` in preference to `roadName` */
    get roadName() {
        return this.getRoadName();
    }

    /** Please use `code` in preference to `roadCode` */
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
        return this.getNullableLinkStartChainage();
    }

    get linkEndName() {
        return this.getLinkEndName();
    }

    get linkEndChainage() {
        return this.getNullableLinkEndChainage();
    }

    get linkCode() {
        return this.getLinkCode();
    }

    get linkLength() {
        const linkLength = this.getNullableLinkLength();
        if (linkLength === null) {
            return linkLength;
        }

        return linkLength.toFixed(3);
    }

    get constructionYear() {
        const constructionYear = this.getNullableConstructionYear();
        if (constructionYear === null) {
            return constructionYear;
        }

        return constructionYear.toFixed(0);
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

    get core() {
        return choice_or_default(this.getCore().toString(), CORE_CHOICES);
    }

    get technicalClass() {
        return choice_or_default(this.getTechnicalClass(), TECHNICAL_CLASS_CHOICES);
    }

    get maintenanceNeed() {
        return choice_or_default(this.getMaintenanceNeed(), MAINTENANCE_NEED_CHOICES);
    }

    get trafficLevel() {
        return choice_or_default(this.getTrafficLevel(), TRAFFIC_LEVEL_CHOICES);
    }

    get servedFacilities() {
        return this.getServedFacilitiesList()
            .map((id) => choice_or_default(id.toString(), FACILITY_TYPE_CHOICES));
    }

    get servedEconomicAreas() {
        return this.getServedEconomicAreasList()
            .map((id) => choice_or_default(id.toString(), ECONOMIC_AREA_CHOICES));
    }

    get servedConnectionTypes() {
        return this.getServedConnectionTypesList()
            .map((id) => choice_or_default(id.toString(), CONNECTION_TYPE_CHOICES));
    }

    get rainfallMaximum() {
        return this.getNullableRainfallMaximum();
    }

    get rainfallMinimum() {
        return this.getNullableRainfallMinimum();
    }


    get projectionStart() {
        const projectionStartRaw = this.getProjectionStart();
        return projectionStartRaw ? makeEstradaProjection(projectionStartRaw) : projectionStartRaw;
    }

    get projectionEnd() {
        const projectionEndRaw = this.getProjectionEnd();
        return projectionEndRaw ? makeEstradaProjection(projectionEndRaw) : projectionEndRaw;
    }

    get startDMS() {
        return this.projectionStart ? this.projectionStart.dms : "";
    }

    get endDMS() {
        return this.projectionEnd ? this.projectionEnd.dms : "";
    }

    get startUTM() {
        return this.projectionStart ? this.projectionStart.utm : "";
    }

    get endUTM() {
        return this.projectionEnd ? this.projectionEnd.utm : "";
    }

    get numberLanes() {
        return this.getNullableNumberLanes();
    }

    get inventoryMedia(): EstradaMedia[] | undefined {
        const inventoryMediaListRaw = this.getInventoryMediaList();
        return inventoryMediaListRaw ? inventoryMediaListRaw.map(makeEstradaMedia) : inventoryMediaListRaw;
    }

    set inventoryMedia(values: EstradaMedia[] | undefined) {
        this.setInventoryMediaList(values as Media[]);
    }

    get surveyMedia(): EstradaMedia[] | undefined {
        const surveyMediaListRaw = this.getSurveyMediaList();
        return surveyMediaListRaw ? surveyMediaListRaw.map(makeEstradaMedia) : surveyMediaListRaw;
    }

    set surveyMedia(values: EstradaMedia[] | undefined) {
        this.setSurveyMediaList(values as Media[]);
    }

    get population() {
        return this.getNullablePopulation();
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableRainfallMaximum() {
        const rainfall = super.getRainfallMaximum();
        return (rainfall >= 0 || this.isSerialising) ? rainfall : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableRainfallMinimum() {
        const rainfall = super.getRainfallMinimum();
        return (rainfall >= 0 || this.isSerialising) ? rainfall : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullablePopulation() {
        const population = super.getPopulation();
        return (population >= 0 || this.isSerialising) ? population : null;
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
    public getNullableConstructionYear() {
        const constructionYear = super.getConstructionYear();
        return (constructionYear >= 0 || this.isSerialising) ? constructionYear : null;
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

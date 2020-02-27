import dayjs from "dayjs";

import { Survey } from "../../../protobuf/survey_pb";
import { IEstrada } from "./estradaBase";

import { getFieldName, getHelpText, makeEstradaObject } from "../protoBufUtilities";

// We may need a survey schema - primarily for formatted field names
// JSON.parse(document.getElementById('survey_schema').textContent);
const surveySchema = {};

export class EstradaSurvey extends Survey implements IEstrada {
    public static getFieldName(field: string) {
        return getFieldName(surveySchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(surveySchema, field);
    }

    get id() {
        return this.getId();
    }

    get roadCode() {
        return this.getRoadCode();
    }

    get user() {
        return this.getUser() || "";
    }

    get addedBy() {
        return this.getAddedBy() || "";
    }

    get chainageStart() {
        return this.getChainageStart();
    }

    get chainageEnd() {
        return this.getChainageEnd();
    }

    get dateSurveyed() {
        // Note getDateSurveyed doesn't actually return a proper Timestamp object
        const pbufData = this.getDateSurveyed() as ({ [name: string]: any } | undefined);
        if (!pbufData || !pbufData.array || !pbufData.array.length) {
            return "";
        }
        const date = dayjs(new Date(pbufData.array[0] * 1000));
        return date.isValid() ? date.format("YYYY-MM-DD") : "";
    }

    get source() {
        return this.getSource();
    }

    // All of the `values` defined in 'make_road_surveys.py' should also be present
    // in the following `get` properties
    get assetCondition() {
        const assetCondition = this.values.asset_condition
            || this.values.structure_condition
            || undefined;
        return assetCondition;
    }

    set assetCondition(value: string) {
        this.setValue(value, "asset_condition");
        this.setValue(value, "structure_condition");
    }

    get conditionDescription() {
        return this.values.condition_description;
    }

    set conditionDescription(value: string) {
        this.setValue(value, "condition_description");
    }

    get surfaceType() {
        return this.values.surface_type;
    }

    set surfaceType(value: string) {
        this.setValue(value, "surface_type");
    }

    get pavementClass() {
        return this.values.pavement_class;
    }

    set pavementClass(value: string) {
        this.setValue(value, "pavement_class");
    }

    get technicalClass() {
        return this.values.technical_class;
    }

    set technicalClass(value: string) {
        this.setValue(value, "technical_class");
    }

    get terrainClass() {
        return this.values.terrain_class;
    }

    set terrainClass(value: string) {
        this.setValue(value, "terrain_class");
    }

    get trafficLevel() {
        return this.values.traffic_level;
    }

    set trafficLevel(value: string) {
        this.setValue(value, "traffic_level");
    }

    get numberLanes() {
        return this.values.number_lanes as number;
    }

    set numberLanes(value: number) {
        this.setValue(value, "number_lanes");
    }

    get carriagewayWidth() {
        return this.values.carriageway_width as number;
    }

    set carriagewayWidth(value: number) {
        this.setValue(value, "carriageway_width");
    }

    get rainfall() {
        return this.values.rainfall as number;
    }

    set rainfall(value: number) {
        this.setValue(value, "rainfall");
    }

    get trafficSurveyedDate() {
        if (this.values.forecastYear) {
            return this.values.forecastYear;
        } else {
            return this.values.surveyFromDate;
        }
    }

    get trafficCounts() {
        return this.values.counts || {};
    }

    set trafficCounts(value: any) {
        this.setValue(value, "counts");
    }

    get trafficCountTotal() {
        return this.values.countTotal || 0;
    }

    set trafficCountTotal(value: number) {
        this.setValue(value, "countTotal");
    }

    get trafficDataType() {
        return this.values.trafficType || "Unknown";
    }

    set trafficDataType(value: any) {
        this.setValue(value, "trafficType");
    }

    get values() {
        const jsonValues = this.getValues() || "{}";
        return JSON.parse(jsonValues);
    }

    private setValue(value: any, fieldName: string) {
        const values = this.values;
        values[fieldName] = value;
        this.setValues(JSON.stringify(values));
    }
}

export function makeEstradaSurvey(pbsurvey: { [name: string]: any }): EstradaSurvey {
    return makeEstradaObject(EstradaSurvey, pbsurvey) as EstradaSurvey;
}

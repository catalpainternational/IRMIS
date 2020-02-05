import dayjs from "dayjs";

import { Survey } from "../../../protobuf/survey_pb";
import { PAVEMENT_CLASS_CHOICES, SURFACE_TYPE_CHOICES, TECHNICAL_CLASS_CHOICES, TERRAIN_CLASS_CHOICES, TRAFFIC_LEVEL_CHOICES } from "./road";
import { ASSET_CONDITION_CHOICES } from "./asset";

import { choice_or_default, getFieldName, getHelpText } from "../protoBufUtilities";

// We may need a survey schema - primarily for formatted field names
// JSON.parse(document.getElementById('survey_schema').textContent);
const surveySchema = {};

export class EstradaSurvey extends Survey {

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
        const pbufData = this.getDateSurveyed();
        if (!pbufData || !pbufData.array) {
            return "";
        }
        let date = dayjs(new Date(pbufData.array[0] * 1000));
        return date.isValid() ? date.format('YYYY-MM-DD') : "";
    }

    get source() {
        return this.getSource();
    }

    // All of the `values` defined in 'make_road_surveys.py' should also be present
    // in the following `get` properties
    get assetCondition() {
        const asset_condition = this.values.asset_condition
            || this.values.surface_condition
            || this.values.structure_condition
            || undefined;
        return choice_or_default(asset_condition, ASSET_CONDITION_CHOICES);     
    }

    get surfaceType() {
        return choice_or_default(this.values.surface_type, SURFACE_TYPE_CHOICES);
    }

    get pavementClass() {
        return choice_or_default(this.values.pavement_class, PAVEMENT_CLASS_CHOICES);
    }

    get technicalClass() {
        return choice_or_default(this.values.technical_class, TECHNICAL_CLASS_CHOICES);
    }

    get terrainClass() {
        return choice_or_default(this.values.terrain_class, TERRAIN_CLASS_CHOICES);
    }

    get trafficLevel() {
        return choice_or_default(this.values.traffic_level, TRAFFIC_LEVEL_CHOICES);
    }

    get numberLanes() {
        return this.values.number_lanes;
    }

    get carriagewayWidth() {
        return this.values.carriageway_width;
    }

    get rainfall() {
        return this.values.rainfall;
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

    get trafficCountTotal() {
        return this.values.countTotal || 0;
    }

    get trafficDataType() {
        return this.values.trafficType || "Unknown";
    }

    get values() {
        const jsonValues = this.getValues() || "{}";
        return JSON.parse(jsonValues);
    }

    getFieldName(field) {
        return getFieldName(surveySchema, field);
    }

    getHelpText(field) {
        return getHelpText(surveySchema, field);
    }
}

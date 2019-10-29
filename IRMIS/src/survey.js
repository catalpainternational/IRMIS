import dayjs from "dayjs";

import { Survey } from "../protobuf/survey_pb";
import { SURFACE_CONDITION_CHOICES, TRAFFIC_LEVEL_CHOICES } from "./road";

import { choice_or_empty, toChainageFormat } from "./assets/protoBufUtilities";

// We may need a survey schema - primarily for formatted field names
// JSON.parse(document.getElementById('survey_schema').textContent);
const surveySchema = {};

export class EstradaSurvey extends Survey {

    get id() {
        return this.getId();
    }

    get road() {
        return this.getRoad();
    }

    get user() {
        return this.getUser() || "";
    }

    get addedBy() {
        return this.getAddedBy() || "";
    }

    get chainageStart() {
        return toChainageFormat(this.getChainageStart());
    }

    get chainageEnd() {
        return toChainageFormat(this.getChainageEnd());
    }

    get dateSurveyed() {
        let date = dayjs(new Date(this.getDateSurveyed() * 1000));
        return date.isValid() ? date.format('YYYY-MM-DD HH:mm') : "";
    }

    get source() {
        return this.getSource();
    }

    get surfaceCondition() {
        return choice_or_empty(JSON.parse(this.getValues())['surface_condition'], SURFACE_CONDITION_CHOICES);
    }

    get trafficLevel() {
        return choice_or_empty(JSON.parse(this.getValues())['traffic_level'], TRAFFIC_LEVEL_CHOICES);
    }
}

export function getFieldName(field) {
    return (surveySchema[field]) ? surveySchema[field].display : "";
}

export function getHelpText(field) {
    return (surveySchema[field]) ? surveySchema[field].help_text : "";
}

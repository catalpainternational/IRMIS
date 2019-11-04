import dayjs from "dayjs";

import { Survey } from "../protobuf/survey_pb";
import { SURFACE_CONDITION_CHOICES, SURFACE_TYPE_CHOICES, TECHNICAL_CLASS_CHOICES, TRAFFIC_LEVEL_CHOICES } from "./road";

import { choice_or_empty } from "./assets/protoBufUtilities";

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
        return date.isValid() ? date.format('YYYY-MM-DD HH:mm') : "";
    }

    get source() {
        return this.getSource();
    }

    get surfaceCondition() {
        return choice_or_empty(JSON.parse(this.getValues())['surface_condition'], SURFACE_CONDITION_CHOICES);
    }

    get surfaceType() {
        return choice_or_empty(JSON.parse(this.getValues())['surface_type'], SURFACE_TYPE_CHOICES);
    }

    get technicalClass() {
        return choice_or_empty(JSON.parse(this.getValues())['technical_class'], TECHNICAL_CLASS_CHOICES);
    }

    get trafficLevel() {
        return choice_or_empty(JSON.parse(this.getValues())['traffic_level'], TRAFFIC_LEVEL_CHOICES);
    }

    get numberLanes() {
        return JSON.parse(this.getValues())['number_lanes'];
    }
}

export function getFieldName(field) {
    return (surveySchema[field]) ? surveySchema[field].display : "";
}

export function getHelpText(field) {
    return (surveySchema[field]) ? surveySchema[field].help_text : "";
}

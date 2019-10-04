// We'll have a protobuf import going in here
// import { Survey } from "../protobuf/surveys_pb";

// We may need a survey schema - primarily for formatted field names
// const surveySchema = JSON.parse(document.getElementById('survey_schema').textContent);

// utility function to pick from choices if value is truthy, or return empty string
function choice_or_empty(value, choices) {
    return value ? choices[value] : '';
}

function toChainageFormat(value) {
    const distance = parseFloat(value).toFixed(0);
    const meters = `000${distance.substr(-3)}`.substr(-3);
    const kilometers = `${distance.substr(0, distance.length - 3)}` || 0;

    return `${kilometers}+${meters}`;
}

export class EstradaSurvey extends Survey {

    get id() {
        return this.getId();
    }

    get name() {
        return this.getRoadName();
    }

    get code() {
        return this.getRoadCode();
    }

    get linkName() {
        return `${this.getLinkStartName()} - ${this.getLinkEndName()}`;
    }

    get linkStartName() {
        return this.getLinkStartName();
    }

    get linkStartChainage() {
        return toChainageFormat(this.getLinkStartChainage());
    }

    get linkEndName() {
        return this.getLinkEndName();
    }

    get linkEndChainage() {
        return toChainageFormat(this.getLinkEndChainage());
    }

    get linkCode() {
        return this.getLinkCode();
    }

    get linkLength() {
        return parseFloat(this.getLinkLength()).toFixed(2);
    }

    get status() {
        return choice_or_empty(this.getRoadStatus(), ROAD_STATUS_CHOICES);
    }

    get type() {
        return choice_or_empty(this.getRoadType(), ROAD_TYPE_CHOICES);
    }

    get surfaceType() {
        return choice_or_empty(this.getSurfaceType(), SURFACE_TYPE_CHOICES);
    }

    get surfaceCondition() {
        return choice_or_empty(this.getSurfaceCondition(), SURFACE_CONDITION_CHOICES);
    }

    get pavementClass() {
        return choice_or_empty(this.getPavementClass(), PAVEMENT_CLASS_CHOICES);
    }

    get administrativeArea() {
        return choice_or_empty(parseInt(this.getAdministrativeArea()), ADMINISTRATIVE_AREA_CHOICES);
    }

    get carriagewayWidth() {
        return parseFloat(this.getCarriagewayWidth()).toFixed(1);
    }

    get project() {
        return this.getProject();
    }

    get fundingSource() {
        return this.getFundingSource();
    }

    get technicalClass() {
        return choice_or_empty(this.getTechnicalClass(), TECHNICAL_CLASS_CHOICES);
    }

    get maintenanceNeed() {
        return choice_or_empty(this.getMaintenanceNeed(), MAINTENANCE_NEED_CHOICES);
    }

    get trafficLevel() {
        return choice_or_empty(this.getTrafficLevel(), TRAFFIC_LEVEL_CHOICES);
    }

    get projectionStart() {
        return this.getProjectionStart();
    }

    get projectionEnd() {
        return this.getProjectionEnd();
    }

    get startDMS() {
        return toDms(projToWGS84.forward(this.getProjectionStart().array));
    }

    get endDMS() {
        return toDms(projToWGS84.forward(this.getProjectionEnd().array));
    }

    get startUTM() {
        return toUtm(projToWGS84.forward(this.getProjectionStart().array));
    }

    get endUTM() {
        return toUtm(projToWGS84.forward(this.getProjectionEnd().array));
    }

}

// export function getFieldName(field) {
//     return (surveySchema[field]) ? surveySchema[field].display : "";
// }

// export function getHelpText(field) {
//     return (surveySchema[field]) ? surveySchema[field].help_text : "";
// }

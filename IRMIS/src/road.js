import { Road, Roads } from "../protobuf/roads_pb";

var roadSchema = JSON.parse(document.getElementById('road_schema').textContent);

function humanizeChoices(choiceField, valueKey=false, displayKey=false) {
    let values = {};
    valueKey = valueKey || 0;
    displayKey = displayKey || 1;
    roadSchema[choiceField].options.forEach(function(o){
        values[o[valueKey]] = o[displayKey];
    });
    return values;
}

// utility function to pick from choices if value is truthy, or return empty string
function choice_or_empty(value, choices) {
    return value ? choices[value] : '';
}

const ROAD_STATUS_CHOICES = humanizeChoices('road_status', 'code', 'name');
const ROAD_TYPE_CHOICES = humanizeChoices('road_type');
const SURFACE_TYPE_CHOICES = humanizeChoices('surface_type', 'code', 'name');
const SURFACE_CONDITION_CHOICES = humanizeChoices('surface_condition');
const PAVEMENT_CLASS_CHOICES = humanizeChoices('pavement_class', 'code', 'name');
const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices('administrative_area', 'id', 'name');
const TECHNICAL_CLASS_CHOICES = humanizeChoices('technical_class', 'code', 'name');
const MAINTENANCE_NEED_CHOICES = humanizeChoices('maintenance_need', 'code', 'name');
const TRAFFIC_LEVEL_CHOICES = humanizeChoices('traffic_level');

export class EstradaRoad extends Road {

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
        return this.getLinkStartChainage();
    }

    get linkEndName() {
        return this.getLinkEndName();
    }

    get linkEndChainage() {
        return this.getLinkEndChainage();
    }

    get linkCode() {
        return this.getLinkCode();
    }

    get linkLength() {
        return this.getLinkLength();
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
        return this.getCarriagewayWidth();
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
}

export function getFieldName(field) {
    if (roadSchema[field]) { return roadSchema[field].display; }
    else { return ""; }
}

window.getHelpText = (field) => {
    if (roadSchema[field]) { return roadSchema[field].help_text; }
    else { return ""; }
}

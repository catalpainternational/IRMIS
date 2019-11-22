import { Road } from "../../../protobuf/roads_pb";

import { projToWGS84, toDms, toUtm } from "../crsUtilities";
import { choice_or_default, getFieldName, getHelpText, humanizeChoices, toChainageFormat } from "../protoBufUtilities";

const roadSchema = JSON.parse(document.getElementById('road_schema').textContent);

const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices(roadSchema, 'administrative_area', 'id', 'name');
const MAINTENANCE_NEED_CHOICES = humanizeChoices(roadSchema, 'maintenance_need', 'code', 'name');
const PAVEMENT_CLASS_CHOICES = humanizeChoices(roadSchema, 'pavement_class', 'code', 'name');
export const ROAD_STATUS_CHOICES = humanizeChoices(roadSchema, 'road_status', 'code', 'name');
const ROAD_TYPE_CHOICES = humanizeChoices(roadSchema, 'road_type');
export const SURFACE_CONDITION_CHOICES = humanizeChoices(roadSchema, 'surface_condition');
export const SURFACE_TYPE_CHOICES = humanizeChoices(roadSchema, 'surface_type', 'code', 'name');
export const TECHNICAL_CLASS_CHOICES = humanizeChoices(roadSchema, 'technical_class', 'code', 'name');
export const TRAFFIC_LEVEL_CHOICES = humanizeChoices(roadSchema, 'traffic_level');

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
        return choice_or_default(this.getRoadStatus(), ROAD_STATUS_CHOICES);
    }

    get type() {
        return choice_or_default(this.getRoadType(), ROAD_TYPE_CHOICES);
    }

    get surfaceType() {
        return choice_or_default(this.getSurfaceType(), SURFACE_TYPE_CHOICES);
    }

    get surfaceCondition() {
        return choice_or_default(this.getSurfaceCondition(), SURFACE_CONDITION_CHOICES);
    }

    get pavementClass() {
        return choice_or_default(this.getPavementClass(), PAVEMENT_CLASS_CHOICES);
    }

    get administrativeArea() {
        return choice_or_default(parseInt(this.getAdministrativeArea()), ADMINISTRATIVE_AREA_CHOICES);
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
        return choice_or_default(this.getTechnicalClass(), TECHNICAL_CLASS_CHOICES);
    }

    get maintenanceNeed() {
        return choice_or_default(this.getMaintenanceNeed(), MAINTENANCE_NEED_CHOICES);
    }

    get trafficLevel() {
        return choice_or_default(this.getTrafficLevel(), TRAFFIC_LEVEL_CHOICES);
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

    get numberLanes() {
        return this.getNumberLanes();
    }

    static getFieldName(field) {
        return getFieldName(roadSchema, field);
    }
    
    static getHelpText(field) {
        return getHelpText(roadSchema, field);
    }
}

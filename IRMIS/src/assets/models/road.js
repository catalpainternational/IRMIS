import { Road } from "../../../protobuf/roads_pb";

import { projToWGS84, toDms, toUtm } from "../crsUtilities";
import { choice_or_default, getFieldName, getHelpText, humanizeChoices, toChainageFormat } from "../protoBufUtilities";

const roadSchema = JSON.parse(document.getElementById('road_schema').textContent);

const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices(roadSchema, 'administrative_area', 'id', 'name');
const MAINTENANCE_NEED_CHOICES = humanizeChoices(roadSchema, 'maintenance_need', 'code', 'name');
export const PAVEMENT_CLASS_CHOICES = humanizeChoices(roadSchema, 'pavement_class', 'code', 'name');
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
        const linkLength = this.getLinkLength();
        if (linkLength === null) {
            return linkLength;
        }

        return parseFloat(linkLength * 1000).toFixed(2);
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
        const carriagewayWidth = this.getCarriagewayWidth();
        if (carriagewayWidth === null) {
            return carriagewayWidth;
        }

        return parseFloat(carriagewayWidth).toFixed(1);
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

    /** A Null or None in the protobuf is indicated by a negative value */
    getLinkStartChainage() {
        const linkStartChainage = super.getLinkStartChainage();
        return (linkStartChainage >= 0 || this.isSerialising) ? linkStartChainage : null;
    }
   
    /** A Null or None in the protobuf is indicated by a negative value */
    getLinkEndChainage() {
        const linkEndChainage = super.getLinkEndChainage();
        return (linkEndChainage >= 0 || this.isSerialising) ? linkEndChainage : null;
    }
   
    /** A Null or None in the protobuf is indicated by a negative value */
    getLinkLength() {
        const linkLength = super.getLinkLength();
        return (linkLength >= 0 || this.isSerialising) ? linkLength : null;
    }
   
    /** A Null or None in the protobuf is indicated by a negative value */
    getCarriagewayWidth() {
        const carriagewayWidth = super.getCarriagewayWidth();
        return (carriagewayWidth >= 0 || this.isSerialising) ? carriagewayWidth : null;
    }
   
    /** A Null or None in the protobuf is indicated by a negative value */
    getNumberLanes() {
        const numberLanes = super.getNumberLanes();
        return (numberLanes >= 0 || this.isSerialising) ? numberLanes : null;
    }

    nullToNegative(value) {
        if (typeof value === "undefined" || value === null) {
            value = -1;
        }
        return value;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    setLinkStartChainage(value) {
        super.getLinkStartChainage(this.nullToNegative(value));
    }
    
    /** A Null or None in the protobuf is indicated by a negative value */
    setLinkEndChainage(value) {
        super.setLinkEndChainage(this.nullToNegative(value));
    }
    
    /** A Null or None in the protobuf is indicated by a negative value */
    setLinkLength(value) {
        super.setLinkLength(this.nullToNegative(value));
    }
    
    /** A Null or None in the protobuf is indicated by a negative value */
    setCarriagewayWidth(value) {
        super.setCarriagewayWidth(this.nullToNegative(value));
    }
    
    /** A Null or None in the protobuf is indicated by a negative value */
    setNumberLanes(value) {
        super.setNumberLanes(this.nullToNegative(value));
    }

    serializeBinary() {
        // prepare the nullable numerics for serialisation
        this.isSerialising = true;
        const wireFormat = super.serializeBinary();
        this.isSerialising = false;

        return wireFormat;
    }

    static getFieldName(field) {
        return getFieldName(roadSchema, field);
    }
    
    static getHelpText(field) {
        return getHelpText(roadSchema, field);
    }
}

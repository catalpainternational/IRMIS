import { Bridge, Culvert } from "../../../protobuf/structure_pb";
import { projToWGS84, toDms } from "../crsUtilities";
import { choice_or_default, getFieldName, getHelpText, humanizeChoices, toChainageFormat } from "../protoBufUtilities";

const assetSchema = JSON.parse(document.getElementById("asset_schema").textContent);

export const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices(assetSchema, 'administrative_area', 'id', 'name');
export const STRUCTURE_CONDITION_CHOICES = humanizeChoices(assetSchema, 'structure_condition', 'code', 'name');


// We may need a collection of Structure schemas - primarily for formatted field names
// JSON.parse(document.getElementById('<structureType>_schema').textContent);
const structureSchemas = {
    bridge: {},
    culvert: {},
};

export class EstradaBridge extends Bridge {

    get id() {
        return this.getId();
    }

    get name() {
        return this.getStructureName();
    }

    get roadCode() {
        return this.getRoadCode();
    }

    get user() {
        return this.getUser() || "";
    }

    get dms() {
        return toDms(projToWGS84.forward(this.getProjectionStart().array));
    }

    get chainage() {
        return toChainageFormat(this.getChainage());
    }

    get structureCondition() {
        return choice_or_default(this.getStructureCondition(), STRUCTURE_CONDITION_CHOICES);
    }

    get conditionDescription() {
        return this.getConditionDescription();
    }

    get administrativeArea() {
        return choice_or_default(parseInt(this.getAdministrativeArea()), ADMINISTRATIVE_AREA_CHOICES);
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    getChainage() {
        const chainage = super.getChainage();
        return (chainage >= 0 || this.isSerialising) ? chainage : null;
    }

    static getFieldName(field) {
        return getFieldName(structureSchemas.bridge, field);
    }

    static getHelpText(field) {
        return getHelpText(structureSchemas.bridge, field);
    }
}

export class EstradaCulvert extends Culvert {

    get id() {
        return this.getId();
    }

    get name() {
        return this.getStructureName();
    }

    get roadCode() {
        return this.getRoadCode();
    }

    get user() {
        return this.getUser() || "";
    }

    get dms() {
        return toDms(projToWGS84.forward(this.getProjectionStart().array));
    }

    get chainage() {
        return toChainageFormat(this.getChainage());
    }

    get structureCondition() {
        return choice_or_default(this.getStructureCondition(), STRUCTURE_CONDITION_CHOICES);
    }

    get conditionDescription() {
        return this.getConditionDescription();
    }

    get administrativeArea() {
        return choice_or_default(parseInt(this.getAdministrativeArea()), ADMINISTRATIVE_AREA_CHOICES);
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    getChainage() {
        const chainage = super.getChainage();
        return (chainage >= 0 || this.isSerialising) ? chainage : null;
    }

    static getFieldName(field) {
        return getFieldName(structureSchemas.culvert, field);
    }

    static getHelpText(field) {
        return getHelpText(structureSchemas.culvert, field);
    }
}

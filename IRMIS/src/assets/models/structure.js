// import { Structure } from "../../../protobuf/structures_pb";

// import { projToWGS84, toDms, toUtm } from "../crsUtilities";
import { choice_or_default, getFieldName, getHelpText, humanizeChoices, toChainageFormat } from "../protoBufUtilities";

const assetSchema = JSON.parse(document.getElementById("asset_schema").textContent);

export const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices(assetSchema, 'administrative_area', 'id', 'name');
export const STRUCTURE_CONDITION_CHOICES = humanizeChoices(assetSchema, 'structure_condition', 'code', 'name');


// export class EstradaStructure extends Structure {
export class EstradaStructure {
        get id() {
        return this.getId();
    }

    get name() {
        return this.getStructureName();
    }

    get code() {
        return this.getStructureCode();
    }

    get Chainage() {
        return toChainageFormat(this.getChainage());
    }

    get RoadCode() {
        return this.getRoadCode();
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

    get structureCondition() {
        return choice_or_default(this.getStructureCondition(), STRUCTURE_CONDITION_CHOICES);
    }

    get conditionDescription() {
        return this.getConditionDescription();
    }

    get inventoryPhoto() {
        return this.getInventoryPhoto();
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

    serializeBinary() {
        // prepare the nullable numerics for serialisation
        this.isSerialising = true;
        const wireFormat = super.serializeBinary();
        this.isSerialising = false;

        return wireFormat;
    }

    static getFieldName(field) {
        return getFieldName(assetSchema, field);
    }

    static getHelpText(field) {
        return getHelpText(assetSchema, field);
    }
}

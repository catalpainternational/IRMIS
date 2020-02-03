import { Bridge, Culvert, Structures } from "../../../protobuf/structure_pb";
import { projToWGS84, toDms } from "../crsUtilities";
import { choice_or_default, getFieldName, getHelpText, humanizeChoices, makeEstradaObject, toChainageFormat } from "../protoBufUtilities";

const assetSchema = JSON.parse(document.getElementById("asset_schema").textContent);

// export const STRUCTURE_CONDITION_CHOICES = humanizeChoices(assetSchema, 'structure_condition', 'code', 'name');
export const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices(assetSchema, 'administrative_area', 'id', 'name');
export const STRUCTURE_CLASS_CHOICES = humanizeChoices(assetSchema, 'structure_class');
export const STRUCTURE_UPSTREAM_PROTECTION_TYPE_CHOICES = humanizeChoices(assetSchema, 'protection_upstream', 'code', 'name');
export const STRUCTURE_DOWNSTREAM_PROTECTION_TYPE_CHOICES = humanizeChoices(assetSchema, 'protection_downstream', 'code', 'name');
export const STRUCTURE_TYPE_BRIDGE_CHOICES = humanizeChoices(assetSchema, 'structure_type', 'code', 'name');
export const STRUCTURE_TYPE_CULVERT_CHOICES = humanizeChoices(assetSchema, 'structure_type', 'code', 'name');
export const MATERIAL_TYPE_BRIDGE_CHOICES = humanizeChoices(assetSchema, 'material', 'code', 'name');
export const MATERIAL_TYPE_CULVERT_CHOICES = humanizeChoices(assetSchema, 'material', 'code', 'name');

// We may need a collection of Structure schemas - primarily for formatted field names
// JSON.parse(document.getElementById('<structureType>_schema').textContent);
const structureSchemas = {
    bridge: {},
    culvert: {},
};

export class EstradaStructures extends Structures {
    get id() {
        return "StructuresWrapperClass";
    }

    get bridges() {
        const bridgesListRaw = this.getBridgesList() || [];
        return bridgesListRaw.map(this.makeEstradaBridge);
    }

    get culverts() {
        const culvertsListRaw = this.getCulvertsList() || [];
        return culvertsListRaw.map(this.makeEstradaCulvert);
    }

    getObject() {
        const structures = {};
        this.bridges.forEach((bridge) => {
            if (bridge.id) {
                structures[bridge.id] = bridge;
            }
        });
        this.culverts.forEach((culvert) => {
            if (culvert.id) {
                structures[culvert.id] = culvert;
            }
        });

        return structures;
    }

    makeEstradaBridge(pbattribute) {
        return makeEstradaObject(EstradaBridge, pbattribute);
    }

    makeEstradaCulvert(pbattribute) {
        return makeEstradaObject(EstradaCulvert, pbattribute);
    }
}

export class EstradaBridge extends Bridge {

    get id() {
        return this.getId();
    }

    get name() {
        return this.getStructureName();
    }

    get structureCode() {
        return this.getStructureCode();
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

    get administrativeArea() {
        return choice_or_default(parseInt(this.getAdministrativeArea()), ADMINISTRATIVE_AREA_CHOICES);
    }

    get constructionYear() {
        return this.getConstructionYear();
    }

    get length() {
        return this.getLength();
    }

    get width() {
        return this.getWidth();
    }

    get riverName() {
        return this.getRiverName();
    }

    get numberSpans() {
        return this.getNumberSpans();
    }

    get spanLength() {
        return this.getSpanLength();
    }

    get structureClass() {
        return choice_or_default(this.getStructureClass(), STRUCTURE_CLASS_CHOICES);
    }

    get structureType() {
        return choice_or_default(this.getStructureType(), STRUCTURE_TYPE_BRIDGE_CHOICES );
    }

    get material() {
        return choice_or_default(this.getMaterial(), MATERIAL_TYPE_BRIDGE_CHOICES);
    }

    get protectionUpstream() {
        return choice_or_default(this.getProtectionUpstream(), STRUCTURE_UPSTREAM_PROTECTION_TYPE_CHOICES);
    }

    get protectionDownstream() {
        return choice_or_default(this.getProtectionDownstream(), STRUCTURE_DOWNSTREAM_PROTECTION_TYPE_CHOICES);
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

    get structureCode() {
        return this.getStructureCode();
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

    get administrativeArea() {
        return choice_or_default(parseInt(this.getAdministrativeArea()), ADMINISTRATIVE_AREA_CHOICES);
    }

    get constructionYear() {
        return this.getConstructionYear();
    }

    get length() {
        return this.getLength();
    }

    get width() {
        return this.getWidth();
    }

    get height() {
        return this.getHeight();
    }

    get numberCells() {
        return this.getNumberCells();
    }

    get structureClass() {
        return choice_or_default(this.getStructureClass(), STRUCTURE_CLASS_CHOICES);
    }

    get structureType() {
        return choice_or_default(this.getStructureType(), STRUCTURE_TYPE_CULVERT_CHOICES );
    }

    get material() {
        return choice_or_default(this.getMaterial(), MATERIAL_TYPE_CULVERT_CHOICES);
    }

    get protectionUpstream() {
        return choice_or_default(this.getProtectionUpstream(), STRUCTURE_UPSTREAM_PROTECTION_TYPE_CHOICES);
    }

    get protectionDownstream() {
        return choice_or_default(this.getProtectionDownstream(), STRUCTURE_DOWNSTREAM_PROTECTION_TYPE_CHOICES);
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

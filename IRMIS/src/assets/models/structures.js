import { Bridge, Culvert, Structures } from "../../../protobuf/structure_pb";
import { projToWGS84, toDms } from "../crsUtilities";
import { choice_or_default, getFieldName, getHelpText, humanizeChoices, makeEstradaObject, toChainageFormat } from "../protoBufUtilities";

import { ADMINISTRATIVE_AREA_CHOICES, ASSET_CLASS_CHOICES, ASSET_CONDITION_CHOICES } from "./asset";

const assetSchema = JSON.parse(document.getElementById("asset_schema").textContent);

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

    /** The asset's type - the prefix part of its Id */
    get assetType() {
        return "BRDG";
    }

    get assetTypeName() {
        return window.gettext("Bridge");
    }

    /** Return just the asset's Id without the assetType prefix */
    get assetId() {
        return this.id.startsWith(this.assetType)
            ? this.id.split("-")[1]
            : this.id
    }

    get code() {
        return this.structureCode;
    }

    get name() {
        return this.structureName;
    }

    get structureCode() {
        return this.getStructureCode();
    }

    get structureName() {
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

    get assetClass() {
        return choice_or_default(this.getAssetClass(), ASSET_CLASS_CHOICES);
    }

    get assetCondition() {
        return choice_or_default(this.getAssetCondition(), ASSET_CONDITION_CHOICES);
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

    /** The asset's type - the prefix part of its Id */
    get assetType() {
        return "CULV";
    }

    get assetTypeName() {
        return window.gettext("Culvert");
    }

    /** Return just the asset's Id without the assetType prefix */
    get assetId() {
        return this.id.startsWith(this.assetType)
            ? this.id.split("-")[1]
            : this.id
    }

    get code() {
        return this.structureCode;
    }

    get name() {
        return this.structureName;
    }

    get structureCode() {
        return this.getStructureCode();
    }

    get structureName() {
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

    get assetClass() {
        return choice_or_default(this.getAssetClass(), ASSET_CLASS_CHOICES);
    }

    get assetCondition() {
        return choice_or_default(this.getAssetCondition(), ASSET_CONDITION_CHOICES);
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

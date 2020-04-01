import { Bridge, Culvert, Structures } from "../../../protobuf/structure_pb";
import { Photo } from "../../../protobuf/photo_pb";

import { EstradaPhoto, makeEstradaPhoto } from "./photo";
import { makeEstradaProjection } from "./road";

import {
    choice_or_default,
    getFieldName,
    getHelpText,
    humanizeChoices,
    makeEstradaObject,
    toChainageFormat,
} from "../protoBufUtilities";

import { ADMINISTRATIVE_AREA_CHOICES, ASSET_CLASS_CHOICES, ASSET_CONDITION_CHOICES, IAsset, IEstrada } from "./estradaBase";

const assetSchema = JSON.parse(document.getElementById("asset_schema")?.textContent || "");

export const STRUCTURE_UPSTREAM_PROTECTION_TYPE_CHOICES = humanizeChoices(assetSchema, "protection_upstream", "code", "name");
export const STRUCTURE_DOWNSTREAM_PROTECTION_TYPE_CHOICES
    = humanizeChoices(assetSchema, "protection_downstream", "code", "name");
export const STRUCTURE_TYPE_BRIDGE_CHOICES = humanizeChoices(assetSchema, "structure_type_BRDG", "code", "name");
export const STRUCTURE_TYPE_CULVERT_CHOICES = humanizeChoices(assetSchema, "structure_type_CULV", "code", "name");
export const MATERIAL_TYPE_BRIDGE_CHOICES = humanizeChoices(assetSchema, "material_BRDG", "code", "name");
export const MATERIAL_TYPE_CULVERT_CHOICES = humanizeChoices(assetSchema, "material_CULV", "code", "name");

// tslint:disable: max-classes-per-file

// We may need a collection of Structure schemas - primarily for formatted field names
// JSON.parse(document.getElementById('<structureType>_schema').textContent);
const structureSchemas = {
    bridge: {},
    culvert: {},
};

export class EstradaStructures extends Structures implements IEstrada {
    get id() {
        return this.getId();
    }

    public getId() {
        return "StructuresWrapperClass";
    }

    get bridges() {
        const bridgesListRaw = this.getBridgesList() || [];
        return bridgesListRaw.map(makeEstradaBridge);
    }

    get culverts() {
        const culvertsListRaw = this.getCulvertsList() || [];
        return culvertsListRaw.map(makeEstradaCulvert);
    }

    public getObject() {
        const structures: { [name: string]: any } = {};
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
}

export class EstradaBridge extends Bridge implements IAsset {
    public static getFieldName(field: string) {
        if (assetSchema[`${field}_${EstradaBridge.assetType}`]) {
            return assetSchema[`${field}_${EstradaBridge.assetType}`].display || "";
        }
        return getFieldName(assetSchema, field);
    }

    public getFieldName(field: string) {
        return EstradaBridge.getFieldName(field);
    }

    public static getHelpText(field: string) {
        return getHelpText(assetSchema, field);
    }

    private isSerialising: boolean;

    public constructor() {
        super();
        this.isSerialising = false;
    }

    get id() {
        return this.getId();
    }

    /** The asset's type - the prefix part of its Id */
    static get assetType() {
        return "BRDG";
    }

    get assetType() {
        return EstradaBridge.assetType;
    }

    get assetTypeName() {
        return (window as any).gettext("Bridge");
    }

    /** Return just the asset's Id without the assetType prefix */
    get assetId() {
        return this.id.startsWith(this.assetType)
            ? this.id.split("-")[1]
            : this.id;
    }

    // generic version of the getStructureCode() function for Map use
    get code() {
        return this.getStructureCode();
    }

    // generic version of the getStructureName() function for Map use
    get name() {
        return this.getStructureName();
    }

    /** Please use `code` in preference to `structureCode` */
    get structureCode() {
        return this.getStructureCode();
    }

    /** Please use `name` in preference to `structureName` */
    get structureName() {
        return this.getStructureName();
    }

    get roadCode() {
        return this.getRoadCode();
    }

    get roadId() {
        return this.getRoadId();
    }

    // get user() {
    //     return this.getUser() || "";
    // }

    get geomPoint() {
        const geomPointRaw = this.getGeomPoint();
        return geomPointRaw ? makeEstradaProjection(geomPointRaw) : geomPointRaw;
    }

    get dms() {
        return this.geomPoint ? this.geomPoint.dms : "";
    }

    get chainage() {
        return toChainageFormat(this.getNullableChainage());
    }

    get administrativeArea() {
        return choice_or_default(this.getAdministrativeArea(), ADMINISTRATIVE_AREA_CHOICES);
    }

    get constructionYear() {
        return this.getNullableConstructionYear();
    }

    get length() {
        return this.getNullableLength();
    }

    get width() {
        return this.getNullableWidth();
    }

    get riverName() {
        return this.getRiverName();
    }

    get numberSpans() {
        return this.getNullableNumberSpans();
    }

    get spanLength() {
        return this.getNullableSpanLength();
    }

    get assetClass() {
        return choice_or_default(this.getAssetClass(), ASSET_CLASS_CHOICES);
    }

    get structureType() {
        return choice_or_default(this.getStructureType(), STRUCTURE_TYPE_BRIDGE_CHOICES);
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

    get inventoryPhotos(): EstradaPhoto[] | undefined {
        const inventoryPhotosListRaw = this.getInventoryPhotosList();
        return inventoryPhotosListRaw ? inventoryPhotosListRaw.map(makeEstradaPhoto) : inventoryPhotosListRaw;
    }

    set inventoryPhotos(values: EstradaPhoto[] | undefined) {
        this.setInventoryPhotosList(values as Photo[]);
    }

    get surveyPhotos(): EstradaPhoto[] | undefined {
        const surveyPhotosListRaw = this.getSurveyPhotosList();
        return surveyPhotosListRaw ? surveyPhotosListRaw.map(makeEstradaPhoto) : surveyPhotosListRaw;
    }

    set surveyPhotos(values: EstradaPhoto[] | undefined) {
        this.setSurveyPhotosList(values as Photo[]);
    }

    /** assetCondition is the most recent structure condition from the surveys */
    get assetCondition() {
        return choice_or_default(this.getAssetCondition(), ASSET_CONDITION_CHOICES);
    }

    /** conditionDescription is the most recent condition description from the surveys */
    get conditionDescription() {
        return this.getConditionDescription();
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableChainage() {
        const chainage = super.getChainage();
        return (chainage >= 0 || this.isSerialising) ? chainage : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableConstructionYear() {
        const constructionYear = super.getConstructionYear();
        return (constructionYear >= 0 || this.isSerialising) ? constructionYear : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableLength() {
        const length = super.getLength();
        return (length >= 0 || this.isSerialising) ? length : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableWidth() {
        const width = super.getWidth();
        return (width >= 0 || this.isSerialising) ? width : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableNumberSpans() {
        const numberSpans = super.getNumberSpans();
        return (numberSpans >= 0 || this.isSerialising) ? numberSpans : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableSpanLength() {
        const spanLength = super.getSpanLength();
        return (spanLength >= 0 || this.isSerialising) ? spanLength : null;
    }
}

export class EstradaCulvert extends Culvert implements IAsset {
    public static getFieldName(field: string) {
        if (assetSchema[`${field}_${EstradaCulvert.assetType}`]) {
            return assetSchema[`${field}_${EstradaCulvert.assetType}`].display || "";
        }
        return getFieldName(assetSchema, field);
    }

    public getFieldName(field: string) {
        return EstradaCulvert.getFieldName(field);
    }

    private isSerialising: boolean;

    public constructor() {
        super();
        this.isSerialising = false;
    }

    get id() {
        return this.getId();
    }

    /** The asset's type - the prefix part of its Id */
    static get assetType() {
        return "CULV";
    }

    get assetType() {
        return EstradaCulvert.assetType;
    }

    get assetTypeName() {
        return (window as any).gettext("Culvert");
    }

    /** Return just the asset's Id without the assetType prefix */
    get assetId() {
        return this.id.startsWith(this.assetType)
            ? this.id.split("-")[1]
            : this.id;
    }

    // generic version of the getStructureCode() function for Map use
    get code() {
        return this.getStructureCode();
    }

    // generic version of the getStructureName() function for Map use
    get name() {
        return this.getStructureName();
    }

    /** Please use `code` in preference to `structureCode` */
    get structureCode() {
        return this.getStructureCode();
    }

    /** Please use `name` in preference to `structureName` */
    get structureName() {
        return this.getStructureName();
    }

    get roadCode() {
        return this.getRoadCode();
    }

    get roadId() {
        return this.getRoadId();
    }

    // get user() {
    //     return this.getUser() || "";
    // }

    get geomPoint() {
        const geomPointRaw = this.getGeomPoint();
        return geomPointRaw ? makeEstradaProjection(geomPointRaw) : geomPointRaw;
    }

    get dms() {
        return this.geomPoint ? this.geomPoint.dms : "";
    }

    get chainage() {
        return toChainageFormat(this.getNullableChainage());
    }

    get administrativeArea() {
        return choice_or_default(this.getAdministrativeArea(), ADMINISTRATIVE_AREA_CHOICES);
    }

    get constructionYear() {
        return this.getNullableConstructionYear();
    }

    get length() {
        return this.getNullableLength();
    }

    get width() {
        return this.getNullableWidth();
    }

    get height() {
        return this.getNullableHeight();
    }

    get numberCells() {
        return this.getNullableNumberCells();
    }

    get assetClass() {
        return choice_or_default(this.getAssetClass(), ASSET_CLASS_CHOICES);
    }

    get structureType() {
        return choice_or_default(this.getStructureType(), STRUCTURE_TYPE_CULVERT_CHOICES);
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

    get inventoryPhotos(): EstradaPhoto[] | undefined {
        const inventoryPhotosListRaw = this.getInventoryPhotosList();
        return inventoryPhotosListRaw ? inventoryPhotosListRaw.map(makeEstradaPhoto) : inventoryPhotosListRaw;
    }

    set inventoryPhotos(values: EstradaPhoto[] | undefined) {
        this.setInventoryPhotosList(values as Photo[]);
    }

    get surveyPhotos(): EstradaPhoto[] | undefined {
        const surveyPhotosListRaw = this.getSurveyPhotosList();
        return surveyPhotosListRaw ? surveyPhotosListRaw.map(makeEstradaPhoto) : surveyPhotosListRaw;
    }

    set surveyPhotos(values: EstradaPhoto[] | undefined) {
        this.setSurveyPhotosList(values as Photo[]);
    }

    /** assetCondition is the most recent structure condition from the surveys */
    get assetCondition() {
        return choice_or_default(this.getAssetCondition(), ASSET_CONDITION_CHOICES);
    }

    /** conditionDescription is the most recent condition description from the surveys */
    get conditionDescription() {
        return this.getConditionDescription();
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableChainage() {
        const chainage = super.getChainage();
        return (chainage >= 0 || this.isSerialising) ? chainage : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableConstructionYear() {
        const constructionYear = super.getConstructionYear();
        return (constructionYear >= 0 || this.isSerialising) ? constructionYear : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableLength() {
        const length = super.getLength();
        return (length >= 0 || this.isSerialising) ? length : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableWidth() {
        const width = super.getWidth();
        return (width >= 0 || this.isSerialising) ? width : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableHeight() {
        const height = super.getHeight();
        return (height >= 0 || this.isSerialising) ? height : null;
    }

    /** A Null or None in the protobuf is indicated by a negative value */
    public getNullableNumberCells() {
        const numberCells = super.getNumberCells();
        return (numberCells >= 0 || this.isSerialising) ? numberCells : null;
    }
}

export function makeEstradaStructures(pbstructures: { [name: string]: any }): EstradaStructures {
    return makeEstradaObject(EstradaStructures, pbstructures) as EstradaStructures;
}

export function makeEstradaBridge(pbattribute: { [name: string]: any }): EstradaBridge {
    return makeEstradaObject(EstradaBridge, pbattribute) as EstradaBridge;
}

export function makeEstradaCulvert(pbattribute: { [name: string]: any }): EstradaCulvert {
    return makeEstradaObject(EstradaCulvert, pbattribute) as EstradaCulvert;
}

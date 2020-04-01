import { getFieldName, getHelpText, humanizeChoices } from "../protoBufUtilities";

const assetSchema = JSON.parse(document.getElementById("asset_schema")?.textContent || "");

export const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices(assetSchema, "administrative_area", "id", "name");
export const ASSET_CONDITION_CHOICES = humanizeChoices(assetSchema, "asset_condition");
export const ASSET_CLASS_CHOICES = humanizeChoices(assetSchema, "asset_class");

export function AdminAreaChoices() {
    const adminAreaChoices: { [name: string]: any } = {};
    assetSchema.administrative_area.options.forEach((option: { [name: string]: any }) => {
        adminAreaChoices[option.id] = option.name || option.id;
    });

    return adminAreaChoices;
}

export interface IEstrada {
    id: string | number;
    getId(): string | number;
}

export interface IAsset extends IEstrada {
    // Asset Ids can only be strings
    id: string;
    name: string;
    code: string;

    /** The asset's type - the prefix part of its Id */
    assetType: string;
    /** The asset's type name - in the currently selected language */
    assetTypeName: string;
    /** The asset's Id without the assetType prefix */
    assetId: string;

    // public static methods
    getFieldName(field: string): string;
    // getHelpText(field: string): string;
}

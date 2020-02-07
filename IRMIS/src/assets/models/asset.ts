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

export interface IAsset {
    id: string;
    name: string;
    code: string;

    // public static methods
    // getFieldName(field: string): string;
    // getHelpText(field: string): string;
}

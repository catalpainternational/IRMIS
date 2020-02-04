import { humanizeChoices } from "../protoBufUtilities";

const assetSchema = JSON.parse(document.getElementById("asset_schema").textContent);

export const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices(assetSchema, 'administrative_area', 'id', 'name');
export const ASSET_CONDITION_CHOICES = humanizeChoices(assetSchema, 'asset_condition', 'code', 'name');
export const ASSET_CLASS_CHOICES = humanizeChoices(assetSchema, 'asset_class');

export function AdminAreaChoices() {
    const adminAreaChoices = {};
    asset_schema.administrative_area.options.forEach((option) => {
        adminAreaChoices[option.id] = option.name || option.id;
    });

    return adminAreaChoices;
}
import { humanizeChoices } from "../protoBufUtilities";

const assetSchema = JSON.parse(document.getElementById("asset_schema")?.textContent || "");

// Common to all Assets
export const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices(assetSchema, "administrative_area", "id", "name");
export const ASSET_CONDITION_CHOICES = humanizeChoices(assetSchema, "asset_condition");
export const ASSET_CLASS_CHOICES = humanizeChoices(assetSchema, "asset_class");
export const ASSET_TYPE_CHOICES = humanizeChoices(assetSchema, "asset_type");

// For Roads
export const MAINTENANCE_NEED_CHOICES = humanizeChoices(assetSchema, "maintenance_need", "code", "name");
export const PAVEMENT_CLASS_CHOICES = humanizeChoices(assetSchema, "pavement_class", "code", "name");
export const ROAD_STATUS_CHOICES = humanizeChoices(assetSchema, "road_status", "code", "name");
export const SURFACE_TYPE_CHOICES = humanizeChoices(assetSchema, "surface_type", "code", "name");
export const TECHNICAL_CLASS_CHOICES = humanizeChoices(assetSchema, "technical_class", "code", "name");
export const TRAFFIC_LEVEL_CHOICES = humanizeChoices(assetSchema, "traffic_level");
export const TERRAIN_CLASS_CHOICES = humanizeChoices(assetSchema, "terrain_class");
export const FACILITY_TYPE_CHOICES = humanizeChoices(assetSchema, "facility_type", "code", "name");
export const ECONOMIC_AREA_CHOICES = humanizeChoices(assetSchema, "economic_area", "code", "name");
export const CONNECTION_TYPE_CHOICES = humanizeChoices(assetSchema, "connection_type", "code", "name");
export const CORE_CHOICES = humanizeChoices(assetSchema, "core");

// For Structures
export const STRUCTURE_UPSTREAM_PROTECTION_TYPE_CHOICES = humanizeChoices(assetSchema, "protection_upstream", "code", "name");
export const STRUCTURE_DOWNSTREAM_PROTECTION_TYPE_CHOICES
    = humanizeChoices(assetSchema, "protection_downstream", "code", "name");
export const STRUCTURE_TYPE_BRIDGE_CHOICES = humanizeChoices(assetSchema, "structure_type_BRDG", "code", "name");
export const STRUCTURE_TYPE_CULVERT_CHOICES = humanizeChoices(assetSchema, "structure_type_CULV", "code", "name");
export const MATERIAL_TYPE_BRIDGE_CHOICES = humanizeChoices(assetSchema, "material_BRDG", "code", "name");
export const MATERIAL_TYPE_CULVERT_CHOICES = humanizeChoices(assetSchema, "material_CULV", "code", "name");
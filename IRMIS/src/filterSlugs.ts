// tslint:disable: object-literal-sort-keys

// we'll need to add more in here as we add more filters
export const slugToPropertyGetter: {[name: string]: string} = {
    // Common
    administrative_area: "getAdministrativeArea",
    asset_class: "getAssetClass",
    asset_condition: "getAssetCondition",
    asset_type: "assetType",
    // Common-ish
    road_code: "getRoadCode",
    structure_code: "getStructureCode",
    // Road
    surface_type: "getSurfaceType",
    road_status: "getRoadStatus",
};

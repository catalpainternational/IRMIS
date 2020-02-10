import { dispatch } from "./assets/utilities";
import { assetTypeName } from "./side_menu";

/* Hold the state for the global filter
 * expose methods that change or query the global filter
 * communicate the filter function to the map and table
 * */
let filterState = {};

// we'll need to add more in here as we add more filters
export const slugToPropertyGetter = {
    // Common
    administrative_area: "getAdministrativeArea",
    asset_class: "getAssetClass",
    asset_condition: "getAssetCondition",
    asset_type: "getAssetType",
    // Common-ish
    road_code: "getRoadCode",
    structure_code: "getStructureCode",
    // Road
    surface_type: "getSurfaceType",
    road_status: "getRoadStatus",
    // Structure
    asset_type: "assetType",
};

/** applies or unapplies the value to the slug filter */
export function toggleFilter(slug, value) {
    initFilter(slug);
    let slugFilterValues = filterState[slug];
    let index = slugFilterValues.indexOf(value);
    if (index === -1) {
        slugFilterValues.push(value);
    } else {
        slugFilterValues.splice(index, 1);
    }
    applyFilter();
}

/** ensures the slug filterstate is ready for adding values */
function initFilter(slug) {
    if (!filterState.hasOwnProperty(slug)) {
        filterState[slug] = [];
    }
}

/** is slug=value filter active */
export function isFilterApplied(slug, value) {
    initFilter(slug);
    return filterState[slug].indexOf(value) !== -1;
}

/** clear a slug filter */
export function clearFilter(slug) {
    filterState[slug] = [];
    applyFilter();
}

/** clear all slug filters */
export function clearAllFilters() {
    filterState = {};
    applyFilter();
}

/** actually make the filter happen */
export function applyFilter() {
    const eventName = (assetTypeName !== "STRC")
        ? "estrada.road.filter.apply"
        : "estrada.structure.filter.apply";
    dispatch(eventName, { detail: { filterState } });
}

/** Get the common filter details from the event */
export function filterDetail(e) {
    const element = e.currentTarget;
    const filter = element.closest('.filter');
    const slug = filter.attributes['data-slug'].value;
    const header = filter.querySelector('.header');

    return { element, filter, slug, header };
}

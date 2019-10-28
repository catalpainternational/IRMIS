/* Hold the state for the global filter
 * expose methods that change or query the global filter
 * communicate the filter function to the map and table
 * */
let filterState = {};


// we'll need to add more in here as we add more filters
export const slugToPropertyGetter = {
    road_code: 'getRoadCode',
    road_type: 'getRoadType',
    surface_type: 'getSurfaceType',
    surface_condition: 'getSurfaceCondition',
    road_status: 'getRoadStatus',
    administrative_area: 'getAdministrativeArea',
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
    document.dispatchEvent(new CustomEvent("estrada.filter.apply", { "detail": { filterState } }));
}

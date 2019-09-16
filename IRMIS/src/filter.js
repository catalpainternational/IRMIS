/* Hold the state for the global filter
 * expose methods that change or query the global filter
 * communicate the filter function to the map and table
 * */


let filterState = {};


// applies or unapplies the value to the slug filter
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

// ensures the slug filterstate is ready for adding values
function initFilter(slug) {
    if( !filterState.hasOwnProperty(slug) ) filterState[slug] = [];
}

// is slug=value filter active
export function isFilterApplied(slug, value) {
    initFilter(slug);
    return filterState[slug].indexOf(value) !== -1;
}

// clear a slug filter
export function clearFilter(slug) {
    filterState[slug] = [];
    applyFilter();
}

// clear a slug filter
export function clearAllFilters() {
    filterState = {};
    applyFilter();
}

// actually make the filter happen
function applyFilter() {
    document.dispatchEvent(new CustomEvent("estrada.filter.apply", {"detail": { filterState }}));
}

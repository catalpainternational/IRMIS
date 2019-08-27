/* Hold the state for the global filter
 * expose methods that change or query the global filter
 * communicate the filter function to the map and table
 * */

import { filterFeatures } from "./map/map_simple.js"
import { filterRows } from "./table.js"

let filterState = {};

// we'll need to add more in here as we add more filters
const slugToPropertyName = {
    road_type: 'roadType',
    surface_type: 'surfaceType',
    surface_condition: 'surfaceCondition',
    road_status: 'roadStatus',
    administrative_area: 'administrativeArea',
};

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

    // filter function passed to map and table
    function filter(properties) {
        // every filter state must match
        return Object.entries(filterState).every(([slug, values]) => {
            // empty array means all match
            if (values.length === 0) return true;
            // or some values of one state must match
            return values.some(value => {
                let propertyName = slugToPropertyName[slug];
                return properties[propertyName] === value;
            });
        });
    }

    // communicate the filter
    filterRows(filter);
    filterFeatures(filter);
}

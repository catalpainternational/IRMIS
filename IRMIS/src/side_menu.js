import { toggleFilter, isFilterApplied, applyFilter, clearFilter } from './filter';

const filters = ["road-condition", "road-code"];

let filterUIState = {};

export function collapse_side_menu() {
    const collapsedSideMenu = document.getElementById("collapsed-side-menu");
    const mapTable = document.getElementById("map-table-irmis");
    const sideMenu = document.getElementById("side-menu");

    mapTable.style.maxWidth = "calc(100% - 30px)";
    mapTable.style.flex = "0 0 100%";
    sideMenu.hidden = true;
    collapsedSideMenu.classList.add("d-flex");
    roads.map.lMap.invalidateSize();
}

export function expand_side_menu() {
    const collapsedSideMenu = document.getElementById("collapsed-side-menu");
    const mapTable = document.getElementById("map-table-irmis");
    const sideMenu = document.getElementById("side-menu");

    mapTable.style.maxWidth = "75%";
    mapTable.style.flex = "0 0 75%";
    sideMenu.hidden = false;
    collapsedSideMenu.classList.remove("d-flex");
    roads.map.lMap.invalidateSize();
}

export function change_view(element, view) {
    const mapTable = document.getElementById("map-table-irmis");
    const siblings = document.getElementById("view").children;

    if (view === 0) {
        mapTable.className = "col-9 map table";
    } else if (view === 1) {
        mapTable.className = "col-9 map";
    } else {
        mapTable.className = "col-9 table";
    }

    for (let index = 0; index < siblings.length; index += 1) {
        const sibling = siblings[index];
        if (sibling !== element) { sibling.classList.remove("active"); }
    }
    element.classList.add("active");
    roads.map.lMap.invalidateSize();
}

export function toggleFilterOption(element, elementId, value) {
    const filterBlock = document.getElementById(elementId);
    const clear = filterBlock.getElementsByClassName("clear-filter").item(0);
    const header = filterBlock.getElementsByClassName("header").item(0);
    const checkbox = element.getElementsByTagName("span").item(0);

    checkbox.classList.toggle("selected");
    if (filterBlock.getElementsByClassName("selected").length) {
        header.classList.add("active");
        clear.hidden = false;
    } else {
        header.classList.remove("active");
    }
    toggleFilter(elementId, value);
    clear.hidden = !isFilterApplied(elementId, value);
    applyFilter();
}

export function toggleFilterOpen(element, elementId) {
    const filter = document.getElementById(elementId);
    const options = filter.getElementsByClassName("options").item(0);

    toggleFilterUIState(elementId);
    if (element.classList.contains("plus")) {
        element.classList.replace("plus", "minus");
    } else {
        element.classList.replace("minus", "plus");
    }
    options.hidden = !isFilterOpen(elementId);
}

function isFilterOpen(elementId) {
    initFilterUIState(elementId);
    return filterUIState[elementId];
}

function initFilterUIState(elementId) {
    if( !filterUIState.hasOwnProperty(elementId) ) filterUIState[elementId] = false;
}

function toggleFilterUIState(elementId) {
    initFilterUIState(elementId);
    filterUIState[elementId] = !filterUIState[elementId];
}

export function clear_filter(elementId) {
    const filter = document.getElementById(elementId);
    const checkboxes = filter.getElementsByClassName("selected");
    while (checkboxes.length) {
        checkboxes[0].classList.remove("selected");
    }
    filter.getElementsByClassName("header").item(0).classList.remove("active");
    filter.getElementsByClassName("clear-filter").item(0).hidden = true;
    clearFilter(elementId);
    applyFilter();
}

export function clear_all_filters() {
    filters.forEach(filter => clear_filter(filter));
}

import { toggleFilter, isFilterApplied, clearFilter, clearAllFilters } from './filter';
import { table } from './table';
import $ from "jquery";
import "select2";

const filters = ["road_code", "road_type", "surface_type", "surface_condition", "road_status", "administrative_area"];
const select2_filters = ["road_code", "administrative_area"];

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

    mapTable.style.removeProperty('max-width');
    mapTable.style.removeProperty('flex');
    sideMenu.hidden = false;
    collapsedSideMenu.classList.remove("d-flex");
    roads.map.lMap.invalidateSize();
}

export function change_view(element, view) {
    const mapTable = document.getElementById("map-table-irmis");
    const siblings = document.getElementById("view").children;

    if (view === 0) {
        mapTable.className = "col-8 col-lg-9 col-xl-10 map table";
        table.page.len(10).draw('page');
    } else if (view === 1) {
        mapTable.className = "col-8 col-lg-9 col-xl-10 map";
    } else {
        mapTable.className = "col-8 col-lg-9 col-xl-10 table";
        table.page.len(20).draw('page');
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
    const select2 = select2_filters.includes(elementId);

    if (!select2) {
        const checkbox = element.getElementsByTagName("span").item(0);
        checkbox.classList.toggle("selected");
    }

    if (select2 && value != -1 || filterBlock.getElementsByClassName("selected").length > 0) {
        header.classList.add("active");
        clear.hidden = false;
    } else {
        header.classList.remove("active");
        clear.hidden = true;
    }

    toggleFilter(elementId, value);
}

export function toggleFilterOpen(element, elementId) {
    const filter = document.getElementById(elementId);
    const header = filter.getElementsByClassName("header").item(0);
    const options = filter.getElementsByClassName("options").item(0);

    toggleFilterUIState(elementId);
    if (element.classList.contains("plus")) {
        element.classList.replace("plus", "minus");
    } else {
        element.classList.replace("minus", "plus");
    }
    header.classList.toggle('open');
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
    const select2 = select2_filters.includes(elementId);

    if (!select2) {
        const checkboxes = filter.getElementsByClassName("selected");
        while (checkboxes.length) {
            checkboxes[0].classList.remove("selected");
        }
    } else {
        // trigger clearing of select2
        $("#" + elementId + "_select").val([]).trigger('change');
    }
    filter.getElementsByClassName("header").item(0).classList.remove("active");
    filter.getElementsByClassName("clear-filter").item(0).hidden = true;
    clearFilter(elementId);
}

export function clear_all_filters() {
    filters.forEach(filter => clear_filter(filter));
    clearAllFilters();
}


$(document).ready(function(){
    // setup rode_code and administrative_area filters with select2
    $('#road_code_select').select2();
    $('#administrative_area_select').select2();
    // event listeners to trigger filters on changes in select2 options
    $('#road_code_select').on('select2:select', function (e) {
        var data = e.params.data;
        roads.toggleFilterOption(this, 'road_code', data.id);
    });
    $('#road_code_select').on('select2:unselect', function (e) {
        var data = e.params.data;
        roads.toggleFilterOption(this, 'road_code', data.id);
    });
    $('#administrative_area_select').on('select2:select', function (e) {
        var data = e.params.data;
        roads.toggleFilterOption(this, 'administrative_area', data.id);
    });
    $('#administrative_area_select').on('select2:unselect', function (e) {
        var data = e.params.data;
        roads.toggleFilterOption(this, 'administrative_area', data.id);
    });
});

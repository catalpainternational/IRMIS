import $ from "jquery";
import "select2/dist/js/select2.full.min.js";

import { dispatch } from "./assets/utilities";

import { toggleFilter, clearFilter, clearAllFilters, filterDetail, isFilterApplied } from "./filter";

let filterUIState = {};

$(document).ready(function(){
    // setup road_code and administrative_area filters with select2
    $('.filter_select2').select2({
        width: "100%",
        containerCssClass: "filter-select2",
        dropdownCssClass: "filter-dropdown-select2",
    });
    // event listeners to trigger filters on changes in select2 options
    $('.filter_select2').on('select2:select', toggleFilterSelect2);
    $('.filter_select2').on('select2:unselect', toggleFilterSelect2);

    // hide and show the side menu
    $('#side-menu-collapse').click(collapse_side_menu);
    $('#collapsed-side-menu').click(expand_side_menu);

    // switch map and table views
    $('#view a').click(change_view);

    // switch asset types
    $('#assetType a').click(toggleAssetType);

    // toggle filter open/close
    $('.filterToggle').click(toggleFilterOpen);

    // clear filters
    $('.clear-all-filters').click(clear_all_filters);
    $('.clear-filter').click(clear_filter);
    $('.clear-select2').click(clear_select2);

    // select options
    $('.optionToggle').click(toggleFilterOption);
});

function collapse_side_menu() {
    const collapsedSideMenu = document.getElementById("collapsed-side-menu");
    const mapTable = document.getElementById("map-table-irmis");
    const sideMenu = document.getElementById("side-menu");

    mapTable.style.maxWidth = "calc(100% - 30px)";
    mapTable.style.flex = "0 0 100%";
    sideMenu.hidden = true;
    collapsedSideMenu.classList.add("d-flex");

    const eventName = (assetTypeName === "STRC")
        ? "estrada.roadTable.sideMenu.viewChanged"
        : "estrada.structureTable.sideMenu.viewChanged";
    dispatch(eventName, undefined);
}

function expand_side_menu() {
    const collapsedSideMenu = document.getElementById("collapsed-side-menu");
    const mapTable = document.getElementById("map-table-irmis");
    const sideMenu = document.getElementById("side-menu");

    mapTable.style.removeProperty('max-width');
    mapTable.style.removeProperty('flex');
    sideMenu.hidden = false;
    collapsedSideMenu.classList.remove("d-flex");

    const eventName = (assetTypeName === "STRC")
        ? "estrada.roadTable.sideMenu.viewChanged"
        : "estrada.structureTable.sideMenu.viewChanged";
    dispatch(eventName, undefined);
}

function change_view(e) {
    const viewName = e.currentTarget.attributes['data-viewname'].value;
    const mapTable = document.getElementById("map-table-irmis");
    const siblings = document.getElementById("view").children;

    mapTable.className = viewName;

    for (let index = 0; index < siblings.length; index += 1) {
        const sibling = siblings[index];
        if (sibling !== e.currentTarget) {
            sibling.classList.remove("active");
        }
    }
    e.currentTarget.classList.add("active");

    const eventName = (assetTypeName === "STRC")
        ? "estrada.roadTable.sideMenu.viewChanged"
        : "estrada.structureTable.sideMenu.viewChanged";
    dispatch(eventName, { "detail": { viewName } });
}

/** assetTypeName is the current selection of the Asset Type filter switch */
export let assetTypeName = "ROAD"; // or "STRC" for structures, i.e. bridges and culverts

function toggleAssetType(e) {
    const fd = filterDetail(e);
    assetTypeName = fd.element.attributes["data-option"].value;

    const siblings = document.getElementById("assetType").getElementsByTagName("a");
    const filterSections = document.getElementsByClassName("filters-section");

    for (let index = 0; index < siblings.length; index++) {
        const sibling = siblings[index];
        if (sibling !== e.currentTarget) {
            sibling.classList.remove("active");
        }
    }
    e.currentTarget.classList.add("active");

    for (let index = 0; index < filterSections.length; index++) {
        const filterSection = filterSections[index];
        const sectionClasses = filterSection.classList;
        if (sectionClasses.contains(assetTypeName)) {
            filterSection.removeAttribute("hidden");
        } else {
            filterSection.setAttribute("hidden", true)
        }
    }

    // Swap road and structures table
    const roadTable = document.getElementById("table-roads");
    const structureTable = document.getElementById("table-structures");

    if (assetTypeName === "ROAD") {
        roadTable.removeAttribute("hidden");
        structureTable.setAttribute("hidden", true);
    } else {
        roadTable.setAttribute("hidden", true);
        structureTable.removeAttribute("hidden");
    }

    const eventName = (assetTypeName !== "STRC")
        ? "estrada.roadTable.sideMenu.assetTypeChanged"
        : "estrada.structureTable.sideMenu.assetTypeChanged";
    dispatch(eventName, { "detail": { assetTypeName } });

    const roadValues = ["Road"];
    const structureValues = ["Structure", "bridge", "culvert"];

    const onValues = (assetTypeName !== "STRC") ? roadValues : structureValues;
    const offValues = (assetTypeName !== "STRC") ? structureValues : roadValues;

    onValues.forEach((on) => {
        if (!isFilterApplied(fd.slug, on)) {
            toggleFilter(fd.slug, on);
        }
    });
    offValues.forEach((off) => {
        if (isFilterApplied(fd.slug, off)) {
            toggleFilter(fd.slug, off);
        }
    });
}

function toggleFilterSelect2(e) {
    const fd = filterDetail(e);
    const value = e.params.data.id;
    const clear = fd.filter.querySelector(".clear-select2");

    if (fd.element.value !== "") {
        fd.header.classList.add("active");
        clear.hidden = false;
    } else {
        fd.header.classList.remove("active");
        clear.hidden = true;
    }

    toggleFilter(fd.slug, value);
}

function toggleFilterOption(e) {
    const fd = filterDetail(e);
    const value = fd.element.attributes['data-option'].value;
    const clear = fd.filter.querySelector(".clear-filter");
    const checkbox = fd.element.querySelector("span");

    checkbox.classList.toggle("selected");

    if (fd.filter.getElementsByClassName("selected").length > 0) {
        fd.header.classList.add("active");
        clear.hidden = false;
    } else {
        fd.header.classList.remove("active");
        clear.hidden = true;
    }

    toggleFilter(fd.slug, value);
}

function toggleFilterOpen(e) {
    const fd = filterDetail(e);
    const options = fd.filter.querySelector('.options');

    toggleFilterUIState(fd.slug);
    if (fd.element.classList.contains("plus")) {
        fd.element.classList.replace("plus", "minus");
    } else {
        fd.element.classList.replace("minus", "plus");
    }
    fd.header.classList.toggle('open');
    options.hidden = !isFilterOpen(fd.slug);
}

function clear_filter(e) {
    const fd = filterDetail(e);
    const clear = fd.filter.getElementsByClassName("clear-filter");
    const checkboxes = fd.filter.getElementsByClassName("selected");

    while (checkboxes.length) {
        checkboxes[0].classList.remove("selected");
    }
    fd.header.classList.remove("active");
    clear.item(0).hidden = true;
    clearFilter(fd.slug);
}

function clear_select2(e) {
    const fd = filterDetail(e);
    const clear = fd.filter.querySelector(".clear-select2");

    // trigger clearing of select2
    $(".filter_select2", fd.filter).val([]).trigger('change');

    fd.header.classList.remove("active");
    clear.hidden = true;
    clearFilter(fd.slug);
}

function clear_all_filters() {
    $(".filters .header").removeClass("active");
    $(".filters .clear-filter").attr("hidden", true);
    $(".filters .filter_select2").val([]).trigger('change');
    $(".filters .clear-select2").attr("hidden", true);
    $(".filters .optionToggle span").removeClass("selected");

    clearAllFilters();
}

function isFilterOpen(elementId) {
    initFilterUIState(elementId);
    return filterUIState[elementId];
}

function initFilterUIState(elementId) {
    if( !filterUIState.hasOwnProperty(elementId) ) filterUIState[elementId] = false;
}

function toggleFilterUIState(slug) {
    initFilterUIState(slug);
    filterUIState[slug] = !filterUIState[slug];
}

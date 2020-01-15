import $ from "jquery";
import "select2/dist/js/select2.full.min.js";

import { dispatch } from "./assets/utilities";

import { toggleFilter, clearFilter, clearAllFilters} from './filter';

let filterUIState = {};

$(document).ready(function(){
    // setup rode_code and administrative_area filters with select2
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
    dispatch("estrada.sideMenu.viewChanged", undefined);
}

function expand_side_menu() {
    const collapsedSideMenu = document.getElementById("collapsed-side-menu");
    const mapTable = document.getElementById("map-table-irmis");
    const sideMenu = document.getElementById("side-menu");

    mapTable.style.removeProperty('max-width');
    mapTable.style.removeProperty('flex');
    sideMenu.hidden = false;
    collapsedSideMenu.classList.remove("d-flex");
    dispatch("estrada.sideMenu.viewChanged", undefined);
}

function change_view(e) {
    const viewName = e.currentTarget.attributes['data-viewname'].value;
    const mapTable = document.getElementById("map-table-irmis");
    const siblings = document.getElementById("view").children;

    mapTable.className = viewName;

    for (let index = 0; index < siblings.length; index += 1) {
        const sibling = siblings[index];
        if (sibling !== e.currentTarget) { sibling.classList.remove("active"); }
    }
    e.currentTarget.classList.add("active");

    document.dispatchEvent(new CustomEvent("estrada.sideMenu.viewChanged", { "detail": { viewName } }));

}

function toggleFilterSelect2(e) {
    const element = e.currentTarget;
    const value = e.params.data.id;
    const filter = element.closest('.filter');
    const slug = filter.attributes['data-slug'].value;
    const header = filter.querySelector('.header');
    const clear = filter.querySelector(".clear-select2");

    if (element.value !== "") {
        header.classList.add("active");
        clear.hidden = false;
    } else {
        header.classList.remove("active");
        clear.hidden = true;
    }

    toggleFilter(slug, value);
}

function toggleFilterOption(e) {
    const element = e.currentTarget;
    const value = element.attributes['data-option'].value;

    const filter = element.closest('.filter');
    const slug = filter.attributes['data-slug'].value;
    const clear = filter.querySelector(".clear-filter");
    const header = filter.querySelector('.header');

    const checkbox = element.querySelector("span");
    checkbox.classList.toggle("selected");

    if (filter.getElementsByClassName("selected").length > 0) {
        header.classList.add("active");
        clear.hidden = false;
    } else {
        header.classList.remove("active");
        clear.hidden = true;
    }

    toggleFilter(slug, value);
}

function toggleFilterOpen(e) {
    const element = e.currentTarget;
    const filter = element.closest('.filter');
    const header = filter.querySelector('.header');
    const options = filter.querySelector('.options');
    const slug = filter.attributes['data-slug'].value;

    toggleFilterUIState(slug);
    if (element.classList.contains("plus")) {
        element.classList.replace("plus", "minus");
    } else {
        element.classList.replace("minus", "plus");
    }
    header.classList.toggle('open');
    options.hidden = !isFilterOpen(slug);
}

function clear_filter(e) {
    const element = e.currentTarget;
    const filter = element.closest('.filter');
    const slug = filter.attributes['data-slug'].value;
    const header = filter.querySelector('.header');
    const checkboxes = filter.getElementsByClassName("selected");
    while (checkboxes.length) {
        checkboxes[0].classList.remove("selected");
    }
    header.classList.remove("active");
    filter.getElementsByClassName("clear-filter").item(0).hidden = true;
    clearFilter(slug);
}

function clear_select2(e) {
    const element = e.currentTarget;
    const filter = element.closest('.filter');
    const slug = filter.attributes['data-slug'].value;
    // trigger clearing of select2
    $(".filter_select2", filter).val([]).trigger('change');

    filter.querySelector(".header").classList.remove("active");
    filter.querySelector(".clear-select2").hidden = true;
    clearFilter(slug);
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


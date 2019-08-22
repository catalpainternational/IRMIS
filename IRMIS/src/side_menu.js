const filters = ["road-condition", "road-code"];

export function collapse_side_menu() {
    const collapsedSideMenu = document.getElementById("collapsed-side-menu");
    const sideMenu = document.getElementById("side-menu");
    const mapTable = document.getElementById("map-table");

    mapTable.style.maxWidth = "calc(100% - 30px)";
    mapTable.style.flex = "0 0 100%";
    sideMenu.hidden = true;
    collapsedSideMenu.classList.add("d-flex");
}

export function expand_side_menu() {
    const collapsedSideMenu = document.getElementById("collapsed-side-menu");
    const sideMenu = document.getElementById("side-menu");
    const mapTable = document.getElementById("map-table");

    mapTable.style.maxWidth = "75%";
    mapTable.style.flex = "0 0 75%";
    sideMenu.hidden = false;
    collapsedSideMenu.classList.remove("d-flex");
}

export function change_view(element) {
    const siblings = document.getElementById("view").children;
    for (let index = 0; index < siblings.length; index += 1) {
        const sibling = siblings[index];
        if (sibling !== element) { sibling.classList.remove("active"); }
    }
    element.classList.add("active");
}

export function toggle_filter(element, elementId) {
    const filter = document.getElementById(elementId);
    const options = filter.getElementsByClassName("options").item(0);

    if (element.classList.contains("plus")) {
        element.classList.replace("plus", "minus");
        options.hidden = false;
    } else {
        element.classList.replace("minus", "plus");
        options.hidden = true;
    }
}

export function clear_filter(elementId) {
    const filter = document.getElementById(elementId);
    const checkboxes = filter.getElementsByClassName("selected");
    while (checkboxes.length) {
        checkboxes[0].classList.remove("selected");
    }
    filter.getElementsByClassName("header").item(0).classList.remove("active");
    filter.getElementsByClassName("clear-filter").item(0).hidden = true;
}

export function clear_all_filters() {
    filters.forEach(filter => clear_filter(filter));
}

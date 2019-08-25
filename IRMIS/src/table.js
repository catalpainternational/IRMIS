import "datatables.net-bs4";

import $ from "jquery";

let table;
let currentFilter = (p) => true;

$.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
        let properties = oSettings.aoData[iDataIndex]._aData;
        return currentFilter(properties);
    }
);

export function initializeDataTable(roadList) {

    table = $("#data-table").DataTable({
        columns: [
            { data: "roadCode", title: "Road Code", "defaultContent": "<i>Not set</i>" },
            { data: "roadType", title: "Road Type", "defaultContent": "<i>Not set</i>" },
            { data: "roadName", title: "Road Name", "defaultContent": "<i>Not set</i>" },
            { data: "linkCode", title: "Link Name", "defaultContent": "<i>Not set</i>" },
            { data: "linkLength", title: "Link Length", "defaultContent": "<i>Not set</i>" },
            { data: "surfaceType", title: "Surface Type", "defaultContent": "<i>Not set</i>" },
            { data: "surfaceCondition", title: "Surface Condition", "defaultContent": "<i>Not set</i>" },
        ],
        data: roadList,
        // lengthChange: false, // hide table entries filter
        // searching: false, // hide search box
        search: {
            regex: true, // Enable escaping of regular expression characters in the search term.
        },
    });
}

export function filterRows(filter) {
    currentFilter = filter;
    table.draw();
}

export function toggle_column(element) {
    const checkbox = element.getElementsByClassName("checkbox").item(0);
    const column = table.column(element.dataset.column);
    checkbox.classList.toggle("selected");
    column.visible(!column.visible());
}


// params: (settings, data, dataIndex, row, counter)
/*
function length_search(settings, data) {
    const minLength = parseInt(document.getElementById("min-length-filter").value, 10);
    const maxLength = parseInt(document.getElementById("max-length-filter").value, 10);
    const currLength = parseInt(data[3], 10);

    if (Number.isNaN(minLength) && Number.isNaN(maxLength)) { return true; }
    if (Number.isNaN(minLength) && currLength <= maxLength) { return true; }
    if (Number.isNaN(maxLength) && currLength >= minLength) { return true; }
    if (currLength <= maxLength && currLength >= minLength) { return true; }
    return false;
}

function condition_search(settings, data) {
    const condition = document.getElementById("condition-filter").value;
    const currCondition = data[2];

    if (condition === "" || condition === currCondition) { return true; }
    return false;
}

function code_search(settings, data) {
    const code = document.getElementById("code-filter").value;
    const currCode = data[1];

    if (code === "" || code === currCode) { return true; }
    return false;
}

$.fn.dataTable.ext.search.push(condition_search);
$.fn.dataTable.ext.search.push(length_search);
$.fn.dataTable.ext.search.push(code_search);
*/

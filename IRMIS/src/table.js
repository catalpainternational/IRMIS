import "datatables.net-bs4";
import $ from "jquery";

let table;

let currentFilter = (p) => (true);

$.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
        let properties = oSettings.aoData[iDataIndex]._aData;
        return currentFilter(properties);
    }
);

let defineColumn = (data, title) => ({ data: data, title: title, defaultContent: "<i>Not set</i>"});

export function initializeDataTable(roadList) {
    table = $("#data-table").DataTable({
        columns: [
            defineColumn("roadCode", "Code"),
            defineColumn("roadType", "Type"),
            defineColumn("roadName", "Name"),

            defineColumn("linkCode", "Link Code"),
            defineColumn("linkName", "Link Name"),
            defineColumn("linkStartChainage", "Chainage Start"),
            defineColumn("linkEndChainage", "Chainage End"),
            defineColumn("linkLength", "Link Length"),

            defineColumn("surfaceType", "Surface Type"),
            defineColumn("surfaceCondition", "Surface Condition"),
            defineColumn("pavementClass", "Pavement Class"),

            defineColumn("administrativeArea", "Administrative Area"),
            defineColumn("carriagewayWidth", "Carriageway Width"),
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

import "datatables.net-bs4";
import $ from "jquery";

let table;

let currentFilter = (p) => (true);

function humanize(schema, model, keyArg=false, nameArg=false) {
    let values = {};
    if (keyArg && nameArg) {
        schema[model].options.forEach(function(o){
            values[o[keyArg]] = o[nameArg]
        });
    } else {
        schema[model].options.forEach(function(o){
            values[o[0]] = o[1]
        });
    }
    return values;
}

const ROAD_STATUS_CHOICES = humanize(window.road_schema, 'road_status');
const ROAD_TYPE = humanize(window.road_schema, 'road_type');
const SURFACE_CONDITION_CHOICES = humanize(window.road_schema, 'surface_condition');
const SURFACE_TYPE_CHOICES = humanize(window.road_schema, 'surface_type', 'code', 'name');
const PAVEMENT_CLASS_CHOICES = humanize(window.road_schema, 'pavement_class', 'code', 'name');
// const MAINTENANCE_NEED_CHOICES = humanize(window.road_schema, 'maintenance_need', 'code', 'name');
// const TECHNICAL_CLASS_CHOICES = humanize(window.road_schema, 'technical_class', 'code', 'name');

$.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
        let properties = oSettings.aoData[iDataIndex]._aData;
        return currentFilter(properties);
    }
);

let defineColumn = (data, title, mapObj=false, defaultVal="<i>Not set</i>") => ({
    data: data,
    title: title,
    defaultContent: defaultVal,
    render: item => (mapObj) ? mapObj[item] : item
});

export function initializeDataTable(roadList) {
    table = $("#data-table").DataTable({
        columns: [
            defineColumn("roadCode", "Code"),
            defineColumn("roadType", "Type", ROAD_TYPE),
            defineColumn("roadName", "Name"),

            defineColumn("linkCode", "Link Code"),
            defineColumn("linkName", "Link Name"),
            defineColumn("linkStartChainage", "Chainage Start"),
            defineColumn("linkEndChainage", "Chainage End"),
            defineColumn("linkLength", "Link Length"),

            defineColumn("surfaceType", "Surface Type", SURFACE_TYPE_CHOICES),
            defineColumn("surfaceCondition", "Surface Condition", SURFACE_CONDITION_CHOICES),
            defineColumn("pavementClass", "Pavement Class", PAVEMENT_CLASS_CHOICES),

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

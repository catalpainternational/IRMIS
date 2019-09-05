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

const ROAD_STATUS_CHOICES = humanize(window.road_schema, 'road_status', 'code', 'name');
const ROAD_TYPE_CHOICES = humanize(window.road_schema, 'road_type');
const SURFACE_CONDITION_CHOICES = humanize(window.road_schema, 'surface_condition');
const SURFACE_TYPE_CHOICES = humanize(window.road_schema, 'surface_type', 'code', 'name');
const PAVEMENT_CLASS_CHOICES = humanize(window.road_schema, 'pavement_class', 'code', 'name');
const ADMINISTRATIVE_AREA_CHOICES = humanize(window.road_schema, 'administrative_area', 'id', 'name');
const TECHNICAL_CLASS_CHOICES = humanize(window.road_schema, 'technical_class', 'code', 'name');
const MAINTENANCE_NEED_CHOICES = humanize(window.road_schema, 'maintenance_need', 'code', 'name');
const TRAFFIC_LEVEL_CHOICES = humanize(window.road_schema, 'traffic_level');

$.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
        let properties = oSettings.aoData[iDataIndex]._aData;
        return currentFilter(properties);
    }
);

let defineColumn = (data, title, mapObj=false, defaultVal="<i>Not set</i>", orderable=true) => ({
    data: data,
    title: title,
    defaultContent: defaultVal,
    orderable: orderable,
    render: item => (mapObj) ? mapObj[item] : item
});

export function initializeDataTable(roadList) {
    roadList.forEach((road) => road["edit"] = "<span class='image pencil' onclick='roads.edit_road()'></span>");
    table = $("#data-table").DataTable({
        columns: [
            defineColumn("edit", "", false, "", false),
            defineColumn("roadCode", "Code"),
            defineColumn("roadType", "Type", ROAD_TYPE_CHOICES),
            defineColumn("roadName", "Name"),
            defineColumn("roadStatus", "Status", ROAD_STATUS_CHOICES),

            defineColumn("linkCode", "Link Code"),
            defineColumn("linkName", "Link Name"),
            defineColumn("linkStartName", "Link Start Name"),
            defineColumn("linkStartChainage", "Link Start Chainage"),
            defineColumn("linkEndName", "Link End Name"),
            defineColumn("linkEndChainage", "Link End Chainage"),
            defineColumn("linkLength", "Link Length"),

            defineColumn("surfaceType", "Surface Type", SURFACE_TYPE_CHOICES),
            defineColumn("surfaceCondition", "Surface Condition", SURFACE_CONDITION_CHOICES),
            defineColumn("pavementClass", "Pavement Class", PAVEMENT_CLASS_CHOICES),

            defineColumn("administrativeArea", "Administrative Area", ADMINISTRATIVE_AREA_CHOICES),
            defineColumn("carriagewayWidth", "Carriageway Width"),
            defineColumn("project", "Project"),
            defineColumn("fundingSource", "Funding Source"),
            defineColumn("technicalClass", "Technical Class", TECHNICAL_CLASS_CHOICES),
            defineColumn("maintenanceNeed", "Maintenance Need", MAINTENANCE_NEED_CHOICES),
            defineColumn("trafficLevel", "Traffic Level", TRAFFIC_LEVEL_CHOICES),
        ],
        order: [3, 'asc'], // default order is ascending by name
        data: roadList,
        // lengthChange: false, // hide table entries filter
        // searching: false, // hide search box
    });
}
export function filterRows(filter) {
    currentFilter = filter;
    table.draw();
}

export function edit_road() {
    document.getElementById('edit-content').hidden = false;
    document.getElementById('view-content').hidden = true;
}

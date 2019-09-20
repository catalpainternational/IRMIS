import jsZip from "jszip";
import "datatables.net-bs4";
import "datatables.net-buttons-bs4";
import "datatables.net-buttons/js/buttons.html5";
import "datatables.net-buttons/js/buttons.flash";
import $ from "jquery";

let table;

// needed for export to excel
window.JSZip = jsZip;

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

// when the roadManager has new roads, add them to the table
document.addEventListener('estrada.roadManager.roadMetaDataAdded', (data) => {
    // add the roads to the table
    table.rows.add(data.detail.roadList).draw();
});

document.addEventListener('estrada.table.roadMetaDataUpdated', (data) => {
    table.row(`#${data.detail.getId()}`).data(data.detail).draw();
});

// when a filter is applied, update the filter id whitelist
document.addEventListener('estrada.filter.applied', (data) => {
    idWhitelistMap = data.detail.idMap;
    table.draw();
});

// when the view changes adjust the table rows
document.addEventListener('estrada.sideMenu.viewChanged', (data) => {
    const viewName = data.detail ? data.detail.viewName : null;
    if (viewName === 'map table') {
        table.page.len(10).draw('page');
    } else if (viewName === 'table') {
        table.page.len(20).draw('page');
    }
});

window.addEventListener("load", () => {
    const columnsList = document.getElementById("columns-list");

    document.getElementById("select-data").addEventListener("click", () => {
        columnsList.hidden = !columnsList.hidden;
    });

    columnsList.querySelectorAll("[data-column]").forEach((item) => {
        item.addEventListener("click", (e) => {
            e.stopPropagation();
            const element = e.currentTarget;
            const column = table.column(window.canEdit ? parseInt(element.dataset.column) + 1 : element.dataset.column);
            column.visible(!column.visible());
            element.getElementsByClassName("checkbox").item(0).classList.toggle("selected");
        });
    });

    initializeDataTable();
});

function initializeDataTable() {
    const date = new Date();
    const columns = [
        {
            title: 'Road Code', data: null,
            render: 'getRoadCode',
            type: "roadCode"
        },
        {
            title: 'Road Name', data: null,
            render: 'getRoadName',
            visible: false,
        },
        {
            title: 'Link Code', data: null,
            render: 'getLinkCode'
        },
        {
            title: 'Link Name', data: null,
            render: 'getLinkName',
            visible: false,
        },
        {
            title: 'Link Length (Km)', data: null,
            render: r => parseFloat(r.getLinkLength()).toFixed(2)
        },
        {
            title: 'Link Start Name', data: null,
            render: 'getLinkStartName'
        },
        {
            title: 'Link Start Chainage (Km)', data: null,
            render: r => parseFloat(r.getLinkStartChainage()).toFixed(2)
        },
        {
            title: 'Link End Name', data: null,
            render: 'getLinkEndName'
        },
        {
            title: 'Link End Chainage (Km)', data: null,
            render: r => parseFloat(r.getLinkEndChainage()).toFixed(2)
        },
        {
            title: 'Surface Type', data: null,
            render: r => choice_or_empty(r.getSurfaceType(), SURFACE_TYPE_CHOICES)
        },
        {
            title: 'Pavement Class', data: null,
            render: r => choice_or_empty(r.getPavementClass(), PAVEMENT_CLASS_CHOICES)
        },
        {
            title: 'Carriageway Width (m)', data: null,
            render: r => parseFloat(r.getCarriagewayWidth()).toFixed(2)
        },
        {
            title: 'Administrative Area', data: null,
            render: r => choice_or_empty(parseInt(r.getAdministrativeArea()), ADMINISTRATIVE_AREA_CHOICES)
        },
        {
            title: 'Road Type', data: null,
            render: r => choice_or_empty(r.getRoadType(), ROAD_TYPE_CHOICES),
            visible: false,
        },
        {
            title: 'Technical Class', data: null,
            render: r => choice_or_empty(r.getTechnicalClass(), TECHNICAL_CLASS_CHOICES),
            visible: false,
        },
        {
            title: 'Funding Source', data: null,
            render: 'getFundingSource',
            visible: false,
        },
        {
            title: 'Road Status', data: null,
            render: r => choice_or_empty(r.getRoadStatus(), ROAD_STATUS_CHOICES),
            visible: false,
        },
        {
            title: 'Project', data: null,
            render: 'getProject',
            visible: false,
        },
        {
            title: 'Surface Condition', data: null,
            render: r => choice_or_empty(r.getSurfaceCondition(), SURFACE_CONDITION_CHOICES)
        },
        {
            title: 'Maintenance needs', data: null,
            render: r => choice_or_empty(r.getMaintenanceNeed(), MAINTENANCE_NEED_CHOICES),
            visible: false,
        },
        {
            title: 'Traffic Data', data: null,
            render: r => choice_or_empty(r.getTrafficLevel(), TRAFFIC_LEVEL_CHOICES),
            visible: false,
        }
    ];

    if (window.canEdit) {
        columns.unshift({
            title: '', data: null,
            render: r => `<a class='image pencil' href='#edit/${r.getId()}/location_type'></a>`,
            orderable: false,
            className: "edit-col"
        });
    }

    table = $("#data-table").DataTable({
        columns: columns,
        rowId: '.getId()',
        order: [[window.canEdit ? 1 : 0, 'asc']], // default order is ascending by road code
        dom: `<'row'<'col-12'B>> + <'row'<'col-sm-12'tr>> + <'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>`, // https://datatables.net/reference/option/dom#Styling
        buttons: [{
            extend: "excel",
            className: "btn-sm",
            sheetName: "Estrada",
            text: "Export table",
            title: "Estrada_" + date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate(),
            exportOptions: {
                columns: ":visible",
            },
        }]
    });
}

// Filter functionality
let idWhitelistMap = null;
let currentFilter = (p) => {
    return idWhitelistMap === null || idWhitelistMap[p.getId().toString()];
}

$.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
        let road = oSettings.aoData[iDataIndex]._aData;
        return currentFilter(road);
    }
);

// change the sorting of the road code column to place empty values last
$.extend($.fn.dataTableExt.oSort, {
    "roadCode-asc": function (str1, str2) {
        if(str1 == "") return 1;
        if(str2 == "") return -1;
        return ((str1 < str2) ? -1 : ((str1 > str2) ? 1 : 0));
    },

    "roadCode-desc": function (str1, str2) {
        if(str1 == "") return -1;
        if(str2 == "") return 1;
        return ((str1 < str2) ? 1 : ((str1 > str2) ? -1 : 0));
    }
});

// utility function to pick from choices if value is truthy, or return empty string
function choice_or_empty(value, choices) {
    return value ? choices[value] : '';
}

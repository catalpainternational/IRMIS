import jsZip from "jszip";
import "datatables.net-bs4";
import "datatables.net-buttons-bs4";
import "datatables.net-buttons/js/buttons.html5";
import "datatables.net-buttons/js/buttons.flash";

import $ from "jquery";

import { getRoadMetadata } from "./assets/assets_api.js";

export let table;

let idWhitelistMap = 'all';
let currentFilter = (p) => {
    return idWhitelistMap === 'all' || idWhitelistMap[p.getId().toString()];
}

$.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
        let road = oSettings.aoData[iDataIndex]._aData;
        return currentFilter(road);
    }
);

export function filterRows(idMap) {
    idWhitelistMap = Object.entries(idMap).length === 0 ? 'all' : idMap;
    table.draw();
}

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

function choice_or_empty(value, choices) {
    return value ? choices[value] : '';
}
export function initializeDataTable() {
    const date = new Date();
    table = $("#data-table").DataTable({
        columns: [{
            title: 'Edit', data: null,
            render: r => `<span class='image pencil' onclick='roads.editRoad(${r.id})'></span>`,
            orderable: false
        },
        { 
            title: 'Road Code', data: null,
            render: 'getRoadCode',
            type: "roadCode"
        },
        { 
            title: 'Type', data: null,
            render: r => choice_or_empty(r.getRoadType(), ROAD_TYPE_CHOICES)
        },
        { 
            title: 'Name', data: null,
            render: 'getRoadName'
        },
        { 
            title: 'Status', data: null,
            render: r => choice_or_empty(r.getRoadStatus(), ROAD_STATUS_CHOICES)
        },
        { 
            title: 'Link Code', data: null,
            render: 'getLinkCode'
        },
        { 
            title: 'Link Name', data: null,
            render: 'getLinkName'
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
            title: 'Link Length (Km)', data: null,
            render: r => parseFloat(r.getLinkLength()).toFixed(2)
        },
        { 
            title: 'Surface Type', data: null,
            render: r => choice_or_empty(r.getSurfaceType(), SURFACE_TYPE_CHOICES)
        },
        { 
            title: 'Surface Condition', data: null,
            render: r => choice_or_empty(r.getSurfaceCondition(), SURFACE_CONDITION_CHOICES)
        },
        { 
            title: 'Pavement Class', data: null,
            render: r => choice_or_empty(r.getPavementClass(), PAVEMENT_CLASS_CHOICES)
        },
        { 
            title: 'Administrative Area', data: null,
            render: r => choice_or_empty(parseInt(r.getAdministrativeArea()), ADMINISTRATIVE_AREA_CHOICES)
        },
        { 
            title: 'Carriageway Width (m)', data: null,
            render: r => parseFloat(r.getCarriagewayWidth()).toFixed(2)
        },
        { 
            title: 'Project', data: null,
            render: 'getProject'
        },
        { 
            title: 'Funding Source', data: null,
            render: 'getFundingSource'
        },
        { 
            title: 'Technical Class', data: null,
            render: r => choice_or_empty(r.getTechnicalClass(), TECHNICAL_CLASS_CHOICES)
        },
        { 
            title: 'Maintenance needs', data: null,
            render: r => choice_or_empty(r.getMaintenanceNeed(), MAINTENANCE_NEED_CHOICES)
        },
        { 
            title: 'Traffic Data', data: null,
            render: r => choice_or_empty(r.getTrafficLevel(), TRAFFIC_LEVEL_CHOICES)
        }],
        order: [[1, 'asc']], // default order is ascending by road code
        dom: `<'row'<'col-12'B>> + <'row'<'col-sm-12'tr>> + <'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>`, // https://datatables.net/reference/option/dom#Styling
        buttons: [{
            extend: "excel",
            className: "btn-sm",
            sheetName: "Estrada",
            text: "Export table",
            title: "Estrada_" + date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate(),
        }]
    });

    return table;
}

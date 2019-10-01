import jsZip from "jszip";
import "datatables.net-bs4";
import "datatables.net-buttons-bs4";
import "datatables.net-buttons/js/buttons.html5";
import "datatables.net-buttons/js/buttons.flash";
import $ from "jquery";
import proj4 from "proj4";


let table;
let pendingRows = [];

// INPUT FORMAT: EPSG:32751 WGS 84 / UTM zone 51S
let projection_source = '+proj=utm +zone=51 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs';
// OUTPUT FORMAT: EPSG:4326 WGS 84
let projection_dest = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";

let modf = (number) => {
    // JS implementation of Python math -> modf() function
    // split a number into interger and remainder values
    // returned items have same sign as original number
    return [number%1, Math.trunc(number)];
}

let splitOutDms = (coord) => {
    let split_deg = modf(coord);
    let degrees = Math.trunc(split_deg[1]);
    let interm = modf(split_deg[0] * 60);
    let minutes = Math.abs(Math.trunc(interm[1]));
    let seconds = Math.abs(Math.round((interm[0] * 60 + 0.00001) * 100) / 100);
    return [degrees, minutes, seconds];
}

let toDms = (lat_long) => {
    if (lat_long) {
        let x_dms = splitOutDms(lat_long[0]);
        let y_dms = splitOutDms(lat_long[1]);
        // calculate N/S (lat) & E/W (long)
        let NorS = "N";
        if (y_dms[0] < 0) { NorS = "S"; }
        let EorW = "E";
        if (x_dms[0] < 0) { EorW = "W"; }
        // return formatted DMS string
        return `${Math.abs(y_dms[0])}\u00b0${y_dms[1]}'${y_dms[2]}"${NorS} ${Math.abs(x_dms[0])}\u00b0${x_dms[1]}'${x_dms[2]}"${EorW}`;
    } else {
        return "";
    }
}

let toUtm = (lat_long) => {
    if (lat_long) { return `${lat_long[0].toFixed(5)}, ${lat_long[1].toFixed(5)}`; }
    else { return ""; }
}

// needed for export to excel
window.JSZip = jsZip;

// when the roadManager has new roads, add them to the table
document.addEventListener('estrada.roadManager.roadMetaDataAdded', (data) => {
    // add the roads to a pending array ( in case the table is not initialised early enough )
    pendingRows =  pendingRows.concat(data.detail.roadList);
    if( table ) {
        // if the table is ready add all the pending rows
        table.rows.add(pendingRows).draw();
        pendingRows = [];
    }
});

document.addEventListener('estrada.table.roadMetaDataUpdated', (data) => {
    table.row(`#${data.detail.road.id}`).data(data.detail.road).draw();
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
    const restoreDefaults = document.getElementsByClassName("restore").item(0);
    const columnsDropdown = document.getElementById("columns-dropdown");
    const columns = columnsDropdown.querySelectorAll("[data-column]");

    document.getElementById("select-data").addEventListener("click", () => {
        function clickOutside(e) {
            if (!document.getElementById("select-data").contains(e.target)) {
                columnsDropdown.hidden = true;
            }
        }

        if (columnsDropdown.hidden) document.addEventListener("click", clickOutside);
        else document.removeEventListener("click", clickOutside);

        columnsDropdown.hidden = !columnsDropdown.hidden;
    });

    columnsDropdown.addEventListener("click", (e) => {
        e.stopPropagation();
    });

    columns.forEach((item) => {
        item.addEventListener("click", (e) => {
            e.stopPropagation();
            const element = e.currentTarget;
            const column = table.column(window.canEdit ? parseInt(element.dataset.column) + 1 : element.dataset.column);
            column.visible(!column.visible());
            element.getElementsByClassName("checkbox").item(0).classList.toggle("selected");
        });
    });

    restoreDefaults.addEventListener("click", (e) => {
        e.stopPropagation();
        columns.forEach((item) => {
            const column = table.column(window.canEdit ? parseInt(item.dataset.column) + 1 : item.dataset.column);
            const checkbox = item.getElementsByClassName("checkbox").item(0);

            if (item.dataset.default && !checkbox.classList.contains("selected")) {
                column.visible(true);
                checkbox.classList.add("selected");
            } else if (!item.dataset.default) {
                column.visible(false);
                checkbox.classList.remove("selected");
            }
        });
    });

    initializeDataTable();

    // Append table name onto DataTable generated layout
    document.getElementsByClassName("dt-buttons").item(0).prepend(document.getElementById("table-name"));
});

function initializeDataTable() {
    const date = new Date();
    const columns = [
        {
            title: 'Road Code', data: null,
            render: 'code',
            type: "roadCode"
        },
        {
            title: 'Road Name', data: null,
            render: 'name',
            visible: false,
        },
        {
            title: 'Link Code', data: null,
            render: 'linkCode'
        },
        {
            title: 'Link Name', data: null,
            render: 'linkName',
            visible: false,
        },
        {
            title: 'Link Length (Km)', data: null,
            render: r => parseFloat(r.linkLength).toFixed(2)
        },
        {
            title: 'Link Start Name', data: null,
            render: 'linkStartName'
        },
        {
            title: 'Link Start Chainage (Km)', data: null,
            render: r => parseFloat(r.linkStartChainage).toFixed(2)
        },
        {
            title: 'Link End Name', data: null,
            render: 'linkEndName'
        },
        {
            title: 'Link End Chainage (Km)', data: null,
            render: r => parseFloat(r.linkEndChainage).toFixed(2)
        },
        {
            title: 'Surface Type', data: null,
            render: 'surfaceType'
        },
        {
            title: 'Pavement Class', data: null,
            render: 'pavementClass'
        },
        {
            title: 'Carriageway Width (m)', data: null,
            render: r => parseFloat(r.carriagewayWidth).toFixed(2)
        },
        {
            title: 'Administrative Area', data: null,
            render: 'administrativeArea'
        },
        {
            title: 'Road Type', data: null,
            render: 'type',
            visible: false,
        },
        {
            title: 'Technical Class', data: null,
            render: 'technicalClass',
            visible: false,
        },
        {
            title: 'Funding Source', data: null,
            render: 'fundingSource',
            visible: false,
        },
        {
            title: 'Road Status', data: null,
            render: 'status',
            visible: false,
        },
        {
            title: 'Project', data: null,
            render: 'project',
            visible: false,
        },
        {
            title: 'Surface Condition', data: null,
            render: 'surfaceCondition'
        },
        {
            title: 'Maintenance needs', data: null,
            render: 'maintenanceNeed',
            visible: false,
        },
        {
            title: 'Traffic Data', data: null,
            render: 'trafficLevel',
            visible: false,
        },
        {
            title: 'Start Point (DMS)', data: null,
            render: r => toDms(proj4(projection_source, projection_dest, r.projectionStart.array)),
            visible: false,
        },
        {
            title: 'End Point (DMS)', data: null,
            render: r => toDms(proj4(projection_source, projection_dest, r.projectionEnd.array)),
            visible: false,
        },
        {
            title: 'Start Point (UTM)', data: null,
            render: r => toUtm(proj4(projection_source, projection_dest, r.projectionStart.array)),
            visible: false,
        },
        {
            title: 'End Point (UTM)', data: null,
            render: r => toUtm(proj4(projection_source, projection_dest, r.projectionEnd.array)),
            visible: false,
        },
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
    if (pendingRows.length) {
        // add any rows the road manager has delivered before initialization
        table.rows.add(pendingRows).draw();
        pendingRows = [];
    }

    // Append toggle columns button onto DataTable generated layout
    document.getElementsByClassName("dt-buttons").item(0).append(document.getElementById("select-data"));

    // Append table name onto DataTable generated layout
    document.getElementsByClassName("dt-buttons").item(0).prepend(document.getElementById("table-name"));
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

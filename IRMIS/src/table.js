import jsZip from "jszip";
import "datatables.net-bs4";
import "datatables.net-buttons-bs4";
import "datatables.net-buttons/js/buttons.html5";
import "datatables.net-buttons/js/buttons.flash";
import $ from "jquery";
import { getFieldName } from "./road";

let table;
let pendingRows = [];

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
});

function initializeDataTable() {
    const date = new Date();
    const columns = [
        {
            title: getFieldName('road_code'), data: null,
            render: 'code',
            type: "roadCode"
        },
        {
            title: getFieldName('road_name'), data: null,
            render: 'name',
            visible: false,
        },
        {
            title: getFieldName('link_code'), data: null,
            render: 'linkCode'
        },
        {
            title: 'Link Name', data: null,
            render: 'linkName',
            visible: false,
        },
        {
            title: getFieldName('link_length'), data: null,
            render: r => parseFloat(r.linkLength).toFixed(2)
        },
        {
            title: getFieldName('link_start_name'), data: null,
            render: 'linkStartName'
        },
        {
            title: getFieldName('link_start_chainage'), data: null,
            render: r => parseFloat(r.linkStartChainage).toFixed(2)
        },
        {
            title: getFieldName('link_end_name'), data: null,
            render: 'linkEndName'
        },
        {
            title: getFieldName('link_end_chainage'), data: null,
            render: r => parseFloat(r.linkEndChainage).toFixed(2)
        },
        {
            title: getFieldName('surface_type'), data: null,
            render: 'surfaceType'
        },
        {
            title: getFieldName('pavement_class'), data: null,
            render: 'pavementClass'
        },
        {
            title: getFieldName('carriageway_width'), data: null,
            render: r => parseFloat(r.carriagewayWidth).toFixed(2)
        },
        {
            title: getFieldName('administrative_area'), data: null,
            render: 'administrativeArea'
        },
        {
            title: getFieldName('road_type'), data: null,
            render: 'type',
            visible: false,
        },
        {
            title: getFieldName('technical_class'), data: null,
            render: 'technicalClass',
            visible: false,
        },
        {
            title: getFieldName('funding_source'), data: null,
            render: 'fundingSource',
            visible: false,
        },
        {
            title: getFieldName('road_status'), data: null,
            render: 'status',
            visible: false,
        },
        {
            title: getFieldName('project'), data: null,
            render: 'project',
            visible: false,
        },
        {
            title: getFieldName('surface_condition'), data: null,
            render: 'surfaceCondition'
        },
        {
            title: getFieldName('maintenance_need'), data: null,
            render: 'maintenanceNeed',
            visible: false,
        },
        {
            title: getFieldName('traffic_level'), data: null,
            render: 'trafficLevel',
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

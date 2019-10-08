import "datatables.net-bs4";
import $ from "jquery";

import { applyFilter } from './filter';
import { getFieldName } from "./road";
import { exportCsv } from "./exportCsv";

let table;
let pendingRows = [];

// when the roadManager has new roads, add them to the table
document.addEventListener('estrada.roadManager.roadMetaDataAdded', (data) => {
    const roadList = data.detail.roadList;

    // add the roads to a pending array ( in case the table is not initialised early enough )
    pendingRows = pendingRows.concat(roadList);
    if (table) {
        table.rows.add(pendingRows).draw();
        pendingRows = [];
    }
});

document.addEventListener('estrada.table.roadMetaDataUpdated', (data) => {
    const road = data.detail.road.id;
    table.row(`#${road.id}`).data(road).draw();
});

// when a filter is applied, update the filter id whitelist
document.addEventListener('estrada.filter.applied', (data) => {
    idWhitelistMap = data.detail.idMap;
    table.draw();

    // Handle any table row selection change
    applyTableSelection(table.selectionProcessing);
});

// when the view changes adjust the table rows
document.addEventListener('estrada.sideMenu.viewChanged', (data) => {
    const viewName = data.detail ? data.detail.viewName : null;
    if (viewName && viewName.indexOf('table') !== -1) {
        const tableRows = (viewName === 'table') ? 20 : 10;
        table.page.len(tableRows).draw('page');
    }
});

window.addEventListener("load", () => {
    // Export All - to CSV
    document.getElementById("export").addEventListener("click", exportTable);

    // Select - data columns
    const restoreDefaults = document.getElementsByClassName("restore").item(0);
    const columnsDropdown = document.getElementById("columns-dropdown");
    const columns = columnsDropdown.querySelectorAll("[data-column]");

    document.getElementById("select-data").addEventListener("click", () => {
        function clickOutside(e) {
            if (!document.getElementById("select-data").contains(e.target)) {
                columnsDropdown.hidden = true;
            }
        }

        if (columnsDropdown.hidden) {
            document.addEventListener("click", clickOutside);
        } else {
            document.removeEventListener("click", clickOutside);
        }

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

export const columns = [
    {
        title: getFieldName("road_code"),
        data: "code",
        defaultContent: "",
        type: "roadCode"
    },
    {
        title: getFieldName("road_name"),
        data: "name",
        defaultContent: "",
        visible: false
    },
    {
        title: getFieldName("link_code"),
        data: "linkCode",
        defaultContent: "",
    },
    {
        title: window.gettext("Link Name"),
        data: "linkName",
        defaultContent: "",
        visible: false
    },
    {
        title: getFieldName("link_length"),
        data: "linkLength",
        defaultContent: "",
    },
    {
        title: getFieldName("link_start_name"),
        data: "linkStartName",
        defaultContent: "",
    },
    {
        title: getFieldName("link_start_chainage"),
        data: "linkStartChainage",
        defaultContent: "",
    },
    {
        title: getFieldName("link_end_name"),
        data: "linkEndName",
        defaultContent: "",
    },
    {
        title: getFieldName("link_end_chainage"),
        data: "linkEndChainage",
        defaultContent: "",
    },
    {
        title: getFieldName("surface_type"),
        data: "surfaceType",
        defaultContent: "",
    },
    {
        title: getFieldName("pavement_class"),
        data: "pavementClass",
        defaultContent: "",
    },
    {
        title: getFieldName("carriageway_width"),
        data: "carriagewayWidth",
        defaultContent: "",
    },
    {
        title: getFieldName("administrative_area"),
        data: "administrativeArea",
        defaultContent: "",
    },
    {
        title: getFieldName("road_type"),
        data: "type",
        defaultContent: "",
        visible: false
    },
    {
        title: getFieldName("technical_class"),
        data: "technicalClass",
        defaultContent: "",
        visible: false
    },
    {
        title: getFieldName("funding_source"),
        data: "fundingSource",
        defaultContent: "",
        visible: false
    },
    {
        title: getFieldName("road_status"),
        data: "status",
        defaultContent: "",
        visible: false,
    },
    {
        title: getFieldName("project"),
        data: "project",
        defaultContent: "",
        visible: false,
    },
    {
        title: getFieldName("surface_condition"),
        data: "surfaceCondition",
        defaultContent: "",
    },
    {
        title: getFieldName("maintenance_need"),
        data: "maintenanceNeed",
        defaultContent: "",
        visible: false,
    },
    {
        title: getFieldName("traffic_level"),
        data: "trafficLevel",
        defaultContent: "",
        visible: false,
    },
    {
        title: window.gettext("Start Point (DMS)"),
        data: "startDMS",
        defaultContent: "",
        visible: false
    },
    {
        title: window.gettext("End Point (DMS)"),
        data: "endDMS",
        defaultContent: "",
        visible: false
    },
    {
        title: window.gettext("Start Point (UTM)"),
        data: "startUTM",
        defaultContent: "",
        visible: false
    },
    {
        title: window.gettext("End Point (UTM)"),
        data: "endUTM",
        defaultContent: "",
        visible: false
    },
];

function initializeDataTable() {
    if (window.canEdit) {
        columns.unshift({
            title: "",
            data: null,
            render: r => `<a class="image pencil" href="#edit/${r.getId()}/location_type"></a>`,
            orderable: false,
            className: "edit-col"
        });
    }

    table = $("#data-table").DataTable({
        columns: columns,
        rowId: ".getId()",
        // default order is ascending by: road code, link code, & link start chainage
        order: window.canEdit ? [[1, 'asc'], [3, 'asc'], [7, 'asc']] : [[0, 'asc'], [2, 'asc'], [6, 'asc']],
        dom: `<'row'<'col-12'B>> + <'row'<'col-sm-12'tr>> + <'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>`, // https://datatables.net/reference/option/dom#Styling
        search: {
            regex: true, // Enable escaping of regular expression characters in the search term.
        },
        select: {
            style: "os",
            items: "row",
        }
    });

    table.on('click', 'tbody tr', (e) => {
        const clickedRowId = e.currentTarget.id;
        const clickedRow = $(`tr#${clickedRowId}`);
        
        if (clickedRow.hasClass("selected")) {
            clickedRow.removeClass("selected");

            table.selectionProcessing = undefined;
            // reset to the previously selected filters
            applyFilter();            
        } else {
            table.$('tr.selected').removeClass('selected');
            clickedRow.addClass("selected");

            table.selectionProcessing = clickedRowId;

            applyTableSelection(table.selectionProcessing);
        }
    });

    if (pendingRows.length) {
        // add any rows the road manager has delivered before initialization
        table.rows.add(pendingRows).draw();
        pendingRows = [];
    }
}

function applyTableSelection(rowId) {
    if (!rowId) {
        return;
    }

    const idMap = {}
    idMap[rowId] = true;

    // communicate the filter
    document.dispatchEvent(new CustomEvent("estrada.idFilter.applied", { "detail": { idMap } }));
}

function getTableData() {
    const headers = columns
        .filter((c) => c.title !== "")
        .map((c) => ({ title: c.title, data: c.data }));

    const rowsData = table.rows().data();
    const rows = Object.keys(rowsData).map((rowKey) => {
        const rowFields = [];
        headers.forEach((h) => {
            let data = rowsData[rowKey][h.data];
            // Check if data is null, or implicitly, undefined
            if (data == null) {
                data = "";
            }
            rowFields.push(data);
        })
        return rowFields;
    });

    return { headers: headers.map((h) => h.title), rows: rows };
}


function exportTable() {
    const tableData = getTableData();
    exportCsv(tableData.headers, tableData.rows);
}

// Filter functionality
let idWhitelistMap = null;
let currentFilter = (p) => {
    return idWhitelistMap === null || idWhitelistMap[p.getId().toString()];
}

$.fn.dataTableExt.afnFiltering.push(
    function (oSettings, aData, iDataIndex) {
        let road = oSettings.aoData[iDataIndex]._aData;
        return currentFilter(road);
    }
);

// change the sorting of the road code column to place empty values last
$.extend($.fn.dataTableExt.oSort, {
    "roadCode-asc": function (str1, str2) {
        if (str1 === "") return 1;
        if (str2 === "") return -1;
        return ((str1 < str2) ? -1 : ((str1 > str2) ? 1 : 0));
    },

    "roadCode-desc": function (str1, str2) {
        if (str1 === "") return -1;
        if (str2 === "") return 1;
        return ((str1 < str2) ? 1 : ((str1 > str2) ? -1 : 0));
    }
});

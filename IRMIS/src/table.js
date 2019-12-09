import "datatables.net-bs4";
import $ from "jquery";

import { exportCsv } from "./exportCsv";
import { applyFilter } from './filter';
import { estradaTableColumns, estradaTableEventListeners } from "./mainTableDefinition";
import { carriagewayWidthColumns, numberLanesColumns, pavementClassColumns, rainfallColumns, surfaceConditionColumns, surfaceTypeColumns, technicalClassColumns, terrainClassColumns } from "./segmentsInventoryTableDefinition";

import { datatableTranslations } from "./datatableTranslations";
import { getRoad } from "./roadManager";
import { getRoadReport } from "./reportManager";

let surfaceConditionTable = null;
let surfaceTypeTable = null;
let technicalClassTable = null;
let numberLanesTable = null;
let carriagewayWidthTable = null;
let rainfallTable = null;
let terrainClassTable = null;
let pavementClassTable = null;
let table = null;
let pendingRows = [];

window.addEventListener("load", () => {
    // Event listeners for the table, that are NOT attached to specific elements
    Object.keys(estradaTableEventListeners).forEach((eventKey) => {
        document.addEventListener(eventKey, (event) => estradaTableEventListeners[eventKey](event, table, pendingRows, idWhitelistMap));
    });

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

const segmentInventoryModalTables = {
    surfaceCondition: "inventory-surface-condition-table",
    surfaceType: "inventory-surface-type-table",
    technicalClass: "inventory-technical-class-table",
    numberLanes: "inventory-number-lanes-table",
    carriagewayWidth: "inventory-carriageway-width-table",
    rainfall: "inventory-rainfall-table",
    terrainClass: "inventory-terrain-class-table",
    pavementClass: "inventory-pavement-class-table",
};

function initializeDataTable() {
    if (window.canEdit) {
        estradaTableColumns.unshift({
            title: "",
            data: null,
            render: r => `<a class="image pencil" href="#edit/${r.getId()}/location_type"></a>`,
            orderable: false,
            className: "edit-col"
        });
    }

    table = $("#all-data-table").DataTable({
        columns: estradaTableColumns,
        rowId: ".getId()",
        // default order is ascending by: road code, link code, & link start chainage
        order: window.canEdit ? [[1, 'asc'], [3, 'asc'], [7, 'asc']] : [[0, 'asc'], [2, 'asc'], [6, 'asc']],
        dom: "<'row'<'col-12'B>> + <'row'<'col-sm-12'tr>>", // https://datatables.net/reference/option/dom#Styling
        paging: false,
        language: datatableTranslations,
        search: {
            regex: true, // Enable escaping of regular expression characters in the search term.
        },
        select: {
            style: "os",
            items: "row",
        },
        ajax: function (data, callback, settings) {
            if (pendingRows.length) {
                // add any rows the road manager has delivered before initialization
                callback(pendingRows);
                pendingRows = [];
            }
        }
    });

    table.on("click", "tbody tr td", (e) => {
        const clickedRowId = e.currentTarget.parentNode.id;
        const clickedRow = $(`tr#${clickedRowId}`);

        const cellChildren = e.currentTarget.children;
        const cellChildrenLength = cellChildren.length;
        if (cellChildrenLength > 0) {
            for (let ix = 0; ix < cellChildrenLength; ix++) {
                const cellChild = cellChildren.item(ix);
                if (cellChild.classList.contains("image")) {
                    return;
                }
            }
        }

        if (clickedRow.hasClass("selected")) {
            clickedRow.removeClass("selected");

            table.selectionProcessing = undefined;
            // reset to the previously selected filters
            applyFilter();
        } else {
            table.$("tr.selected").removeClass("selected");
            clickedRow.addClass("selected");

            table.selectionProcessing = clickedRowId;

            applyTableSelection(table.selectionProcessing);
        }
    });

    function setUpModalTable(tableId, columns) {
        return $(`#${tableId}`).DataTable({
            columns: columns,
            rowId: ".getId()",
            dom: "<'row'<'col-sm-12'tr>>", // https://datatables.net/reference/option/dom#Styling
            language: datatableTranslations,
            // This turns off filtering for all tables ( DO NOT SET THIS TO TRUE )
            // dataTables has a bug where the searching / filtering clause passes from one table to another
            // We only want it for the main table
            searching: false,
        });
    }

    surfaceConditionTable = setUpModalTable(segmentInventoryModalTables.surfaceCondition, surfaceConditionColumns);
    surfaceTypeTable = setUpModalTable(segmentInventoryModalTables.surfaceType, surfaceTypeColumns);
    technicalClassTable = setUpModalTable(segmentInventoryModalTables.technicalClass, technicalClassColumns);
    numberLanesTable = setUpModalTable(segmentInventoryModalTables.numberLanes, numberLanesColumns);
    carriagewayWidthTable = setUpModalTable(segmentInventoryModalTables.carriagewayWidth, carriagewayWidthColumns);
    rainfallTable = setUpModalTable(segmentInventoryModalTables.rainfall, rainfallColumns);
    terrainClassTable = setUpModalTable(segmentInventoryModalTables.terrainClass, terrainClassColumns);
    pavementClassTable = setUpModalTable(segmentInventoryModalTables.pavementClass, pavementClassColumns);

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
    const headers = estradaTableColumns
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
let idWhitelistMap = {};
let currentFilter = (p) => {
    return Object.keys(idWhitelistMap).length === 0 || idWhitelistMap[p.getId().toString()];
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

$.fn.dataTable.Api.register('row().show()', function () {
    this.table().row(this.index()).node().scrollIntoView(false);

    // Return row object
    return this;
});

$("#inventory-segments-modal").on("show.bs.modal", function (event) {
    const button = $(event.relatedTarget); // Button that triggered the modal
    const linkCode = button.data("code"); // Extract info from data-* attributes
    const roadId = button.data("id");
    const attr = button.data("attr");
    const modal = $(this);
    let reportDataTableId = undefined;
    let reportTable = undefined;

    $(`#${segmentInventoryModalTables.surfaceCondition}_wrapper`).hide();
    $(`#${segmentInventoryModalTables.surfaceType}_wrapper`).hide();
    $(`#${segmentInventoryModalTables.technicalClass}_wrapper`).hide();
    $(`#${segmentInventoryModalTables.numberLanes}_wrapper`).hide();
    $(`#${segmentInventoryModalTables.carriagewayWidth}_wrapper`).hide();
    $(`#${segmentInventoryModalTables.rainfall}_wrapper`).hide();
    $(`#${segmentInventoryModalTables.terrainClass}_wrapper`).hide();
    $(`#${segmentInventoryModalTables.pavementClass}_wrapper`).hide();

    switch (attr) {
        case "surface_condition":
            reportDataTableId = segmentInventoryModalTables.surfaceCondition;
            modal.find(".modal-title").text(linkCode + " " + gettext("Surface Condition segments"));
            reportTable = surfaceConditionTable;
            break;
        case "surface_type":
            reportDataTableId = segmentInventoryModalTables.surfaceType;
            modal.find(".modal-title").text(linkCode + " " + gettext("Surface Type segments"));
            reportTable = surfaceTypeTable;
            break;
        case "technical_class":
            reportDataTableId = segmentInventoryModalTables.technicalClass;
            modal.find(".modal-title").text(linkCode + " " + gettext("Technical Class segments"));
            reportTable = technicalClassTable;
            break;
        case "number_lanes":
            reportDataTableId = segmentInventoryModalTables.numberLanes;
            modal.find(".modal-title").text(linkCode + " " + gettext("Number of Lanes segments"));
            reportTable = numberLanesTable;
            break;
        case "carriageway_width":
            reportDataTableId = segmentInventoryModalTables.carriagewayWidth;
            modal.find(".modal-title").text(linkCode + " " + gettext("Carriageway Width segments"));
            reportTable = carriagewayWidthTable;
            break;
        case "rainfall":
            reportDataTableId = segmentInventoryModalTables.rainfall;
            modal.find(".modal-title").text(linkCode + " " + gettext("Rainfall segments"));
            reportTable = rainfallTable;
            break;
        case "terrain_class":
            reportDataTableId = segmentInventoryModalTables.terrainClass;
            modal.find(".modal-title").text(linkCode + " " + gettext("Terrain Class segments"));
            reportTable = terrainClassTable;
            break;
        case "pavement_class":
            reportDataTableId = segmentInventoryModalTables.pavementClass;
            modal.find(".modal-title").text(linkCode + " " + gettext("Pavement Class segments"));
            reportTable = pavementClassTable;
            break;
    }
    reportTable.clear(); // remove all rows in the table

    getRoad(roadId).then((roadData) => {
         let filters = {
            primaryattribute: attr,
        };
        if (roadData.getLinkStartChainage() && roadData.getLinkEndChainage()) {
            filters.roadcode = roadData.getRoadCode();
            filters.chainagestart = roadData.getLinkStartChainage();
            filters.chainageend = roadData.getLinkEndChainage();
        } else {
            filters.roadid = roadData.id;
        }
        getRoadReport(filters).then((reportData) => {
            reportTable.clear(); // remove all rows in the table - again
            if (reportData && reportDataTableId) {
                const attributes = reportData.attributeTable(attr, true);
                if (attributes.length) {
                    reportTable.rows.add(attributes);
                }
            }

        }).finally(() => {
            reportTable.draw();

            $(`#${reportDataTableId}_wrapper`).show();
        });
    });
});

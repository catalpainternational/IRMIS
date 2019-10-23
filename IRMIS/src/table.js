import "datatables.net-bs4";
import $ from "jquery";

import { applyFilter } from './filter';
import { getFieldName } from "./road";
import { exportCsv } from "./exportCsv";
import { estradaTableColumns, estradaTableEventListeners } from "./mainTableDefinition";
import { datatableTranslations } from "./datatableTranslations";

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

function initializeDataTable() {
    if (window.canEdit) {
        estradaTableColumns.unshift({
            title: "",
            data: null,
            render: r => '<a class="image pencil" href="#edit/' + r.getId() + '/location_type"></a>',
            orderable: false,
            className: "edit-col"
        });
    }

    table = $("#data-table").DataTable({
        columns: estradaTableColumns,
        rowId: ".getId()",
        // default order is ascending by: road code, link code, & link start chainage
        order: window.canEdit ? [[1, 'asc'], [3, 'asc'], [7, 'asc']] : [[0, 'asc'], [2, 'asc'], [6, 'asc']],
        dom: "<'row'<'col-12'B>> + <'row'<'col-sm-12'tr>> + <'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        language: datatableTranslations,
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

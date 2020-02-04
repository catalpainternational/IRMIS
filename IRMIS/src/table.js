import "datatables.net-bs4";
import $ from "jquery";
import * as riot from "riot";

import { exportCsv } from "./exportCsv";
import { applyFilter } from "./filter";
import { assetTypeName } from "./side_menu";
import { estradaTableColumns, estradaRoadTableEventListeners, estradaStructureTableEventListeners, structuresTableColumns } from "./mainTableDefinition";
import {
    carriagewayWidthColumns,
    numberLanesColumns,
    pavementClassColumns,
    rainfallColumns,
    structureConditionColumns,
    structureConditionDescriptionColumns,
    structurePhotosColumns,
    surfaceConditionColumns,
    surfaceTypeColumns,
    technicalClassColumns,
    terrainClassColumns,
} from "./segmentsInventoryTableDefinition";

import { datatableTranslations } from "./datatableTranslations";
import { getRoad, roads } from "./roadManager";
import { getRoadReport as getAssetReport } from "./reportManager";
import {getRoadSurveys as getAssetSurveys} from "./surveyManager";
import { getStructure, structures } from "./structureManager";
import { dispatch } from "./assets/utilities";
import {Survey} from "../protobuf/survey_pb";

let roadsTable = null;
let structuresTable = null;

let pendingRoads = [];
let pendingStructures = [];

window.addEventListener("load", () => {
    // Initialize both roads and structures tables
    initializeDataTable();
});

const attributeModalMapping = {
    surface_condition: {
        columns: surfaceConditionColumns,
        reportDataTableId: "inventory-surface-condition-table",
        reportTable: null,
        title: gettext("Surface Condition segments"),
    },
    surface_type: {
        columns: surfaceTypeColumns,
        reportDataTableId: "inventory-surface-type-table",
        reportTable: null,
        title: gettext("Surface Type segments"),
    },
    technical_class: {
        columns: technicalClassColumns,
        reportDataTableId: "inventory-technical-class-table",
        reportTable: null,
        title: gettext("Technical Class segments"),
    },
    number_lanes: {
        columns: numberLanesColumns,
        reportDataTableId: "inventory-number-lanes-table",
        reportTable: null,
        title: gettext("Number of Lanes segments"),
    },
    carriageway_width: {
        columns: carriagewayWidthColumns,
        reportDataTableId: "inventory-carriageway-width-table",
        reportTable: null,
        title: gettext("Carriageway Width segments"),
    },
    rainfall: {
        columns: rainfallColumns,
        reportDataTableId: "inventory-rainfall-table",
        reportTable: null,
        title: gettext("Rainfall segments"),
    },
    terrain_class: {
        columns: terrainClassColumns,
        reportDataTableId: "inventory-terrain-class-table",
        reportTable: null,
        title: gettext("Terrain Class segments"),
    },
    pavement_class: {
        columns: pavementClassColumns,
        reportDataTableId: "inventory-pavement-class-table",
        reportTable: null,
        title: gettext("Pavement Class segments"),
    },
    structure_condition: {
        columns: structureConditionColumns,
        reportDataTableId: "inventory-structure-condition-table",
        reportTable: null,
        title: gettext("Structure Condition details"),
    },
    structure_condition_description: {
        columns: structureConditionDescriptionColumns,
        reportDataTableId: "inventory-structure-condition-description-table",
        reportTable: null,
        title: gettext("Structure Condition Description details"),
    },
    structure_photos: {
        columns: structurePhotosColumns,
        reportDataTableId: "inventory-structure-photos-table",
        reportTable: null,
        title: gettext("Inventory Photos details"),
    },
}

function initializeDataTable() {
    if (window.canEdit) {
        estradaTableColumns.unshift({
            title: "",
            data: null,
            render: r => `<a class="image pencil" href="#edit/road/${r.getId()}/location_type"></a>`,
            orderable: false,
            className: "edit-col"
        });
        structuresTableColumns.unshift({
            title: "",
            data: null,
            render: r => `<a class="image pencil" href="#edit/${r.getId().substring(0, 4)}/${r.getId().substring(5)}/structure_type"></a>`,
            orderable: false,
            className: "edit-col"
        });
    }

    roadsTable = $("#all-data-table").DataTable({
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
        },
        ajax: function (data, callback, settings) {
            if (pendingRoads.length) {
                // add any rows the road manager has delivered before initialization
                callback(pendingRoads);
                pendingRoads = [];
            }
        }
    });

    structuresTable = $("#structures-data-table").DataTable({
        columns: structuresTableColumns,
        rowId: ".getId()",
        // default order is ascending by: structure code
        order: window.canEdit ? [[2, 'asc']] : [[1, 'asc']],
        dom: "<'row'<'col-12'B>> + <'row'<'col-sm-12'tr>> + <'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        language: datatableTranslations,
        search: {
            regex: true, // Enable escaping of regular expression characters in the search term.
        },
        select: {
            style: "os",
            items: "row",
        },
        ajax: function (data, callback, settings) {
            if (pendingStructures.length) {
                // add any rows the structure manager has delivered before initialization
                callback(pendingStructures);
                pendingStructures = [];
            }
        }

    });

    setupTableEventHandlers();

    function setUpModalTable(tableId, columns) {
        return $(`#${tableId}`).DataTable({
            columns: columns,
            rowId: ".getId()",
            dom: "<'row'<'col-sm-12'tr>>", // https://datatables.net/reference/option/dom#Styling
            language: datatableTranslations,
            // This turns off filtering for all tables ( DO NOT SET THIS TO TRUE )
            // dataTables has a bug where the searching / filtering clause passes from one table to another
            // We only want it for the main tables
            searching: false,
        });
    }

    Object.keys(attributeModalMapping).forEach((attribute) => {
        const attrMapping = attributeModalMapping[attribute];
        attrMapping.reportTable = setUpModalTable(attrMapping.reportDataTableId, attrMapping.columns);
    });

    if (pendingRoads.length) {
        // add any rows the road manager has delivered before initialization
        if (assetTypeName === "roads") {
            roadsTable.rows.add(pendingRoads).draw();

            pendingRoads = [];
        }
    }

    if (pendingStructures.length) {
        // add any rows the structure manager has delivered before initialization
        if (assetTypeName !== "roads") {
            structuresTable.rows.add(pendingStructures).draw();

            pendingStructures = [];
        }
    }
}

function setupTableEventHandlers() {
    // Event listeners for the roadsTable and structuresTable, that are NOT attached to specific elements
    Object.keys(estradaRoadTableEventListeners).forEach((eventKey) => {
        document.addEventListener(eventKey, (event) => estradaRoadTableEventListeners[eventKey](event, roadsTable, pendingRoads, idWhitelistMap));
    });
    Object.keys(estradaStructureTableEventListeners).forEach((eventKey) => {
        document.addEventListener(eventKey, (event) => estradaStructureTableEventListeners[eventKey](event, structuresTable, pendingStructures, idWhitelistMap));
    });

    // Export All - to CSV
    document.getElementById("export-road").addEventListener("click", exportRoadsTable);
    document.getElementById("export-structure").addEventListener("click", exportStructuresTable);

    // Setup column selection and column click handlers
    setupColumnEventHandlers("roads");
    setupColumnEventHandlers("structures");

    function setupColumnEventHandlers(mainTableType = "roads") {
        const selectId = (mainTableType === "roads")
            ? "select-road-data"
            : "select-structure-data";

        const columnsDropdown = (mainTableType === "roads")
            ? document.getElementById("road-columns-dropdown")
            : document.getElementById("structure-columns-dropdown");

        const columns = columnsDropdown.querySelectorAll("[data-column]");

        const mainTable = (mainTableType === "roads")
            ? roadsTable
            : structuresTable;

        const restoreColumnDefaults = (mainTableType === "roads")
            ? document.getElementsByClassName("restore-road").item(0)
            : document.getElementsByClassName("restore-structure").item(0);

        columnSelectionHandler(selectId, columnsDropdown);
        columnClickHandler(columns, mainTable);
        restoreDefaultColumnSelectionHandler(restoreColumnDefaults, columns, mainTable);
    }

    function columnSelectionHandler(selectId, columnsDropdown) {
        document.getElementById(selectId).addEventListener("click", () => {
            function clickOutside(e) {
                if (!document.getElementById(selectId).contains(e.target)) {
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
    }

    function columnClickHandler(columns, mainTable) {
        columns.forEach((item) => {
            item.addEventListener("click", (e) => {
                e.stopPropagation();
                const element = e.currentTarget;
                const column = mainTable.column(window.canEdit ? parseInt(element.dataset.column) + 1 : element.dataset.column);
                column.visible(!column.visible());
                element.getElementsByClassName("checkbox").item(0).classList.toggle("selected");
            });
        });
    }

    function restoreDefaultColumnSelectionHandler(restoreColumnDefaults, columns, mainTable) {
        restoreColumnDefaults.addEventListener("click", (e) => {
            e.stopPropagation();
            columns.forEach((item) => {
                const column = mainTable.column(window.canEdit ? parseInt(item.dataset.column) + 1 : item.dataset.column);
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
    }

    roadsTable.on("click", "tbody tr td", (e) => { handleCellClick(e, "roads"); });
    structuresTable.on("click", "tbody tr td", (e) => { handleCellClick(e, "structures"); });

    function handleCellClick(e, mainTableType = "roads") {
        const mainTable = (mainTableType === "roads")
            ? roadsTable
            : structuresTable;

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

            mainTable.selectionProcessing = undefined;
            // reset to the previously selected filters
            applyFilter();
        } else {
            mainTable.$("tr.selected").removeClass("selected");
            clickedRow.addClass("selected");

            mainTable.selectionProcessing = clickedRowId;

            applyTableSelection(mainTable.selectionProcessing);
        }
    }
}

function applyTableSelection(rowId) {
    if (!rowId) {
        return;
    }

    const idMap = {}
    idMap[rowId] = true;

    // communicate the filter
    dispatch("estrada.idFilter.applied", { detail: { idMap } });
}

/**
 * Get correct data for the popup on the map
 * @param {number} id
 * @param {string} featureType
 * @return [{label: string, value: string}]
 */
export function GetDataForMapPopup(id, featureType) {
    const assetType = ["bridge", "culvert"].includes(featureType) ? "structures" : "roads";
    if (assetType !== assetTypeName) {
        return [{ label: window.gettext("Asset Type"), value: featureType }];
    }
    const asset = assetTypeName === "roads" ? roads[id] : structures[id];

    if (!asset) {
        return [{ label: window.gettext("Loading"), value: "" }];
    }

    const code = assetTypeName === "roads" ? asset.getRoadCode() : asset.getStructureCode();
    const name = assetTypeName === "roads" ? asset.getRoadName() : asset.getStructureName();

    const mapPopupData = [];
    if (code) {
        mapPopupData.push({ label: window.gettext("Code"), value: code });
    }
    if (name) {
        mapPopupData.push({ label: window.gettext("Name"), value: name });
    }

    return mapPopupData;
}

function getTableData(mainTableType = "roads") {
    const mainTableColumns = (mainTableType === "roads")
        ? estradaTableColumns
        : structuresTableColumns;
    const mainTable = (mainTableType === "roads")
        ? roadsTable
        : structuresTable;

    const headers = mainTableColumns
        .filter((c) => c.title !== "")
        .map((c) => ({ title: c.title, data: c.data }));

    const rowsData = mainTable.rows().data();
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

function exportRoadsTable() {
    const tableData = getTableData("roads");
    exportCsv(tableData.headers, tableData.rows);
}

function exportStructuresTable() {
    const structuresData = getTableData("structures");
    exportCsv(structuresData.headers, structuresData.rows);
}

// Filter functionality
let idWhitelistMap = {};
let currentFilter = (p) => {
    return Object.keys(idWhitelistMap).length === 0 || idWhitelistMap[p.getId().toString()];
}

$.fn.dataTableExt.afnFiltering.push(
    function (oSettings, aData, iDataIndex) {
        let asset = oSettings.aoData[iDataIndex]._aData;
        return currentFilter(asset);
    }
);

// change the sorting of the road/structure code columns to place empty values last
function ascSort(str1, str2) {
    if (str1 === "") return 1;
    if (str2 === "") return -1;
    return ((str1 < str2) ? -1 : ((str1 > str2) ? 1 : 0));
}

function descSort(str1, str2) {
    if (str1 === "") return -1;
    if (str2 === "") return 1;
    return ((str1 < str2) ? 1 : ((str1 > str2) ? -1 : 0));
}

$.extend($.fn.dataTableExt.oSort, {
    "roadCode-asc": ascSort,
    "roadCode-desc": descSort,
    "structureCode-asc": ascSort,
    "structureCode-desc": descSort
});

$.fn.dataTable.Api.register('row().show()', function () {
    const page = this.table().page;
    const tableRows = this.table().rows({ order:"current", page:"all", search: "applied" });
    const rowIndex = this.index();
    const rowPosition = tableRows[0].indexOf( rowIndex );

    if( rowPosition >= page.info().start && rowPosition < page.info().end ) {
        // On the correct page - return the row
        return this;
    }

    const newPageNumber = Math.floor(rowPosition / page.len());
    // Change page
    page(newPageNumber);

    // Return row object
    return this;
});

$("#inventory-segments-modal").on("show.bs.modal", function (event) {
    // Hide them all segment tables first
    Object.keys(attributeModalMapping).forEach((attribute) => {
        const repTable = attributeModalMapping[attribute].reportTable;
        if (repTable) {
            const repTableId = attributeModalMapping[attribute].reportDataTableId;
            $(`#${repTableId}_wrapper`).hide();
        }
    });
    // Hide special traffic data div
    document.dispatchEvent(new CustomEvent("inventory-traffic-level-table.hideData"));

    const button = $(event.relatedTarget); // Button that triggered the modal
    const assetCode = button.data("code"); // Extract info from data-* attributes
    const assetId = button.data("id");
    const attr = button.data("attr");
    const modal = $(this);

    if (attr === "traffic_level") {
        modal.find(".modal-title").text(`${assetCode} Traffic Data`);
        let latestSurvey = false;
        getAssetSurveys(assetId, "trafficType")
            .then((surveyData) => {
                // Get the latest Survey (AADT or Forecast)
                latestSurvey = surveyData.filter((s) => {
                    return s.values.trafficType === "Forecast" || s.values.trafficType === "AADT";
                }).sort((a, b) => {
                    a = new Date(a.dateSurveyed);
                    b = new Date(b.dateSurveyed);
                    return (a > b) ? -1 : (a < b) ? 1 : 0;
                })[0] || false;
            }).finally(() => {
                // update the traffic details inventory modal tag with current data
                document.dispatchEvent(new CustomEvent("inventory-traffic-level-table.updateTrafficData", {detail: {currentRowData: latestSurvey }}));
            });
    } else {
        const reportDataTableId = attributeModalMapping[attr].reportDataTableId;
        const reportTable = attributeModalMapping[attr].reportTable;
        modal.find(".modal-title").text(`${assetCode} ${attributeModalMapping[attr].title}`);
        reportTable.clear(); // remove all rows in the table

        const getAsset = assetTypeName === "roads" ? getRoad : getStructure;
        const getAssetFilters = (assetData) => {
            let filters = {
                primaryattribute: attr,
            };

            if (assetTypeName === "roads") {
                if (assetData.getLinkStartChainage() && assetData.getLinkEndChainage()) {
                    filters.road_code = assetData.getRoadCode();
                    filters.chainagestart = assetData.getLinkStartChainage();
                    filters.chainageend = assetData.getLinkEndChainage();
                } else {
                    filters.road_id = assetData.id;
                }
            } else {
                if (assetData.getChainage()) {
                    filters.structure_code = assetData.getStructureCode();
                    filters.chainage = assetData.getChainage();
                } else {
                    filters.structure_id = assetData.id;
                }
            }

            return filters;
        };

        getAsset(assetId).then((assetData) => {
            const filters = getAssetFilters(assetData)
            getAssetReport(filters)
                .then((reportData) => {
                    reportTable.clear(); // remove all rows in the table - again
                    if (reportData && reportDataTableId) {
                        const attributes = reportData.attributes(attr, null, false, true);
                        if (attributes.attributeEntries.length) {
                            reportTable.rows.add(attributes.attributeEntries);
                        }
                    }
                })
                .finally(() => {
                    reportTable.draw();
                    $(`#${reportDataTableId}_wrapper`).show();
                });
        });
    }
});

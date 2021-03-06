import "datatables.net-bs4";
import $ from "jquery";

import { dispatch } from "./assets/utilities";

import { exportCsv } from "exportCsv";
import { currentFilter } from "./side_menu";
import { estradaTableColumns, estradaRoadTableEventListeners, estradaStructureTableEventListeners, structuresTableColumns } from "./mainTableDefinition";
import {
    carriagewayWidthColumns,
    numberLanesColumns,
    pavementClassColumns,
    rainfallColumns,
    surfaceConditionColumns,
    surfaceTypeColumns,
    technicalClassColumns,
    terrainClassColumns,
    totalWidthColumns,
} from "./segmentsInventoryTableDefinition";
import { datatableTranslations } from "./datatableTranslations";

import { getRoad, roads } from "./roadManager";
import { getStructure, structures } from "./structureManager";
import { getMedias } from "./mediaManager";
import { getAssetReport } from "./reportManager";
import { getAssetSurveys, getStructureSurveys } from "./surveyManager";

let roadsTable = null;
let structuresTable = null;

let pendingRoads = [];
let pendingStructures = [];

window.addEventListener("load", () => {
    // Initialize both roads and structures tables
    initializeDataTable();
});

const attributeModalMapping = {
    asset_condition: {
        columns: surfaceConditionColumns,
        reportDataTableId: "inventory-asset-condition-table",
        reportTable: null,
        title: gettext("Asset Condition segments"),
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
    total_width: {
        columns: totalWidthColumns,
        reportDataTableId: "inventory-total-width-table",
        reportTable: null,
        title: gettext("Total Width segments"),
    },
    rainfall_maximum: {
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
}

function initializeDataTable() {
    if (window.canEdit) {
        estradaTableColumns.unshift({
            title: "",
            data: null,
            render: r => editButtonTemplate(r, "location_type"),
            orderable: false,
            className: "edit-col"
        });
        structuresTableColumns.unshift({
            title: "",
            data: null,
            render: r => editButtonTemplate(r, "structure_type"),
            orderable: false,
            className: "edit-col"
        });
    }

    roadsTable = $("#all-data-table").DataTable({
        columns: estradaTableColumns,
        autoWidth: false,
        rowId: ".id",
        // default order is ascending by: road code, link start chainage & link code 
        order: window.canEdit ? [[1, 'asc'], [11, 'asc'], [6, 'asc']] : [[0, 'asc'], [10, 'asc'], [5, 'asc']],
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
        rowId: ".id",
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
        return $("#" + tableId).DataTable({
            columns: columns,
            rowId: ".id",
            dom: "<'row'<'col-sm-12'tr>>", // https://datatables.net/reference/option/dom#Styling
            language: datatableTranslations,
            // Do NOT turn on scrolling for these modal tables, it screws up the headers in unfixable ways
            // scrollY: "" - defines vertical scrolling as off
            scrollY: "",
            paging: false,
            // This turns off filtering for all tables ( DO NOT SET THIS TO TRUE )
            // dataTables has a bug where the searching / filtering clause passes from one table to another
            // We only want it for the main tables
            searching: false,
            ordering: false,
        });
    }

    Object.keys(attributeModalMapping).forEach((attribute) => {
        const attrMapping = attributeModalMapping[attribute];
        attrMapping.reportTable = setUpModalTable(attrMapping.reportDataTableId, attrMapping.columns);
    });

    if (pendingRoads.length) {
        // add any rows the road manager has delivered before initialization
        if (currentFilter.assetType === "ROAD") {
            roadsTable.rows.add(pendingRoads).draw();

            pendingRoads = [];
        }
    }

    if (pendingStructures.length) {
        // add any rows the structure manager has delivered before initialization
        if (currentFilter.assetType !== "ROAD") {
            structuresTable.rows.add(pendingStructures).draw();

            pendingStructures = [];
        }
    }
}

function editButtonTemplate(asset, firstPage) {
    return '<a class="image pencil" href="#edit/' + asset.assetType + '/' + asset.assetId + '/' + firstPage + '"></a>';
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
    setupColumnEventHandlers("ROAD");
    setupColumnEventHandlers("STRC");

    function setupColumnEventHandlers(mainTableType = "ROAD") {
        const selectId = (mainTableType === "ROAD")
            ? "select-road-data"
            : "select-structure-data";

        const columnsDropdown = (mainTableType === "ROAD")
            ? document.getElementById("road-columns-dropdown")
            : document.getElementById("structure-columns-dropdown");

        const columns = columnsDropdown.querySelectorAll("[data-column]");

        const mainTable = (mainTableType === "ROAD")
            ? roadsTable
            : structuresTable;

        const restoreColumnDefaults = (mainTableType === "ROAD")
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

    roadsTable.on("click", "tbody tr td", (e) => { handleCellClick(e, "ROAD"); });
    structuresTable.on("click", "tbody tr td", (e) => { handleCellClick(e, "STRC"); });

    function handleCellClick(e, mainTableType = "ROAD") {
        const mainTable = (mainTableType === "ROAD")
            ? roadsTable
            : structuresTable;

        const clickedRowId = e.currentTarget.parentNode.id;
        const clickedRow = $("tr#" + clickedRowId);

        const cellChildren = e.currentTarget.children;
        const cellChildrenLength = cellChildren.length;

        if (cellChildrenLength > 0) return;

        if (clickedRow.hasClass("selected")) {
            clickedRow.removeClass("selected");

            mainTable.selectionProcessing = undefined;
            // reset to the previously selected filters
            currentFilter.apply();
        } else {
            mainTable.$("tr.selected").removeClass("selected");
            clickedRow.addClass("selected");

            mainTable.selectionProcessing = clickedRowId;

            applyTableSelectionToMap(mainTable.selectionProcessing);
        }
    }
}

function applyTableSelectionToMap(rowId) {
    if (!rowId) {
        return;
    }

    const idMap = {}
    idMap[rowId] = true;

    // communicate the filter
    const eventName = "estrada.map.idFilter.applied";
    dispatch(eventName, { detail: { idMap: idMap, adjustZoomLevel: true } });
}

/**
 * Get correct data for the popup on the map
 * @param {number} id
 * @param {string} featureType
 * @return [{label: string, value: string}]
 */
export function GetDataForMapPopup(id, featureType) {
    const assetType = ["BRDG", "CULV", "DRFT", "bridge", "culvert", "drift"].includes(featureType) ? "STRC" : "ROAD";
    if (assetType !== currentFilter.assetType) {
        return [{ label: window.gettext("Asset Type"), value: featureType }];
    }
    const asset = currentFilter.assetType === "ROAD" ? roads[id] : structures[id];

    if (!asset) {
        return [{ label: window.gettext("Loading"), value: "" }];
    }

    const mapPopupData = [];
    if (asset.code) {
        mapPopupData.push({ label: window.gettext("Code"), value: asset.code });
    }
    if (asset.name) {
        mapPopupData.push({ label: window.gettext("Name"), value: asset.name });
    }

    return mapPopupData;
}

function getTableData(mainTableType = "ROAD") {
    const mainTableColumns = (mainTableType === "ROAD")
        ? estradaTableColumns
        : structuresTableColumns;
    const mainTable = (mainTableType === "ROAD")
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
    const tableData = getTableData("ROAD");
    exportCsv(tableData.headers, tableData.rows, window.gettext("Roads"));
}

function exportStructuresTable() {
    const structuresData = getTableData("STRC");
    exportCsv(structuresData.headers, structuresData.rows, window.gettext("Structures"));
}

// Filter functionality
let idWhitelistMap = {};
let currentIdFilter = (p) => {
    return Object.keys(idWhitelistMap).length === 0 || idWhitelistMap[p.id];
}

$.fn.dataTableExt.afnFiltering.push(
    function (oSettings, aData, iDataIndex) {
        let asset = oSettings.aoData[iDataIndex]._aData;
        return currentIdFilter(asset);
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
    const tableRows = this.table().rows({ order: "current", page: "all", search: "applied" });
    const rowIndex = this.index();
    const rowPosition = tableRows[0].indexOf(rowIndex);

    if (rowPosition >= page.info().start && rowPosition < page.info().end) {
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
    // Hide all segment tables first
    Object.keys(attributeModalMapping).forEach((attribute) => {
        const repTable = attributeModalMapping[attribute].reportTable;
        if (repTable) {
            const repTableId = attributeModalMapping[attribute].reportDataTableId;
            $("#" + repTableId + "_wrapper").hide();
        }
    });
    // Hide special traffic data div & medias details box div
    document.dispatchEvent(new CustomEvent("inventory-traffic-level-table.hideData"));
    document.dispatchEvent(new CustomEvent("media-details-modal.hideData"));

    const button = $(event.relatedTarget); // Button that triggered the modal
    const assetCode = button.data("code"); // Extract info from data-* attributes
    const assetId = button.data("id");
    const attr = button.data("attr");
    const assetType = button.data("type");
    const modal = $(this);

    if (attr === "traffic_level") {
        modal.find(".modal-title").text(assetCode + " Traffic Data");
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
                document.dispatchEvent(new CustomEvent("inventory-traffic-level-table.updateTrafficData", { detail: { currentRowData: latestSurvey } }));
            });
    } else if (attr === "structure_condition_media") {
        modal.find(".modal-title").text(assetCode + " Condition Media");
        let latestSurvey = false;
        let media = undefined;
        getStructureSurveys(assetId, "asset_condition")
            .then((surveyData) => {
                latestSurvey = surveyData.sort((a, b) => {
                    a = new Date(a.dateSurveyed);
                    b = new Date(b.dateSurveyed);
                    return (a > b) ? -1 : (a < b) ? 1 : 0;
                })[0] || false;
                if (latestSurvey) {
                    getMedias("SURV-" + latestSurvey.id)
                        .then((mediaData) => {
                            media = mediaData;
                        }).finally(() => {
                            // update the inventory modal tag with current data
                            document.dispatchEvent(new CustomEvent("media-details-modal.updateModalData", { detail: { currentMediaData: media } }));
                        });
                }
            }).finally(() => {
                // update the inventory modal tag with current data
                document.dispatchEvent(new CustomEvent("media-details-modal.updateModalData", { detail: { currentMediaData: media } }));
            });
    } else if (attr == "inventory_media") {
        modal.find(".modal-title").text(assetCode + " Inventory Photos and Videos");
        let media = undefined;
        let globalId = (assetType == "ROAD") ? assetType + "-" + assetId : assetId;
        getMedias(globalId)
            .then((mediaData) => {
                media = mediaData;
            }).finally(() => {
                // update the inventory modal tag with current data
                document.dispatchEvent(new CustomEvent("media-details-modal.updateModalData", { detail: { currentMediaData: media } }));
            });
    } else {
        const reportDataTableId = attributeModalMapping[attr].reportDataTableId;
        const reportTable = attributeModalMapping[attr].reportTable;
        modal.find(".modal-title").text(assetCode + " " + attributeModalMapping[attr].title);
        reportTable.clear(); // remove all rows in the table

        const getAsset = currentFilter.assetType === "ROAD" ? getRoad : getStructure;
        const getAssetFilters = (assetData) => {
            let filters = {
                reportassettype: [currentFilter.assetType],
                primaryattribute: attr,
            };

            if (currentFilter.assetType === "ROAD") {
                if (assetData.linkStartChainage && assetData.linkEndChainage) {
                    // Both the generic 'asset' value and the specific 'road' value are set
                    // This ensure correct interpretation of the filters
                    // the 'road' value will be 'discarded' during report processing
                    filters.asset_code = assetData.roadCode
                    filters.road_code = assetData.roadCode;
                    // Use the protobuf object get members here, because we want chainage unformatted
                    filters.chainagestart = assetData.getLinkStartChainage();
                    filters.chainageend = assetData.getLinkEndChainage();
                } else {
                    filters.asset_id = assetData.id;
                    filters.road_id = assetData.id;
                }
            } else {
                if (assetData.chainage) {
                    // Both the generic 'asset' value and the specific 'road' value are set
                    // This ensure correct interpretation of the filters
                    // the 'road' value will be 'retained' during report processing
                    filters.asset_code = assetData.structureCode;
                    filters.road_code = assetData.roadCode;
                    filters.chainage = assetData.getChainage();
                } else {
                    filters.asset_id = assetData.id;
                    filters.road_id = assetData.roadId;
                }
            }

            return filters;
        };

        getAsset(assetId).then((assetData) => {
            const filters = getAssetFilters(assetData);
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
                    $("#" + reportDataTableId + "_wrapper").show();
                });
        });
    }
});

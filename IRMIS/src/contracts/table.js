import "datatables.net-bs4";
import $ from "jquery";

import { datatableTranslations } from "../datatableTranslations";
import { exportCsv } from "exportCsv";

window.addEventListener("load", () => {
    const projectsListTable = $("#project-list-table");
    const tendersListTable = $("#tender-list-table");
    const contractsListTable = $("#contract-list-table");
    const companiesListTable = $("#company-list-table");

    if (projectsListTable.length) initializeProjectsListTable(projectsListTable);
    if (tendersListTable.length) initializeTendersListTable(tendersListTable);
    if (contractsListTable.length) initializeContractsListTable(contractsListTable);
    if (companiesListTable.length) initializeCompaniesListTable(companiesListTable);

    initializeListTable($("#project-document-list-table"), [{ orderable: false, targets: [0, 1] }], [[2, 'asc']]);
    initializeListTable($("#project-document-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#tender-document-list-table"), [{ orderable: false, targets: [0, 1] }], [[2, 'asc']]);
    initializeListTable($("#tender-document-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#contract-inspection-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
    initializeListTable($("#contract-inspection-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#contract-payment-list-table"), [{ orderable: false, targets: 0 }, { targets: 2, type: "sort-currency" }], [[1, 'asc']]);
    initializeListTable($("#contract-payment-view-list-table"), [{ targets: 1, type: "sort-currency" }], [[0, 'asc']]);
    initializeListTable($("#contract-social-safeguard-list-table"), [{ orderable: false, targets: 0 }, { targets: [2, 3, 4, 5], type: "sort-integer" }], [[1, 'asc']]);
    initializeListTable($("#contract-social-safeguard-view-list-table"), [{ targets: [1, 2, 3, 4], type: "sort-integer" }], [[0, 'asc']]);
    initializeListTable($("#contract-document-list-table"), [{ orderable: false, targets: [0, 1] }], [[2, 'asc']]);
    initializeListTable($("#contract-document-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#company-document-list-table"), [{ orderable: false, targets: [0, 1] }], [[2, 'asc']]);
    initializeListTable($("#company-document-view-list-table"), [], [[0, 'asc']]);

    initializePrintableTable($("#project-document-print-list-table"), []);
    initializePrintableTable($("#tender-document-print-list-table"), []);
    initializePrintableTable($("#contract-inspection-print-list-table"), []);
    initializePrintableTable($("#contract-payment-print-list-table"), []);
    initializePrintableTable($("#contract-social-safeguard-print-list-table"), []);
    initializePrintableTable($("#contract-document-print-list-table"), []);
    initializePrintableTable($("#company-document-print-list-table"), []);
});

function initializeProjectsListTable(table) {
    let columnDefs;
    let order;

    // Define hidden columns
    const project_code = -4;
    const project_assets = -3;
    const project_assets_class = -2;
    const project_municipality = -1;
    const hidden_columns = [
        project_code,
        // project_assets, 
        project_assets_class, 
        project_municipality,
    ];

    if (window.canChangeProjects) {
        order = [[1, 'asc']];
        columnDefs = [
            { orderable: false, targets: 0 },
            { visible: false, targets: hidden_columns },
            { targets: 5, type: "sort-currency" }
        ];
    } else {
        order = [[0, 'asc']];
        columnDefs = [
            { visible: false, targets: hidden_columns },
            { targets: 4, type: "sort-currency" }
        ];
    }

    const dataTable = table.DataTable({
        dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        columnDefs: columnDefs,
        order: order,
        language: datatableTranslations,
    });

    // Export projects table as CSV
    document.getElementById("export-csv").addEventListener("click", () => {
        const headers = [
            window.gettext("Project Name"),
            window.gettext("Status"),
            window.gettext("Program"),
            window.gettext("Type of Work"),
            window.gettext("Estimated Budget"),
            window.gettext("Funding Source")
        ];
        exportTable(dataTable, headers, 7, [1], window.gettext("Projects"));
    });

    // Search box
    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Asset Code, Project Code or Project Name");

    // Select Filters
    setupSelectFilter(dataTable, "project_status_select2", window.gettext("Project status"), textFilter, 2);
    setupSelectFilter(dataTable, "project_type_of_work_select2", window.gettext("Type of work"), textFilter, 4);
    setupSelectFilter(dataTable, "asset_class_select2", window.gettext("Asset class"), multipleTextFilter, 9);
    setupSelectFilter(dataTable, "municipality_select2", window.gettext("Municipality"), multipleTextFilter, 10);

    // Budget value range filter
    setupValueRangeFilter(dataTable, 5);
}

function initializeTendersListTable(table) {
    let columnDefs;
    let order;

    // Define hidden columns
    const project_assets = -5;
    const type_of_work = -4;
    const project_budgets = -3;
    const project_assets_class = -2;
    const project_municipality = -1;
    const hidden_columns = [
        // project_assets, 
        type_of_work, 
        project_budgets, 
        project_assets_class, 
        project_municipality,
    ];

    if (window.canChangeTenders) {
        order = [[1, 'asc']];
        columnDefs = [
            { orderable: false, targets: 0 },
            { visible: false, targets: hidden_columns },
            { targets: 2, type: "sort-integer" },
        ];
    } else {
        order = [[0, 'asc']];
        columnDefs = [
            { visible: false, targets: hidden_columns },
            { targets: 1, type: "sort-integer" }
        ];
    }

    const dataTable = table.DataTable({
        dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        columnDefs: columnDefs,
        order: order,
        language: datatableTranslations,
    });

    // Export tenders table as CSV
    document.getElementById("export-csv").addEventListener("click", () => {
        const headers = [
            window.gettext("Tender Code"),
            window.gettext("Number of Projects"),
            window.gettext("Project(s) Name"),
            window.gettext("Status")
        ];
        exportTable(dataTable, headers, 5, [1, 3], window.gettext("Tenders"));
    });

    // Search box
    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Asset Code or Tender Code");

    // Select Filters
    setupSelectFilter(dataTable, "tender_status_select2", window.gettext("Tender status"), textFilter, 4);
    setupSelectFilter(dataTable, "tender_type_of_work_select2", window.gettext("Type of work"), multipleTextFilter, 6);
    setupSelectFilter(dataTable, "asset_class_select2", window.gettext("Asset class"), multipleTextFilter, 8);
    setupSelectFilter(dataTable, "municipality_select2", window.gettext("Municipality"), multipleTextFilter, 9);

    // Budget value range filter
    setupValueRangeFilter(dataTable, 7);
}

function initializeContractsListTable(table) {
    let columnDefs;
    let order;

    // Define hidden columns
    const project_assets = -4;
    const contract_budget_amendments = -3;
    const project_assets_class = -2;
    const project_municipality = -1;
    const hidden_columns = [
        // project_assets, 
        contract_budget_amendments, 
        project_assets_class, 
        project_municipality,
    ];

    if (window.canChangeProjects) {
        order = [[1, 'asc']];
        columnDefs = [
            { orderable: false, targets: 0 },
            { visible: false, targets: hidden_columns },
            { targets: 2, type: "sort-integer" }
        ];
    } else {
        order = [[0, 'asc']];
        columnDefs = [
            { visible: false, targets: hidden_columns },
            { targets: 1, type: "sort-integer" }
        ];
    }

    const dataTable = table.DataTable({
        dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        columnDefs: columnDefs,
        order: order,
        language: datatableTranslations,
    });

    // Export contracts table as CSV
    document.getElementById("export-csv").addEventListener("click", () => {
        const headers = [
            window.gettext("Contract Code"),
            window.gettext("Number of Projects"),
            window.gettext("Project(s) Name"),
            window.gettext("Type of Work"),
            window.gettext("Status")
        ];
        exportTable(dataTable, headers, 6, [1, 3, 4], window.gettext("Contracts"));
    });

    // Search box
    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Asset Code or Contract Code");

    // Select Filters
    setupSelectFilter(dataTable, "contract_type_of_work_select2", window.gettext("Type of work"), multipleTextFilter, 4);
    setupSelectFilter(dataTable, "contract_status_select2", window.gettext("Contract status"), textFilter, 5);
    setupSelectFilter(dataTable, "asset_class_select2", window.gettext("Asset class"), multipleTextFilter, 8);
    setupSelectFilter(dataTable, "municipality_select2", window.gettext("Municipality"), multipleTextFilter, 9);

    // Budget value range filter
    setupValueRangeFilter(dataTable, 7);
}

function initializeCompaniesListTable(table) {
    let columnDefs;
    let order;

    if (window.canChangeProjects) {
        order = [[1, 'asc']];
        columnDefs = [
            { orderable: false, targets: 0 },
            { visible: false, targets: -1 },
            { targets: [2, 3], type: "sort-integer" }
        ];
    } else {
        order = [[0, 'asc']];
        columnDefs = [
            { visible: false, targets: -1 },
            { targets: [1, 2], type: "sort-integer" }
        ];
    }

    const dataTable = table.DataTable({
        dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        columnDefs: columnDefs,
        order: order,
        language: datatableTranslations,
    });

    // Export companies table as CSV
    document.getElementById("export-csv").addEventListener("click", () => {
        const headers = [
            window.gettext("Name"),
            window.gettext("Total Contracts"),
            window.gettext("Active Contracts")
        ];
        exportTable(dataTable, headers, 4, [1], window.gettext("Companies"));
    });

    // Search box
    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Company Name or Company TIN");
}

function initializeListTable(table, columnDefs, order) {
    if (table.length) {
        table.DataTable({
            dom: "<'row'<'col-12'>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
            columnDefs: columnDefs,
            order: order,
            language: datatableTranslations,
        });
    }
}

function initializePrintableTable(table, columnDefs) {
    if (table.length) {
        table.DataTable({
            dom: "<'row'<'col-12'>><'row'<'col-sm-12'tr>>", // https://datatables.net/reference/option/dom#Styling
            paging: false,
            columnDefs: columnDefs,
            language: datatableTranslations,
        });
    }
}

function exportTable(dataTable, headers, columnsLength, indexes, fileName) {
    const rowsData = dataTable.rows().data();
    const rows = Object.keys(rowsData).map((rowKey) => {
        let rowFields = [];
        for (let index = 1; index < columnsLength; index++) {
            let data = rowsData[rowKey][index];
            if (data == null || data === "None") {
                data = "";
            } else if (indexes.includes(index)) {
                data = data.replace(/<\/?[^>]+(>|$)/g, ""); // strip HTML tags
            }
            rowFields.push(data);
        }
        return rowFields;
    });
    exportCsv(headers, rows, fileName);
}

function setupSelectFilter(dataTable, selectId, placeHolder, filterFunc, columnNo) {
    document.dispatchEvent(new CustomEvent("prepare-select2", { detail: { dataTable, id: selectId, placeHolder } }));
    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return filterFunc(row, columnNo, selectId);
        }
    );
}

function setupValueRangeFilter(dataTable, columnNo) {
    const valueSelectId = "value_select";
    document.getElementById(valueSelectId).addEventListener("change", (e) => {
        const element = e.currentTarget;

        if (element.selectedIndex > 0) element.classList.remove("inactive");
        else element.classList.add("inactive");

        dataTable.draw()
    });
    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return valueRangeFilter(row, columnNo, valueSelectId);
        }
    );
}

const valueRangeFilter = (row, columnIdx, elementId) => {
    const valueFilter = document.getElementById(elementId).selectedOptions.item(0);
    const minValue = valueFilter.dataset.min ? parseInt(valueFilter.dataset.min, 10) : null;
    const maxValue = valueFilter.dataset.max ? parseInt(valueFilter.dataset.max, 10) : null;

    let value = row[columnIdx].split(" ")[1]; // e.g. "$ 500.000" or null

    value = value == null ? 0 : parseInt(value.replace(/\./g, ""), 10);

    if (minValue == null) return true;
    else if (maxValue == null) return value >= minValue;
    else return value >= minValue && value <= maxValue;
}

const textFilter = (row, columnIdx, elementId) => {
    const selectedValues = document.getElementById(elementId).selectedOptions;
    const columnValue = row[columnIdx];

    if (!selectedValues.length) return true;

    for (let value of selectedValues) {
        if (columnValue === value.value) return true;
    };

    return false;
}

const multipleTextFilter = (row, columnIdx, elementId) => {
    const selectedValues = document.getElementById(elementId).selectedOptions;

    if (!selectedValues.length) return true;

    const stripedValues = row[columnIdx].split("<div>");
    let columnValues = [];

    for (let index = 1; index < stripedValues.length; index++) {
        const value = stripedValues[index].replace(/<\/?[^>]+(>|$)/g, "").trim();
        columnValues.push(value);
    }

    for (let selectedValue of selectedValues) {
        for (let columnValue of columnValues) {
            if (columnValue === selectedValue.value) return true;
        };
    };

    return false;
}

// Custom currency sorting function
$.fn.dataTable.ext.type.order['sort-currency-asc'] = function (next, prev) {
    const unformattedNext = next === "" ? undefined : parseInt(next.split(" ")[1].split(".").join(""), 10);
    const unformattedPrev = prev === "" ? undefined : parseInt(prev.split(" ")[1].split(".").join(""), 10);
    if (unformattedNext === undefined) return 1;
    if (unformattedPrev === undefined) return -1;
    return ((unformattedNext < unformattedPrev) ? -1 : ((unformattedNext > unformattedPrev) ? 1 : 0));
};

$.fn.dataTable.ext.type.order['sort-currency-desc'] = function (next, prev) {
    const unformattedNext = next === "" ? undefined : parseInt(next.split(" ")[1].split(".").join(""), 10);
    const unformattedPrev = prev === "" ? undefined : parseInt(prev.split(" ")[1].split(".").join(""), 10);
    return ((unformattedNext < unformattedPrev) ? 1 : ((unformattedNext > unformattedPrev) ? -1 : 0));
};

// Custom integer sorting function
$.fn.dataTable.ext.type.order['sort-integer-asc'] = function (next, prev) {
    const unformattedNext = next === "" ? undefined : parseInt(next.split(".").join(""), 10);
    const unformattedPrev = prev === "" ? undefined : parseInt(prev.split(".").join(""), 10);
    if (unformattedNext === undefined) return 1;
    if (unformattedPrev === undefined) return -1;
    return ((unformattedNext < unformattedPrev) ? -1 : ((unformattedNext > unformattedPrev) ? 1 : 0));
};
$.fn.dataTable.ext.type.order['sort-integer-desc'] = function (next, prev) {
    const unformattedNext = next === "" ? undefined : parseInt(next.split(".").join(""), 10);
    const unformattedPrev = prev === "" ? undefined : parseInt(prev.split(".").join(""), 10);
    return ((unformattedNext < unformattedPrev) ? 1 : ((unformattedNext > unformattedPrev) ? -1 : 0));
};

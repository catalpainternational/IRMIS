import "datatables.net-bs4";
import $ from "jquery";

window.addEventListener("load", () => {
    const projectsListTable = $("#project-list-table");
    const tendersListTable = $("#tender-list-table");
    const contractsListTable = $("#contract-list-table");
    const companiesListTable = $("#company-list-table");

    if (projectsListTable.length) initializeProjectsListTable(projectsListTable);
    if (tendersListTable.length) initializeTendersListTable(tendersListTable);
    if (contractsListTable.length) initializeContractsListTable(contractsListTable);
    if (companiesListTable.length) initializeCompaniesListTable(companiesListTable);

    initializeListTable($("#project-document-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
    initializeListTable($("#project-document-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#tender-document-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
    initializeListTable($("#tender-document-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#contract-inspection-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
    initializeListTable($("#contract-inspection-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#contract-payment-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
    initializeListTable($("#contract-payment-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#contract-social-safeguard-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
    initializeListTable($("#contract-social-safeguard-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#contract-document-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
    initializeListTable($("#contract-document-view-list-table"), [], [[0, 'asc']]);
    initializeListTable($("#company-document-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
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

    if (window.canChangeProjects) {
        order = [[1, 'asc']];
        columnDefs = [
            { orderable: false, targets: 0 },
            { visible: false, targets: [-2, -1] }
        ];
    } else {
        order = [[0, 'asc']];
        columnDefs = [
            { visible: false, targets: [-2, -1] }
        ];
    }

    const dataTable = table.DataTable({
        dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        columnDefs: columnDefs,
        order: order,
    });

    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Asset Code, Project Code or Project Name");

    document.getElementById("status_select2").addEventListener("change", (e) => {
        dataTable.columns(2).search(e.srcElement.value).draw();
    });

    document.getElementById("type_of_work_select2").addEventListener("change", (e) => {
        dataTable.columns(4).search(e.srcElement.value).draw();
    });

    document.getElementById("value_select").addEventListener("change", (e) => {
        dataTable.draw();
    });

    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return valueRangeFilter(row, 5);
        }
    );
}

function initializeTendersListTable(table) {
    let columnDefs;
    let order;

    if (window.canChangeTenders) {
        order = [[1, 'asc']];
        columnDefs = [
            { orderable: false, targets: 0 },
            { visible: false, targets: [-3, -2, -1] }
        ];
    } else {
        order = [[0, 'asc']];
        columnDefs = [
            { visible: false, targets: [-3, -2, -1] }
        ];
    }

    const dataTable = table.DataTable({
        dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        columnDefs: columnDefs,
        order: order,
    });

    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Asset Code or Tender Code");

    document.getElementById("status_select2").addEventListener("change", (e) => {
        dataTable.columns(4).search(e.srcElement.value).draw();
    });

    document.getElementById("type_of_work_select2").addEventListener("change", (e) => {
        dataTable.columns(6).search(e.srcElement.value).draw();
    });

    document.getElementById("value_select").addEventListener("change", (e) => {
        dataTable.draw();
    });

    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return valueRangeFilter(row, 7);
        }
    );
}

function initializeContractsListTable(table) {
    let columnDefs;
    let order;

    if (window.canChangeProjects) {
        order = [[1, 'asc']];
        columnDefs = [
            { orderable: false, targets: 0 },
            { visible: false, targets: [-2, -1] }
        ];
    } else {
        order = [[0, 'asc']];
        columnDefs = [
            { visible: false, targets: [-2, -1] }
        ];
    }

    const dataTable = table.DataTable({
        dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        columnDefs: columnDefs,
        order: order,
    });

    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Asset Code or Contract Code");

    document.getElementById("status_select2").addEventListener("change", (e) => {
        dataTable.columns(5).search(e.srcElement.value).draw();
    });

    document.getElementById("type_of_work_select2").addEventListener("change", (e) => {
        dataTable.columns(7).search(e.srcElement.value).draw();
    });

    document.getElementById("value_select").addEventListener("change", (e) => {
        dataTable.draw();
    });

    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return valueRangeFilter(row, 6);
        }
    );
}

function initializeCompaniesListTable(table) {
    let columnDefs;
    let order;

    if (window.canChangeProjects) {
        order = [[1, 'asc']];
        columnDefs = [
            { orderable: false, targets: 0 },
            { visible: false, targets: -1 }
        ];
    } else {
        order = [[0, 'asc']];
        columnDefs = [
            { visible: false, targets: -1 }
        ];
    }

    table.DataTable({
        dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
        columnDefs: columnDefs,
        order: order,
    });

    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Company Name or Company TIN");
}

function initializeListTable(table, columnDefs, order) {
    if (table.length) {
        table.DataTable({
            dom: "<'row'<'col-12'>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
            columnDefs: columnDefs,
            order: order,
        });
    }
}

function initializePrintableTable(table, columnDefs) {
    if (table.length) {
        table.DataTable({
            dom: "<'row'<'col-12'>><'row'<'col-sm-12'tr>>", // https://datatables.net/reference/option/dom#Styling
            paging: false,
            columnDefs: columnDefs,
        });
    }
}

let valueRangeFilter = (row, columnIdx, elementId) => {
    const valueFilter = document.getElementById(elementId).selectedOptions.item(0);
    const minValue = valueFilter.dataset.min ? parseInt(valueFilter.dataset.min, 10) : null;
    const maxValue = valueFilter.dataset.max ? parseInt(valueFilter.dataset.max, 10) : null;

    let value = row[columnIdx].split(" ")[1]; // e.g. "$ 500.000" or "None"

    value = value === "None" ? 0 : parseInt(value, 10);

    if (minValue == null) return true;
    else if (maxValue == null) return value >= minValue;
    else return value >= minValue && value <= maxValue;
}

let textFilter = (row, columnIdx, elementId) => {
    const selectedValues = document.getElementById(elementId).selectedOptions;
    const columnValue = row[columnIdx];

    if (!selectedValues.length) return true;

    for (let value of selectedValues) {
        if (columnValue === value.text) return true;
    };

    return false;
}

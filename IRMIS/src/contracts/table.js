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

    // Search box
    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Asset Code, Project Code or Project Name");

    // Budget value range filter
    const valueSelectId = "value_select";
    document.getElementById(valueSelectId).addEventListener("change", () => dataTable.draw());
    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return valueRangeFilter(row, 5, valueSelectId);
        }
    );

    // Status select2 filter
    const statusSelectId = "status_select2";
    document.dispatchEvent(new CustomEvent("prepare-select2", { detail: { dataTable: dataTable, id: statusSelectId, placeHolder: window.gettext("Project status") } }));
    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return textFilter(row, 2, statusSelectId);
        }
    );

    // Type of work select2 filter
    const typeOfWorkSelectId = "type_of_work_select2";
    document.dispatchEvent(new CustomEvent("prepare-select2", { detail: { dataTable: dataTable, id: typeOfWorkSelectId, placeHolder: window.gettext("Type of work") } }));
    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return textFilter(row, 4, typeOfWorkSelectId);
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

    // Search box
    const searchBox = document.querySelector(".dataTables_filter input[type='search']");
    searchBox.attributes.getNamedItem("placeholder").value = window.gettext("Search by Asset Code or Tender Code");

    // Budget value range filter
    const valueSelectId = "value_select";
    document.getElementById(valueSelectId).addEventListener("change", () => dataTable.draw());
    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return valueRangeFilter(row, 7, valueSelectId);
        }
    );

    // Status select2 filter
    const statusSelectId = "status_select2";
    document.dispatchEvent(new CustomEvent("prepare-select2", { detail: { dataTable: dataTable, id: statusSelectId, placeHolder: window.gettext("Tender status") } }));
    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return textFilter(row, 4, statusSelectId);
        }
    );

    // Type of work select2 filter
    const typeOfWorkSelectId = "type_of_work_select2";
    document.dispatchEvent(new CustomEvent("prepare-select2", { detail: { dataTable: dataTable, id: typeOfWorkSelectId, placeHolder: window.gettext("Type of work") } }));
    $.fn.dataTableExt.afnFiltering.push(
        function (oSettings, _aData, iDataIndex) {
            let row = oSettings.aoData[iDataIndex]._aData;
            return multipleTextFilter(row, 6, typeOfWorkSelectId);
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

let multipleTextFilter = (row, columnIdx, elementId) => {
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
            if (columnValue === selectedValue.text) return true;
        };
    };

    return false;
}

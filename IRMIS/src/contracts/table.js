import "datatables.net-bs4";
import $ from "jquery";

if (window.canChangeProjects) {
    initializeSearchableTable($("#project-list-table"), [{ orderable: false, targets: 0 }, { visible: false, targets: [-2, -1] }], [[1, 'asc']]);
} else {
    initializeSearchableTable($("#project-list-table"), [{ visible: false, targets: [-2, -1] }], [[1, 'asc']]);
}

if (window.canChangeTenders) {
    initializeSearchableTable($("#tender-list-table"), [{ orderable: false, targets: 0 }, { visible: false, targets: -1 }], [[1, 'asc']]);
} else {
    initializeSearchableTable($("#tender-list-table"), [{ visible: false, targets: -1 }], [[1, 'asc']]);
}

if (window.canChangeContracts) initializeProjectsTable($("#contract-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
else initializeProjectsTable($("#contract-list-table"), [], [[1, 'asc']]);

if (window.canChangeCompanies) initializeProjectsTable($("#company-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
else initializeProjectsTable($("#company-list-table"), [], [[1, 'asc']]);

initializeProjectsTable($("#project-document-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
initializeProjectsTable($("#project-document-view-list-table"), [], [[0, 'asc']]);
initializeProjectsTable($("#tender-document-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
initializeProjectsTable($("#tender-document-view-list-table"), [], [[0, 'asc']]);
initializeProjectsTable($("#contract-inspection-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
initializeProjectsTable($("#contract-inspection-view-list-table"), [], [[0, 'asc']]);
initializeProjectsTable($("#contract-payment-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
initializeProjectsTable($("#contract-payment-view-list-table"), [], [[0, 'asc']]);
initializeProjectsTable($("#contract-social-safeguard-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
initializeProjectsTable($("#contract-social-safeguard-view-list-table"), [], [[0, 'asc']]);
initializeProjectsTable($("#contract-document-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
initializeProjectsTable($("#contract-document-view-list-table"), [], [[0, 'asc']]);
initializeProjectsTable($("#company-document-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
initializeProjectsTable($("#company-document-view-list-table"), [], [[0, 'asc']]);

initializeProjectsPrintableTable($("#project-document-print-list-table"), []);
initializeProjectsPrintableTable($("#tender-document-print-list-table"), []);
initializeProjectsPrintableTable($("#contract-inspection-print-list-table"), []);
initializeProjectsPrintableTable($("#contract-payment-print-list-table"), []);
initializeProjectsPrintableTable($("#contract-social-safeguard-print-list-table"), []);
initializeProjectsPrintableTable($("#contract-document-print-list-table"), []);
initializeProjectsPrintableTable($("#company-document-print-list-table"), []);

function initializeSearchableTable(table, columnDefs, order) {
    if (table.length) {
        table.DataTable({
            dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
            columnDefs: columnDefs,
            order: order,
        });
    }
}

function initializeProjectsTable(table, columnDefs, order) {
    if (table.length) {
        table.DataTable({
            dom: "<'row'<'col-12'>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
            columnDefs: columnDefs,
            order: order,
        });
    }
}

function initializeProjectsPrintableTable(table, columnDefs) {
    if (table.length) {
        table.DataTable({
            dom: "<'row'<'col-12'>><'row'<'col-sm-12'tr>>", // https://datatables.net/reference/option/dom#Styling
            paging: false,
            columnDefs: columnDefs,
        });
    }
}

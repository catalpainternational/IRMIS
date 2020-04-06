import "datatables.net-bs4";
import $ from "jquery";

if (window.canChangeProjects) initializeProjectsTable($("#project-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
else initializeProjectsTable($("#project-list-table"), [], [[1, 'asc']]);

if (window.canChangeTenders) initializeProjectsTable($("#tender-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
else initializeProjectsTable($("#tender-list-table"), [], [[1, 'asc']]);

if (window.canChangeContracts) initializeProjectsTable($("#contract-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
else initializeProjectsTable($("#contract-list-table"), [], [[1, 'asc']]);

if (window.canChangeCompanies) initializeProjectsTable($("#company-list-table"), [{ orderable: false, targets: 0 }], [[1, 'asc']]);
else initializeProjectsTable($("#company-list-table"), [], [[1, 'asc']]);

initializeProjectsTable($("#contract-inspection-list-table"), [{ orderable: false, targets: 4 }], [[0, 'asc']]);
initializeProjectsTable($("#contract-inspection-view-list-table"), [], [[0, 'asc']]);
initializeProjectsTable($("#contract-payment-list-table"), [{ orderable: false, targets: 5 }], [[0, 'asc']]);
initializeProjectsTable($("#contract-payment-view-list-table"), [], [[0, 'asc']]);
initializeProjectsTable($("#contract-social-safeguard-list-table"), [{ orderable: false, targets: 5 }], [[0, 'asc']]);
initializeProjectsTable($("#contract-social-safeguard-view-list-table"), [], [[0, 'asc']]);

initializeProjectsPrintableTable($("#contract-inspection-print-list-table"), []);
initializeProjectsPrintableTable($("#contract-payment-print-list-table"), []);
initializeProjectsPrintableTable($("#contract-social-safeguard-print-list-table"), []);

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

import "datatables.net-bs4";
import $ from "jquery";

const projectsTable = $("#project-list-table");
const projectsColumnDefs = window.canChangeContractsProjects ? [{ orderable: false, targets: 6 }] : [];
const tendersTable = $("#tender-list-table");
const tendersColumnDefs = window.canChangeContractsTenders ? [{ orderable: false, targets: 4 }] : [];
const contractsTable = $("#contract-list-table");
const contractsColumnDefs = window.canChangeContracts ? [{ orderable: false, targets: 5 }] : [];
const companiesTable = $("#company-list-table");
const companiesColumnDefs = window.canChangeContractsCompanies ? [{ orderable: false, targets: 3 }] : [];
const inspectionsTable = $("#contract-inspection-list-table");
const inspectionsColumnDefs = [{ orderable: false, targets: 4 }];
const inspectionsViewTable = $("#contract-inspection-view-list-table");
const inspectionsPrintTable = $("#contract-inspection-print-list-table");
const paymentsTable = $("#contract-payment-list-table");
const paymentsColumnDefs = [{ orderable: false, targets: 5 }];
const paymentsViewTable = $("#contract-payment-view-list-table");
const paymentsPrintTable = $("#contract-payment-print-list-table");
const socialSafeguardTable = $("#contract-social-safeguard-list-table");
const socialSafeguardColumnDefs = [{ orderable: false, targets: 5 }];
const socialSafeguardViewTable = $("#contract-social-safeguard-view-list-table");
const socialSafeguardPrintTable = $("#contract-social-safeguard-print-list-table");

initializeProjectsTable(projectsTable, projectsColumnDefs);
initializeProjectsTable(tendersTable, tendersColumnDefs);
initializeProjectsTable(contractsTable, contractsColumnDefs);
initializeProjectsTable(companiesTable, companiesColumnDefs);
initializeProjectsTable(inspectionsTable, inspectionsColumnDefs);
initializeProjectsTable(inspectionsViewTable, []);
initializeProjectsTable(paymentsTable, paymentsColumnDefs);
initializeProjectsTable(paymentsViewTable, []);
initializeProjectsTable(socialSafeguardTable, socialSafeguardColumnDefs);
initializeProjectsTable(socialSafeguardViewTable, []);

initializeProjectsPrintableTable(inspectionsPrintTable, []);
initializeProjectsPrintableTable(paymentsPrintTable, []);
initializeProjectsPrintableTable(socialSafeguardPrintTable, []);

function initializeProjectsTable(table, columnDefs) {
    if (table.length) {
        table.DataTable({
            dom: "<'row'<'col-12'>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
            columnDefs: columnDefs,
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

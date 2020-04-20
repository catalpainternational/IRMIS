import "datatables.net-bs4";
import $ from "jquery";

window.addEventListener("load", () => {
    const projectPlaceholderText = window.gettext("Search by Asset Code, Project Code or Project Name");
    const tenderPlaceholderText = window.gettext("Search by Asset Code or Tender Code");
    const contractPlaceholderText = window.gettext("Search by Asset Code or Contract Code");
    const companyPlaceholderText = window.gettext("Search by Company Name or Company TIN");

    if (window.canChangeProjects) {
        initializeSearchableTable($("#project-list-table"), [{ orderable: false, targets: 0 }, { visible: false, targets: [-2, -1] }], [[1, 'asc']], projectPlaceholderText);
    } else {
        initializeSearchableTable($("#project-list-table"), [{ visible: false, targets: [-2, -1] }], [[1, 'asc']], projectPlaceholderText);
    }

    if (window.canChangeTenders) {
        initializeSearchableTable($("#tender-list-table"), [{ orderable: false, targets: 0 }, { visible: false, targets: -1 }], [[1, 'asc']], tenderPlaceholderText);
    } else {
        initializeSearchableTable($("#tender-list-table"), [{ visible: false, targets: -1 }], [[1, 'asc']], tenderPlaceholderText);
    }

    if (window.canChangeContracts) {
        initializeSearchableTable($("#contract-list-table"), [{ orderable: false, targets: 0 }, { visible: false, targets: -1 }], [[1, 'asc']], contractPlaceholderText);
    } else {
        initializeSearchableTable($("#contract-list-table"), [{ visible: false, targets: -1 }], [[1, 'asc']], contractPlaceholderText);
    }

    if (window.canChangeCompanies) {
        initializeSearchableTable($("#company-list-table"), [{ orderable: false, targets: 0 }, { visible: false, targets: -1 }], [[1, 'asc']], companyPlaceholderText);
    } else {
        initializeSearchableTable($("#company-list-table"), [{ visible: false, targets: -1 }], [[1, 'asc']], companyPlaceholderText);
    }

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
});

function initializeSearchableTable(table, columnDefs, order, searchPlaceholder) {
    if (table.length) {
        const dataTable = table.DataTable({
            dom: "<'row'<'col-12'f>><'row'<'col-sm-12'tr>><'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>", // https://datatables.net/reference/option/dom#Styling
            columnDefs: columnDefs,
            order: order,
        });

        const searchBox = document.querySelector(".dataTables_filter input[type='search']");
        const statusFilter = document.getElementById("status_select2");

        searchBox.attributes.getNamedItem("placeholder").value = searchPlaceholder;

        if (statusFilter) {
            statusFilter.addEventListener("change", (e) => {
                dataTable.columns(2).search(e.srcElement.value).draw();
            });
        }
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

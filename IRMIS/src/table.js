import jsZip from "jszip";
import "datatables.net-bs4";
import "datatables.net-buttons-bs4";
import "datatables.net-buttons/js/buttons.html5";
import "datatables.net-buttons/js/buttons.flash";
import $ from "jquery";

let table;
let pendingRows = [];

// needed for export to excel
window.JSZip = jsZip;

// when the roadManager has new roads, add them to the table
document.addEventListener('estrada.roadManager.roadMetaDataAdded', (data) => {
    // add the roads to the table
    pendingRows =  pendingRows.concat(data.detail.roadList);
    if( table ) {
        table.rows.add(pendingRows).draw();
        pendingRows = [];
    } else {
        console.log('received new roads before table is ready');
    }
});

document.addEventListener('estrada.table.roadMetaDataUpdated', (data) => {
    table.row(`#${data.detail.road.id}`).data(data.detail.road).draw();
});

// when a filter is applied, update the filter id whitelist
document.addEventListener('estrada.filter.applied', (data) => {
    idWhitelistMap = data.detail.idMap;
    table.draw();
});

// when the view changes adjust the table rows
document.addEventListener('estrada.sideMenu.viewChanged', (data) => {
    const viewName = data.detail ? data.detail.viewName : null;
    if (viewName === 'map table') {
        table.page.len(10).draw('page');
    } else if (viewName === 'table') {
        table.page.len(20).draw('page');
    }
});

window.addEventListener('load', () => {
    initializeDataTable();

    // Append table name onto DataTable generated layout
    document.getElementsByClassName("dt-buttons").item(0).prepend(document.getElementById("table-name"));
});

function initializeDataTable() {
    const date = new Date();
    const columns = [
        {
            title: 'Road Code', data: null,
            render: 'code',
            type: "roadCode"
        },
        {
            title: 'Type', data: null,
            render: 'type'
        },
        {
            title: 'Name', data: null,
            render: 'name'
        },
        {
            title: 'Status', data: null,
            render: 'status'
        },
        {
            title: 'Link Code', data: null,
            render: 'linkCode'
        },
        {
            title: 'Link Name', data: null,
            render: 'linkName'
        },
        {
            title: 'Link Start Name', data: null,
            render: 'linkStartName'
        },
        {
            title: 'Link Start Chainage (Km)', data: null,
            render: r => parseFloat(r.linkStartChainage).toFixed(2)
        },
        {
            title: 'Link End Name', data: null,
            render: 'linkEndName'
        },
        {
            title: 'Link End Chainage (Km)', data: null,
            render: r => parseFloat(r.linkEndChainage).toFixed(2)
        },
        {
            title: 'Link Length (Km)', data: null,
            render: r => parseFloat(r.linkLength).toFixed(2)
        },
        {
            title: 'Surface Type', data: null,
            render: 'surfaceType'
        },
        {
            title: 'Surface Condition', data: null,
            render: 'surfaceCondition'
        },
        {
            title: 'Pavement Class', data: null,
            render: 'pavementClass'
        },
        {
            title: 'Administrative Area', data: null,
            render: 'administrativeArea'
        },
        {
            title: 'Carriageway Width (m)', data: null,
            render: r => parseFloat(r.carriagewayWidth).toFixed(2)
        },
        {
            title: 'Project', data: null,
            render: 'project'
        },
        {
            title: 'Funding Source', data: null,
            render: 'fundingSource'
        },
        {
            title: 'Technical Class', data: null,
            render: 'technicalClass'
        },
        {
            title: 'Maintenance needs', data: null,
            render: 'maintenanceNeed'
        },
        {
            title: 'Traffic Data', data: null,
            render: 'trafficLevel'
        }
    ];

    if (window.canEdit) {
        columns.unshift({
            title: '', data: null,
            render: r => `<a class='image pencil' href='#edit/${r.getId()}/location_type'></a>`,
            orderable: false,
            className: "edit-col"
        });
    }

    table = $("#data-table").DataTable({
        columns: columns,
        rowId: '.getId()',
        order: [[window.canEdit ? 1 : 0, 'asc']], // default order is ascending by road code
        dom: `<'row'<'col-12'B>> + <'row'<'col-sm-12'tr>> + <'row'<'col-md-12 col-lg-5'i><'col-md-12 col-lg-7'p>>`, // https://datatables.net/reference/option/dom#Styling
        buttons: [{
            extend: "excel",
            className: "btn-sm",
            sheetName: "Estrada",
            text: "Export table",
            title: "Estrada_" + date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate(),
        }]
    });
    if (pendingRows.length) {
        console.log('adding roads now table is ready');
        table.rows.add(pendingRows).draw();
        pendingRows = [];
    }

}

// Filter functionality
let idWhitelistMap = null;
let currentFilter = (p) => {
    return idWhitelistMap === null || idWhitelistMap[p.getId().toString()];
}

$.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
        let road = oSettings.aoData[iDataIndex]._aData;
        return currentFilter(road);
    }
);

// change the sorting of the road code column to place empty values last
$.extend($.fn.dataTableExt.oSort, {
    "roadCode-asc": function (str1, str2) {
        if(str1 == "") return 1;
        if(str2 == "") return -1;
        return ((str1 < str2) ? -1 : ((str1 > str2) ? 1 : 0));
    },

    "roadCode-desc": function (str1, str2) {
        if(str1 == "") return -1;
        if(str2 == "") return 1;
        return ((str1 < str2) ? 1 : ((str1 > str2) ? -1 : 0));
    }
});

import { EstradaRoad } from "./assets/models/road";

/** Define the general events that the main table will respond to
 *
 * Note that the passed in values `pendingRows` and `idWhiteListMap`
 * are carefully updated (as opposed to simply reassigned).
 * This ensures that their 'update' is visible to the 'outside'.
 */
export const estradaTableEventListeners = {
    /** when the roadManager has new roads, add them to the table */
    "estrada.roadManager.roadMetaDataAdded": (data, table, pendingRows) => {
        const roadList = data.detail.roadList;

        // add the roads to a pending array ( in case the table is not initialised early enough )
        // Note we can't use array.concat here because concat returns a new array
        // and we need to retain the existing pendingRows array
        roadList.forEach((road) => pendingRows.push(road));
        if (table) {
            table.rows.add(pendingRows).draw();
            // truncate the pendingRows (superfast)
            pendingRows.length = 0;
        }
    },
    "estrada.table.roadMetaDataUpdated": (data, table) => {
        const road = data.detail.road;
        table.row(`#${road.id}`).data(road).draw();
    },
    /** when a filter is applied, update the filter id whitelist */
    "estrada.filter.applied": (data, table, pendingRows, idWhitelistMap) => {
        Object.keys(idWhitelistMap).forEach((key) => { idWhitelistMap[key] = undefined; });

        const idMap = data.detail.idMap;
        Object.keys(idMap).forEach((key) => { idWhitelistMap[key] = idMap[key]; });

        table.draw();
    },
    /** when the view changes adjust the table rows */
    "estrada.sideMenu.viewChanged": (data, table) => {
        const viewName = data.detail ? data.detail.viewName : null;
        if (viewName && viewName.indexOf('table') !== -1) {
            const tableRows = (viewName === 'table') ? 20 : 10;
            table.page.len(tableRows).draw('page');
        }
    }
};

/** Defines the columns for the table on the Estrada main page */
export const estradaTableColumns = [
    {
        title: EstradaRoad.getFieldName("road_code"),
        data: "code",
        defaultContent: "",
        type: "roadCode",
        className: "text-center",
    },
    {
        title: EstradaRoad.getFieldName("road_name"),
        data: "name",
        defaultContent: "",
        visible: false,
    },
    {
        title: EstradaRoad.getFieldName("link_code"),
        data: "linkCode",
        defaultContent: "",
        className: "text-center",
    },
    {
        title: window.gettext("Link Name"),
        data: "linkName",
        defaultContent: "",
        visible: false,
    },
    {
        title: EstradaRoad.getFieldName("link_length"),
        data: "linkLength",
        defaultContent: "",
        className: "text-right",
    },
    {
        title: EstradaRoad.getFieldName("link_start_name"),
        data: "linkStartName",
        defaultContent: "",
    },
    {
        title: EstradaRoad.getFieldName("link_start_chainage"),
        data: "linkStartChainage",
        defaultContent: "",
        className: "text-right",
    },
    {
        title: EstradaRoad.getFieldName("link_end_name"),
        data: "linkEndName",
        defaultContent: "",
    },
    {
        title: EstradaRoad.getFieldName("link_end_chainage"),
        data: "linkEndChainage",
        defaultContent: "",
        className: "text-right",
    },
    {
        title: EstradaRoad.getFieldName("surface_type"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("surface_type", r),
        orderable: false,
        className: "text-center",
    },
    {
        title: EstradaRoad.getFieldName("pavement_class"),
        data: "pavementClass",
        defaultContent: "",
        className: "text-center",
    },
    {
        title: EstradaRoad.getFieldName("carriageway_width"),
        data: "carriagewayWidth",
        defaultContent: "",
        className: "text-right",
    },
    {
        title: EstradaRoad.getFieldName("administrative_area"),
        data: "administrativeArea",
        defaultContent: "",
    },
    {
        title: EstradaRoad.getFieldName("road_type"),
        data: "type",
        defaultContent: "",
        visible: false,
        className: "text-center",
    },
    {
        title: EstradaRoad.getFieldName("technical_class"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("technical_class", r),
        visible: false,
        orderable: false,
        className: "text-center",
    },
    {
        title: EstradaRoad.getFieldName("funding_source"),
        data: "fundingSource",
        defaultContent: "",
        visible: false
    },
    {
        title: EstradaRoad.getFieldName("road_status"),
        data: "status",
        defaultContent: "",
        visible: false,
        className: "text-center",
    },
    {
        title: EstradaRoad.getFieldName("project"),
        data: "project",
        defaultContent: "",
        visible: false,
    },
    {
        title: EstradaRoad.getFieldName("surface_condition"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("surface_condition", r),
        className: "text-center",
        orderable: false,
    },
    {
        title: EstradaRoad.getFieldName("maintenance_need"),
        data: "maintenanceNeed",
        defaultContent: "",
        visible: false,
        className: "text-center",
    },
    {
        title: EstradaRoad.getFieldName("traffic_level"),
        data: "trafficLevel",
        defaultContent: "",
        visible: false,
        className: "text-center",
    },
    {
        title: window.gettext("Start Point (DMS)"),
        data: "startDMS",
        defaultContent: "",
        visible: false,
        className: "text-center",
    },
    {
        title: window.gettext("End Point (DMS)"),
        data: "endDMS",
        defaultContent: "",
        visible: false,
        className: "text-center",
    },
    {
        title: window.gettext("Start Point (UTM)"),
        data: "startUTM",
        defaultContent: "",
        visible: false,
        className: "text-center",
    },
    {
        title: window.gettext("End Point (UTM)"),
        data: "endUTM",
        defaultContent: "",
        visible: false,
        className: "text-center",
    },
    {
        title: EstradaRoad.getFieldName("number_lanes"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("number_lanes", r),
        visible: false,
        className: "text-center",
        orderable: false,
    },
];

function buttonSegmentsTemplate(attrib, road) {
    return `<a data-toggle="modal"
        data-target="#inventory-segments-modal"
        data-code="${road.getLinkCode()}"
        data-id="${road.getId()}"
        data-attr="${attrib}">${window.gettext("View")} ${EstradaRoad.getFieldName(attrib)}</a>`;
}

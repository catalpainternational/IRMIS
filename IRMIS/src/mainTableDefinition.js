import { EstradaBridge, EstradaCulvert } from "./assets/models/structures";
import { EstradaRoad } from "./assets/models/road";
import { assetTypeName } from "./side_menu";

/** Define the general events that the main tables will respond to
 *
 * Note that the passed in values `pendingRoads` / `pendingStructures` and `idWhiteListMap`
 * are carefully updated (as opposed to simply reassigned).
 * This ensures that their 'update' is visible to the 'outside'.
 */
export const estradaRoadTableEventListeners = {
    /** when the roadManager has new roads, add them to the table */
    "estrada.roadManager.roadMetaDataAdded": (data, table, pendingRoads) => {
        const roadList = data.detail.roadList;

        // add the roads to a pending array ( in case the table is not initialised early enough )
        // Note we can't use array.concat here because concat returns a new array
        // and we need to retain the existing pendingRoads array
        roadList.forEach((road) => pendingRoads.push(road));
        if (table) {
            table.rows.add(pendingRoads).draw();
            // truncate the pendingRoads (superfast)
            pendingRoads.length = 0;
        }
    },
    "estrada.roadTable.roadMetaDataUpdated": (data, table) => {
        const road = data.detail.road;
        table.row(`#${road.id}`).data(road).draw();
    },
    /** when a filter is applied, update the filter id whitelist */
    "estrada.roadTable.filter.applied": (data, table, pendingRows, idWhitelistMap) => {
        Object.keys(idWhitelistMap).forEach((key) => { idWhitelistMap[key] = undefined; });

        const idMap = data.detail.idMap;
        Object.keys(idMap).forEach((key) => { idWhitelistMap[key] = idMap[key]; });

        table.draw();
    },
    /** when the view changes adjust the table rows */
    "estrada.roadTable.sideMenu.viewChanged": (data, table) => {
        const viewName = data.detail ? data.detail.viewName : null;
        if (viewName && viewName.indexOf('table') !== -1) {
            const tableRows = (viewName === 'table') ? 20 : 10;
            table.page.len(tableRows).draw('page');
        }
    },
    /** select a row in the table by id */
    "estrada.roadTable.table.rowSelected": (data, table) => {
        const rowId = data.detail ? data.detail.rowId : null;
        if (rowId) {
            const featureType = data.detail ? data.detail.featureType : "";
            const assetType = "roads";

            table.rows().every(function (rowIdx, tableLoop, rowLoop) {
                if (assetType !== assetTypeName || this.id() !== rowId) {
                    this.node().classList.remove("selected");
                } else {
                    this.node().classList.add("selected");
                    table.row(this.index()).show().draw(false);
                }
            });
        }
    }
};
export const estradaStructureTableEventListeners = {
    /** when the structureManager has new structures, add them to the table */
    "estrada.structureManager.structureMetaDataAdded": (data, table, pendingStructures) => {
        // structures is a keyed object
        const structures = data.detail.structures;

        // add the structures to a pending array ( in case the table is not initialised early enough )
        // Note we can't use array.concat here because concat returns a new array
        // and we need to retain the existing pendingStructures array
        Object.keys(structures).forEach((key) => pendingStructures.push(structures[key]));
        if (table) {
            table.rows.add(pendingStructures).draw();
            // truncate the pendingStructures (superfast)
            pendingStructures.length = 0;
        }
    },
    "estrada.structureTable.roadMetaDataUpdated": (data, table) => {
        const road = data.detail.road;
        table.row(`#${road.id}`).data(road).draw();
    },
    /** when a filter is applied, update the filter id whitelist */
    "estrada.structureTable.filter.applied": (data, table, pendingRows, idWhitelistMap) => {
        Object.keys(idWhitelistMap).forEach((key) => { idWhitelistMap[key] = undefined; });

        const idMap = data.detail.idMap;
        Object.keys(idMap).forEach((key) => { idWhitelistMap[key] = idMap[key]; });

        table.draw();
    },
    /** when the view changes adjust the table rows */
    "estrada.structureTable.sideMenu.viewChanged": (data, table) => {
        const viewName = data.detail ? data.detail.viewName : null;
        if (viewName && viewName.indexOf('table') !== -1) {
            const tableRows = (viewName === 'table') ? 20 : 10;
            table.page.len(tableRows).draw('page');
        }
    },
    /** select a row in the table by id */
    "estrada.structureTable.table.rowSelected": (data, table) => {
        const rowId = data.detail ? data.detail.rowId : null;
        if (rowId) {
            const featureType = data.detail ? data.detail.featureType : "";
            const assetType = "structures";

            table.rows().every(function (rowIdx, tableLoop, rowLoop) {
                if (assetType !== assetTypeName || this.id() !== rowId) {
                    this.node().classList.remove("selected");
                } else {
                    this.node().classList.add("selected");
                    table.row(this.index()).show().draw(false);
                }
            });
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
        render: linkLength => linkLength / 1000,
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
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("pavement_class", r),
        className: "text-center",
        orderable: false,
    },
    {
        title: EstradaRoad.getFieldName("carriageway_width"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("carriageway_width", r),
        className: "text-center",
        orderable: false,
    },
    {
        title: EstradaRoad.getFieldName("administrative_area"),
        data: "administrativeArea",
        defaultContent: "",
    },
    {
        // 'road_type' name has been deprecated and will be replaced with 'asset_class'
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
        title: window.gettext("Roughness (IRI)"),
        data: "",
        defaultContent: "",
        visible: false,
        className: "text-center",
    },
    {
        title: EstradaRoad.getFieldName("asset_condition"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("asset_condition", r),
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
        title: EstradaRoad.getFieldName("number_lanes"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("number_lanes", r),
        visible: false,
        className: "text-center",
        orderable: false,
    },
    {
        title: EstradaRoad.getFieldName("rainfall"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("rainfall", r),
        visible: false,
        className: "text-center",
        orderable: false,
    },
    {
        title: EstradaRoad.getFieldName("terrain_class"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("terrain_class", r),
        visible: false,
        className: "text-center",
        orderable: false,
    },
];

/** Defines the columns for the Structures table on the Estrada main page */
export const structuresTableColumns = [
    {
        title: window.gettext("Structure"),
        render: s => detectStructure(s),
        data: null,
        className: "text-center",
    },
    {
        title: getStructureFieldName("structure_code"),
        data: "structureCode",
        className: "text-center",
        defaultContent: "",
    },
    {
        title: getStructureFieldName("structure_name"),
        data: "structureName",
        className: "text-center",
        defaultContent: "",
    },
    {
        title: getStructureFieldName("river_name"),
        data: "riverName",
        className: "text-center",
        defaultContent: "",
        visible: false,
    },
    {
        title: getStructureFieldName("road_code"),
        data: "roadCode",
        className: "text-center",
        defaultContent: "",
    },
    // {
    //     title: getStructureFieldName("road_name"),
    //     data: "roadName",
    //     className: "text-center",
    //     defaultContent: "",
    //     visible: false,
    // },
    {
        title: getStructureFieldName("asset_class"),
        data: "assetClass",
        className: "text-center",
        defaultContent: "",
        visible: false,
    },
    {
        title: "GPS Longitude",
        className: "text-right",
        defaultContent: "43.599307°N",
        visible: false,
    },
    {
        title: "GPS Latitude",
        className: "text-right",
        defaultContent: "1.438724°E",
        visible: false,
    },
    {
        title: getStructureFieldName("chainage"),
        data: "chainage",
        className: "text-right",
        defaultContent: "",
    },
    {
        title: getStructureFieldName("administrative_area"),
        data: "administrativeArea",
        className: "text-center",
        defaultContent: "",
        visible: false,
    },
    // {
    //     title: "Type",
    //     defaultContent: "New bridge",
    // },
    {
        title: getStructureFieldName("material"),
        data: "material",
        className: "text-center",
        defaultContent: "",
    },
    {
        title: getStructureFieldName("structure_type"),
        data: "structureType",
        className: "text-center",
        defaultContent: "N/A",
    },
    {
        title: getStructureFieldName("length"),
        data: "length",
        className: "text-right",
        defaultContent: "",
    },
    {
        title: getStructureFieldName("width"),
        data: "width",
        className: "text-right",
        defaultContent: "",

    },
    {
        title: getStructureFieldName("height"),
        data: "height",
        className: "text-right",
        defaultContent: "",
        visible: false,
    },
    {
        title: getStructureFieldName("number_spans"),
        data: "numberSpans",
        className: "text-right",
        defaultContent: "N/A",
        visible: false,
    },
    {
        title: getStructureFieldName("number_cells"),
        data: "numberCells",
        className: "text-right",
        defaultContent: "N/A",
        visible: false,
    },
    {
        title: getStructureFieldName("protection_upstream"),
        data: "protectionUpstream",
        className: "text-center",
        defaultContent: "",
        visible: false,
    },
    {
        title: getStructureFieldName("protection_downstream"),
        data: "protectionDownstream",
        className: "text-center",
        defaultContent: "",
        visible: false,
    },
    {
        title: getStructureFieldName("construction_year"),
        data: "constructionYear",
        className: "text-right",
        defaultContent: "",
        visible: false,
    },
    {
        title: "Structure Condition",
        defaultContent: "x",
        className: "text-center",
        render: r => buttonSegmentsTemplate("structure_condition", r),
        data: null,
        visible: false,
    },
    {
        title: "Condition Description",
        defaultContent: "x",
        className: "text-center",
        render: r => buttonSegmentsTemplate("condition", r),
        data: null,
        visible: false,
    },
    {
        title: "Inventory Photos",
        defaultContent: "x",
        className: "text-center",
        render: r => buttonSegmentsTemplate("inventory_photos", r),
        data: null
    },
];

function detectStructure(structure) {
    switch (structure.constructor.name) {
        case "EstradaBridge":
            return "Bridge";
        case "EstradaCulvert":
            return "Culvert";
        default:
            return null;
    }
}

function getStructureFieldName(field) {
    try {
        return EstradaBridge.getFieldName(field);
    } catch (err) {
        return EstradaCulvert.getFieldName(field);
    }
}

// function getStructureFieldData(field, structure) { return null; }
function buttonSegmentsTemplate(attrib, asset) {
    const assetStructureType = detectStructure(asset);
    const assetType = !assetStructureType
        ? assetTypeName === "roads" ? "roads" : "structures"
        : assetStructureType === "Bridge" ? "bridges" : "culverts";

    const code = (assetType === "roads") ? asset.getLinkCode() : asset.getStructureCode();
    let getFieldName = (attrib) => (attrib);
    switch (assetType) {
        case "roads":
            getFieldName = EstradaRoad.getFieldName;
            break;
        case "bridges":
            getFieldName = EstradaBridge.getFieldName;
            break;
        case "culverts":
            getFieldName = EstradaCulvert.getFieldName;
            break;
        default:
            break;
    }

    return `<a data-toggle="modal"
        data-target="#inventory-segments-modal"
        data-code="${code}"
        data-id="${asset.getId()}"
        data-attr="${attrib}">${window.gettext("View")} ${getFieldName(attrib)}</a>`;
}

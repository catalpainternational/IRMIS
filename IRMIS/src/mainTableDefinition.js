import { EstradaBridge, EstradaCulvert, EstradaDrift } from "./assets/models/structures";
import { EstradaRoad } from "./assets/models/road";

import { toChainageFormat } from "./assets/protoBufUtilities";
import { formatNumber } from "./assets/utilities";

import { currentFilter } from "./side_menu";

/** Define the general events that the main tables will respond to
 *
 * Note that the passed in values 'pendingRoads' / 'pendingStructures' and 'idWhiteListMap'
 * are carefully updated (as opposed to simply reassigned).
 * This ensures that their 'update' is visible to the 'outside'.
 */
export const estradaRoadTableEventListeners = {
    /** when the roadManager has new roads, add them to the table */
    "estrada.road.assetMetaDataAdded": (data, table, pendingRoads) => {
        const roadList = data.detail.assets;

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
    "estrada.road.assetMetaDataUpdated": (data, table) => eventTableAssetMetaDataUpdated(data, table),
    "estrada.road.filter.applied": (data, table, pendingRows, idWhitelistMap) => eventFilterApplied(data, table, pendingRows, idWhitelistMap),
    "estrada.road.sideMenu.viewChanged": (data, table) => eventSideMenuViewChanged(data, table),
    "estrada.roadTable.rowSelected": (data, table) => eventTableRowSelected(data, table),
};

export const estradaStructureTableEventListeners = {
    /** when the structureManager has new structures, add them to the table */
    "estrada.structure.assetMetaDataAdded": (data, table, pendingStructures) => {
        // structures is a keyed object
        const structures = data.detail.assets;

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
    "estrada.structure.assetMetaDataUpdated": (data, table) => eventTableAssetMetaDataUpdated(data, table),
    "estrada.structure.filter.applied": (data, table, pendingRows, idWhitelistMap) => eventFilterApplied(data, table, pendingRows, idWhitelistMap),
    "estrada.structure.sideMenu.viewChanged": (data, table) => eventSideMenuViewChanged(data, table),
    "estrada.structureTable.rowSelected": (data, table) => eventTableRowSelected(data, table),
};

// Common event handling functionality
/* These are the general events that the main tables will respond to
 *
 * Note that the passed in values 'pendingRoads' / 'pendingStructures' and 'idWhiteListMap'
 * are carefully updated (as opposed to simply reassigned).
 * This ensures that their 'update' is visible to the 'outside'.
 */

function eventTableAssetMetaDataUpdated(data, table) {
    const asset = data.detail.asset;
    table.row('#' + asset.id).data(asset).draw();
}

/** When a filter is applied, update the filter id whitelist */
function eventFilterApplied(data, table, pendingRows, idWhitelistMap) {
    Object.keys(idWhitelistMap).forEach((key) => { idWhitelistMap[key] = undefined; });

    const idMap = data.detail.idMap;
    Object.keys(idMap).forEach((key) => { idWhitelistMap[key] = idMap[key]; });

    table.draw();
}

/** When the view changes adjust the table rows */
function eventSideMenuViewChanged(data, table) {
    const viewName = data.detail ? data.detail.viewName : null;
    if (viewName && viewName.indexOf('table') !== -1) {
        const tableRows = (viewName === 'table') ? 20 : 10;
        table.page.len(tableRows).draw('page');
    }
}

/** Select a row in the table by id */
function eventTableRowSelected(data, table) {
    const rowId = data.detail ? data.detail.rowId : null;
    if (rowId) {
        const assetType = data.detail.assetType;

        table.rows().every(function (rowIdx, tableLoop, rowLoop) {
            if (assetType !== currentFilter.assetType || this.id() !== rowId) {
                this.node().classList.remove("selected");
            } else {
                this.node().classList.add("selected");
                table.row(this.index()).show().draw(false);
            }
        });
    }
}

/** Defines the columns for the table on the Estrada main page */
export const estradaTableColumns = [
    {
        // data-column="0"
        title: EstradaRoad.getFieldName("road_code"),
        data: "code",
        defaultContent: "",
        type: "roadCode",
    },
    {
        // data-column="1"
        title: EstradaRoad.getFieldName("road_name"),
        data: "name",
        defaultContent: "",
    },
    {
        // data-column="2"
        title: EstradaRoad.getFieldName("asset_class") || window.gettext("Asset Class"),
        data: "assetClass",
        defaultContent: "",
    },
    {
        // data-column="3"
        title: EstradaRoad.getFieldName("technical_class"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("technical_class", r),
        visible: false,
        orderable: false,
    },
    {
        // data-column="4"
        title: EstradaRoad.getFieldName("core"),
        data: "core",
        defaultContent: "",
        visible: false,
    },
    {
        // data-column="5"
        title: EstradaRoad.getFieldName("link_code"),
        data: "linkCode",
        defaultContent: "",
    },
    {
        // data-column="6"
        title: window.gettext("Link Name"),
        data: "linkName",
        defaultContent: "",
        visible: false,
    },
    {
        // data-column="7"
        title: EstradaRoad.getFieldName("link_length"),
        data: "linkLength",
        defaultContent: "",
        className: "text-right",
        render: (data, type) => numberTemplate(data, type, 2, ""),
    },
    {
        // data-column="8"
        title: EstradaRoad.getFieldName("administrative_area"),
        data: "administrativeArea",
        defaultContent: "",
    },
    {
        // data-column="9"
        title: EstradaRoad.getFieldName("link_start_name"),
        data: "linkStartName",
        defaultContent: "",
    },
    {
        // data-column="10"
        title: EstradaRoad.getFieldName("link_start_chainage"),
        data: "linkStartChainage",
        defaultContent: "",
        className: "text-right",
        render: (data, type) => {
            return (type === 'display') ? toChainageFormat(data) : data;
        },
    },
    {
        // data-column="11"
        title: window.gettext("Start Point (DMS)"),
        data: "startDMS",
        defaultContent: "",
        visible: false,
    },
    {
        // data-column="12"
        title: window.gettext("Start Point (UTM)"),
        data: "startUTM",
        defaultContent: "",
        visible: false,
    },
    {
        // data-column="13"
        title: EstradaRoad.getFieldName("link_end_name"),
        data: "linkEndName",
        defaultContent: "",
    },
    {
        // data-column="14"
        title: EstradaRoad.getFieldName("link_end_chainage"),
        data: "linkEndChainage",
        defaultContent: "",
        className: "text-right",
        render: (data, type) => {
            return (type === 'display') ? toChainageFormat(data) : data;
        },
    },
    {
        // data-column="15"
        title: window.gettext("End Point (DMS)"),
        data: "endDMS",
        defaultContent: "",
        visible: false,
    },
    {
        // data-column="16"
        title: window.gettext("End Point (UTM)"),
        data: "endUTM",
        defaultContent: "",
        visible: false,
    },
    {
        // data-column="17"
        title: EstradaRoad.getFieldName("surface_type"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("surface_type", r),
        orderable: false,
    },
    {
        // data-column="18"
        title: EstradaRoad.getFieldName("pavement_class"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("pavement_class", r),
        orderable: false,
    },
    {
        // data-column="19"
        title: EstradaRoad.getFieldName("carriageway_width"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("carriageway_width", r),
        orderable: false,
    },
    {
        // note: `total_width` is NOT actually part of EstradaRoad,
        // but EstradaRoad.getFieldName explicitly supports it
        // data-column="20"
        title: EstradaRoad.getFieldName("total_width"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("total_width", r),
        orderable: false,
        visible: false,
    },
    {
        // data-column="21"
        title: EstradaRoad.getFieldName("number_lanes"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("number_lanes", r),
        visible: false,
        orderable: false,
    },
    {
        // data-column="22"
        title: window.gettext("Rainfall"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("rainfall_maximum", r, "Max. Rainfall"),
        visible: false,
        orderable: false,
    },
    {
        // data-column="23"
        title: EstradaRoad.getFieldName("terrain_class"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("terrain_class", r),
        visible: false,
        orderable: false,
    },
    {
        // data-column="24"
        title: window.gettext("Inventory Photos/Videos"),
        data: null,
        defaultContent: "",
        render: (r) => r.inventoryMedia.length ? buttonSegmentsTemplate("inventory_media", r, "Photos/Videos") : "",
        className: "text-center",
        visible: false,
        orderable: false,
    },
    {
        // data-column="25"
        title: EstradaRoad.getFieldName("population"),
        data: "population",
        defaultContent: "",
        visible: false,
        render: (data, type) => numberTemplate(data, type, 0, ""),
    },
    {
        // data-column="26"
        title: window.gettext("Roughness (IRI)"),
        data: "",
        defaultContent: "",
        visible: false,
    },
    {
        // data-column="27"
        title: EstradaRoad.getFieldName("asset_condition"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("asset_condition", r),
        orderable: false,
    },
    {
        // data-column="28"
        title: EstradaRoad.getFieldName("maintenance_need"),
        data: "maintenanceNeed",
        defaultContent: "",
        visible: false,
    },
    {
        // data-column="29"
        title: window.gettext("Traffic data"),
        data: null,
        defaultContent: "",
        render: r => buttonSegmentsTemplate("traffic_level", r),
        visible: false,
    },
    {
        // data-column="30"
        title: EstradaRoad.getFieldName("road_status"),
        data: "status",
        defaultContent: "",
        visible: false,
    },
    {
        // data-column="31"
        title: EstradaRoad.getFieldName("construction_year"),
        data: "constructionYear",
        defaultContent: "",
        visible: false,
        render: (data, type) => numberTemplate(data, type, 0, "", false),
    },
    {
        // data-column="32"
        title: EstradaRoad.getFieldName("funding_source"),
        data: "fundingSource",
        defaultContent: "",
        visible: false
    },
    {
        // data-column="33"
        title: EstradaRoad.getFieldName("project"),
        data: "project",
        defaultContent: "",
        visible: false,
    },
];

/** Defines the columns for the Structures table on the Estrada main page
 * In many cases Bridge, Culvert and Drift use the same field names and are interchangeable
 *
 * For those that don't we'll use the simpler title
 */
export const structuresTableColumns = [
    {
        title: window.gettext("Structure"),
        render: s => getStructureTypeName(detectStructure(s)),
        data: null,
    },
    {
        title: EstradaBridge.getFieldName("structure_code"),
        data: "code",
        type: "structureCode",
        defaultContent: "",
    },
    {
        title: EstradaBridge.getFieldName("structure_name"),
        data: "structureName",
        defaultContent: window.gettext("unknown"),
    },
    {
        title: EstradaBridge.getFieldName("river_name"),
        data: "riverName",
        defaultContent: "N/A",
        visible: false,
    },
    {
        title: EstradaBridge.getFieldName("road_code"),
        data: "roadCode",
        defaultContent: "",
    },
    {
        title: EstradaBridge.getFieldName("asset_class"),
        data: "assetClass",
        defaultContent: "",
        visible: false,
    },
    {
        title: window.gettext("GPS Latitude"),
        data: "dms",
        render: (dms) => { return dms.split(" ")[0] || ""; },
        className: "text-right",
        defaultContent: "-",
        visible: false,
    },
    {
        title: window.gettext("GPS Longitude"),
        data: "dms",
        render: (dms) => { return dms.split(" ")[1] || ""; },
        className: "text-right",
        defaultContent: "-",
        visible: false,
    },
    {
        title: EstradaBridge.getFieldName("chainage"),
        data: "chainage",
        className: "text-right",
        defaultContent: "-",
    },
    {
        title: EstradaBridge.getFieldName("administrative_area"),
        data: "administrativeArea",
        defaultContent: "",
        visible: false,
    },
    {
        // Bridges "Deck Material", Culverts and Drifts "Material"
        // however we show both together
        // so we'll use the simpler title
        title: window.gettext("Material"),
        data: "material",
        defaultContent: "-",
    },
    {
        // Bridges "Bridge Type", Culverts "Culvert Type", Drifts "Drift Type"
        // however we show both together
        // so we'll use the common title "Structure Type"
        title: window.gettext("Structure Type"),
        data: "structureType",
        defaultContent: "-",
    },
    {
        title: EstradaBridge.getFieldName("length"),
        data: "length",
        className: "text-right",
        defaultContent: "",
        render: (data, type) => numberTemplate(data, type, 2, ""),
    },
    {
        title: EstradaBridge.getFieldName("width"),
        data: "width",
        className: "text-right",
        defaultContent: "",
        render: (data, type) => numberTemplate(data, type, 2, ""),
    },
    {
        title: EstradaCulvert.getFieldName("height"),
        data: "height",
        className: "text-right",
        defaultContent: "N/A",
        visible: false,
        render: (data, type) => numberTemplate(data, type, 2, "N/A"),
    },
    {
        title: EstradaDrift.getFieldName("thickness"),
        data: "thickness",
        className: "text-right",
        defaultContent: "N/A",
        visible: false,
        render: (data, type) => numberTemplate(data, type, 2, "N/A"),
    },
    {
        title: EstradaBridge.getFieldName("number_spans"),
        data: "numberSpans",
        className: "text-right",
        defaultContent: "N/A",
        visible: false,
        render: (data, type) => numberTemplate(data, type, 0, "N/A"),
    },
    {
        title: EstradaBridge.getFieldName("span_length"),
        data: "spanLength",
        className: "text-right",
        defaultContent: "N/A",
        visible: false,
        render: (data, type) => numberTemplate(data, type, 2, "N/A"),
    },
    {
        title: EstradaCulvert.getFieldName("number_cells"),
        data: "numberCells",
        className: "text-right",
        defaultContent: "N/A",
        visible: false,
        render: (data, type) => numberTemplate(data, type, 0, "N/A"),
    },
    {
        title: EstradaBridge.getFieldName("protection_upstream"),
        data: "protectionUpstream",
        defaultContent: "",
        visible: false,
    },
    {
        title: EstradaBridge.getFieldName("protection_downstream"),
        data: "protectionDownstream",
        defaultContent: "",
        visible: false,
    },
    {
        title: EstradaBridge.getFieldName("construction_year"),
        data: "constructionYear",
        className: "text-right",
        defaultContent: "",
        visible: false,
        render: (data, type) => numberTemplate(data, type, 0, "", false),
    },
    {
        title: window.gettext("Inventory Photos/Videos"),
        data: null,
        defaultContent: "",
        render: (r) => r.inventoryMedia.length ? buttonSegmentsTemplate("inventory_media", r, "Photos/Videos") : "",
        className: "text-center",
        visible: false,
        orderable: false,
    },
    {
        title: window.gettext("Structure Condition"),
        data: "assetCondition",
        defaultContent: "",
    },
    {
        title: window.gettext("Condition Description"),
        data: "conditionDescription",
        defaultContent: "",
        visible: false,
        className: "clip-text-ellipsis",
    },
    {
        title: window.gettext("Condition Photos/Videos"),
        data: null,
        defaultContent: "",
        render: (r) => r.assetCondition ? buttonSegmentsTemplate("structure_condition_media", r, "Photos/Videos") : "",
        className: "text-center",
        visible: false,
        orderable: false,
    },
];

function detectStructure(structure) {
    const processableId = "-" + structure.id;
    const structureId = processableId.split("-").filter((idPart) => { return idPart; });

    if (structureId.length === 1) {
        structureId.unshift("ROAD");
    }

    return structureId[0];
}

function getStructureTypeName(structureType) {
    const structureTypeToName = {
        "ROAD": "Road",
        "BRDG": "Bridge",
        "CULV": "Culvert",
        "DRFT": "Drift",
        "STRC": "Structure",
    };

    return window.gettext(structureTypeToName[structureType] || structureType);
}

function numberTemplate(data, type, dp = 0, defaultContent = "", toFormat = true) {
    if (type === "display" && data) {
        let value = parseFloat(data).toFixed(dp);
        if (toFormat) value = formatNumber(parseFloat(data).toFixed(dp));
        return data > 0 ? value : defaultContent;
    }
    return data;
}

// function getStructureFieldData(field, structure) { return null; }
function buttonSegmentsTemplate(attrib, asset, fallbackLabel) {
    let getFieldName = (attrib) => (attrib);
    switch (asset.assetType) {
        case "ROAD":
            getFieldName = EstradaRoad.getFieldName;
            break;
        case "BRDG":
            getFieldName = EstradaBridge.getFieldName;
            break;
        case "CULV":
            getFieldName = EstradaCulvert.getFieldName;
            break;
        case "DRFT":
            getFieldName = EstradaDrift.getFieldName;
            break;
        default:
            break;
    }

    // the template is assembled in this way because gettext_collected can't handle
    // real strings "" or '', or angle brackets <> inside template strings ''
    const data_toggle = ' data-toggle="modal"';
    const data_target = ' data-target="#inventory-segments-modal"';
    const data_code = ' data-code="' + asset.code + '"';
    const data_id = ' data-id="' + asset.id + '"';
    const data_attr = ' data-attr="' + attrib + '"';
    const data_type = ' data-type="' + asset.assetType + '"';
    const viewTitle = window.gettext("View") + " " + (window.gettext(fallbackLabel) || getFieldName(attrib));

    return "<a" + data_toggle + data_target + data_code + data_id + data_attr + data_type + ">" + viewTitle + "</a>";
}

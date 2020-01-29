import { toChainageFormat } from "./assets/protoBufUtilities";

/** Defines base columns needed in all segments modal tables **/
const baseSegmentColumns = [
    {
        title: window.gettext("Chainage start"),
        data: "chainageStart",
        defaultContent: "",
        className: "text-right",
        render: (data, type) => {
            return (type === 'display') ? toChainageFormat(data) : data;
        },
    },
    {
        title: window.gettext("Chainage end"),
        data: "chainageEnd",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data, type) => {
            return (type === 'display') ? toChainageFormat(data) : data;
        },
    },
];


/** Defines base columns needed in all details modal tables **/
const baseDetailColumns = [
    {
        title: window.gettext("Chainage"),
        data: "chainage",
        defaultContent: "",
        className: "text-right",
        render: (data, type) => {
            return (type === 'display') ? toChainageFormat(data) : data;
        },
    },
];

/** Defines the columns for the Surface Condition segments table on the inventory page */
export const surfaceConditionColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Surface condition"),
        data: "surfaceCondition",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Surface Type segments table on the inventory page */
export const surfaceTypeColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Surface Type"),
        data: "surfaceType",
        defaultContent: "",
        orderable: false,
    }
]);

/** Defines the columns for the Technical Class segments table on the inventory page */
export const technicalClassColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Technical class"),
        data: "technicalClass",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Number of Lanes segments table on the inventory page */
export const numberLanesColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Number of lanes"),
        data: "numberLanes",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Carriageway Width segments table on the inventory page */
export const carriagewayWidthColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Carriageway width"),
        data: "carriagewayWidth",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Rainfall segments table on the inventory page */
export const rainfallColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Rainfall"),
        data: "rainfall",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Terrain Class segments table on the inventory page */
export const terrainClassColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Terrain class"),
        data: "terrainClass",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Terrain Class segments table on the inventory page */
export const pavementClassColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Pavement class"),
        data: "pavementClass",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Condition Description details table on the inventory page */
export const conditionDescriptionColumns = baseDetailColumns.concat([
    {
        title: window.gettext("Condition description"),
        data: "conditionDescription",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Inventory Photos details table on the inventory page */
export const inventoryPhotosColumns = baseDetailColumns.concat([
    {
        title: window.gettext("Inventory photos"),
        data: "inventoryPhotos", // This should probably be a link to the document/photo
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Condition Description details table on the inventory page */
export const structureConditionColumns = baseDetailColumns.concat([
    {
        title: window.gettext("Structure condition"),
        data: "structureCondition",
        defaultContent: "",
        orderable: false,
    },
]);

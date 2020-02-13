import { choice_or_default, toChainageFormat } from "./assets/protoBufUtilities";
import {ASSET_CONDITION_CHOICES} from "./assets/models/estradaBase";

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
        title: window.gettext("Survey date"),
        data: "dateSurveyed",
        defaultContent: "",
        className: "text-center",
        orderable: false,
    },
];

/** Defines the columns for the Surface (Asset) Condition segments table on the inventory page */
export const surfaceConditionColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Surface condition"),
        data: "assetCondition",
        defaultContent: "",
        orderable: false,
    },
]);

export const surfaceTypeColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Surface Type"),
        data: "surfaceType",
        defaultContent: "",
        orderable: false,
    }
]);

export const technicalClassColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Technical class"),
        data: "technicalClass",
        defaultContent: "",
        orderable: false,
    },
]);

export const numberLanesColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Number of lanes"),
        data: "numberLanes",
        defaultContent: "",
        orderable: false,
    },
]);

export const carriagewayWidthColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Carriageway width"),
        data: "carriagewayWidth",
        defaultContent: "",
        orderable: false,
    },
]);

export const rainfallColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Rainfall"),
        data: "rainfall",
        defaultContent: "",
        orderable: false,
    },
]);

export const terrainClassColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Terrain class"),
        data: "terrainClass",
        defaultContent: "",
        orderable: false,
    },
]);

export const pavementClassColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Pavement class"),
        data: "pavementClass",
        defaultContent: "",
        orderable: false,
    },
]);

// export const structurePhotosColumns = baseDetailColumns.concat([
//     {
//         title: window.gettext("Inventory photos"),
//         data: "structurePhotos", // This should probably be a link to the document/photo
//         defaultContent: "",
//         orderable: false,
//     },
// ]);

/** Defines the columns for the Structure (Asset) Condition segments table on the inventory page */
export const structureConditionColumns = baseDetailColumns.concat([
    {
        title: window.gettext("Structure condition"),
        data: "assetCondition",
        defaultContent: "",
        className: "text-center",
        orderable: false,
        render: (data, type) => {
            return (type === 'display') ? choice_or_default(data, ASSET_CONDITION_CHOICES) : data;
        },
    },
]);

export const structureConditionDescriptionColumns = baseDetailColumns.concat([
    {
        title: window.gettext("Condition description"),
        data: "conditionDescription",
        defaultContent: "",
        orderable: false,
    },
]);

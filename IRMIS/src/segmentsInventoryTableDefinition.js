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

/**
 * Defines the additional columns for the various segments/details
 * attributes modals, found on the inventory page
 * */
export const surfaceConditionColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Surface condition"),
        data: "surfaceCondition",
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

export const structurePhotosColumns = baseDetailColumns.concat([
    {
        title: window.gettext("Inventory photos"),
        data: "structurePhotos", // This should probably be a link to the document/photo
        defaultContent: "",
        orderable: false,
    },
]);

export const structureConditionColumns = baseDetailColumns.concat([
    {
        title: window.gettext("Structure condition"),
        data: "structureCondition",
        defaultContent: "",
        orderable: false,
    },
]);

export const structureConditionDescriptionColumns = baseDetailColumns.concat([
    {
        title: window.gettext("Structure condition description"),
        data: "conditionDescription",
        defaultContent: "",
        orderable: false,
    },
]);

/** SPECIAL SNOWFAKE: Defines all of the columns needed for the TRAFFIC LEVEL inventory modal table **/
export const trafficLevelColumns = [
    {
        title: window.gettext("Survey date"),
        data: "values",
        defaultContent: "",
        className: "text-center",
        render: (data) => {
            if (data.forcastYear) { return data.forcastYear; }
            else { return data.surveyFromDate + " - " + data.surveyToDate; }
        },
    },
    {
        title: window.gettext("Traffic type"),
        data: "",
        defaultContent: "HEHEHE",
        className: "text-center",
        render: (data) => { return data.trafficType; },
    },
    {
        title: window.gettext("Total vehicles"),
        data: "",
        defaultContent: "9999",
        className: "text-center",
        render: (data) => { return data.countTotal; },
    },
];

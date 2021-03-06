import { toChainageFormat } from "./assets/protoBufUtilities";
import { formatNumber } from "./assets/utilities";

/** Defines base columns needed in all segments modal tables **/
const baseSegmentColumns = [
    {
        title: window.gettext("Chainage start"),
        data: "chainageStart",
        defaultContent: "",
        className: "text-right",
        render: (data, type) => {
            return (type === "display" && typeof data === "number") ? toChainageFormat(data) : data;
        },
    },
    {
        title: window.gettext("Chainage end"),
        data: "chainageEnd",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data, type) => {
            return (type === "display" && typeof data === "number") ? toChainageFormat(data) : data;
        },
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
    {
        title: window.gettext("Photos/Videos"),
        data: "media",
        defaultContent: "",
        className: "text-center",
        orderable: false,
        render: (media) => {
            let links = [];
            media.forEach((m, i) => {
                links.push(`<div><a class="image" href="${m.url}" target="_blank">Photo/Video ${i + 1}</a></div>`);
            });
            return links.join(" ");
        },
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
        render: (data, type) => {
            return (type === "display" && typeof data === "number") ? formatNumber(data.toFixed(0)) : data;
        },
    },
]);

export const carriagewayWidthColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Carriageway width (m)"),
        data: "carriagewayWidth",
        defaultContent: "",
        orderable: false,
        render: (data, type) => {
            return (type === "display" && typeof data === "number") ? formatNumber(data.toFixed(1)) : data;
        },
    },
]);

export const totalWidthColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Total width (m)"),
        data: "totalWidth",
        defaultContent: "",
        orderable: false,
        render: (data, type) => {
            return (type === "display" && typeof data === "number") ? formatNumber(data.toFixed(1)) : data;
        },
    },
]);

export const rainfallColumns = baseSegmentColumns.concat([
    {
        title: window.gettext("Max. Rainfall (mm)"),
        data: "value",
        defaultContent: "",
        orderable: false,
        render: (data, type) => {
            return (data == "") ? window.gettext("Unknown") : formatNumber(data);
        },
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

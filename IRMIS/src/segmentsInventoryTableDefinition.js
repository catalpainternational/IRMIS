import { toChainageFormat } from "./assets/protoBufUtilities";

/** Defines base columns needed in all segments modal tables **/
const baseColumns = [
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

/** Defines the columns for the Surface Condition segments table on the inventory page */
export const surfaceConditionColumns = baseColumns.concat([
    {
        title: window.gettext("Surface condition"),
        data: "surfaceCondition",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Surface Type segments table on the inventory page */
export const surfaceTypeColumns = baseColumns.concat([
    {
        title: window.gettext("Surface Type"),
        data: "surfaceType",
        defaultContent: "",
        orderable: false,
    }
]);

/** Defines the columns for the Technical Class segments table on the inventory page */
export const technicalClassColumns = baseColumns.concat([
    {
        title: window.gettext("Technical class"),
        data: "technicalClass",
        defaultContent: "",
        orderable: false,
    },
]);

/** Defines the columns for the Number of Lanes segments table on the inventory page */
export const numberLanesColumns = baseColumns.concat([
    {
        title: window.gettext("Number of lanes"),
        data: "numberLanes",
        defaultContent: "",
        orderable: false,
    },
]);

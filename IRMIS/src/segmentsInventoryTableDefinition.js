import { toChainageFormat } from "./assets/protoBufUtilities";

/** Defines the columns for the surface condition segments table on the inventory page */
export const surfaceConditionColumns = [
    {
        title: window.gettext("Chainage start"), 
        data: "chainageStart",
        defaultContent: "",
        className: "text-right",
        render: (data, type) => {
            if (type === 'display') return toChainageFormat(data);
            return data;
        },
    },
    {
        title: window.gettext("Chainage end"), 
        data: "chainageEnd",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data, type) => {
            if (type === 'display') return toChainageFormat(data);
        },
    },
    {
        title: window.gettext("Surface condition"), 
        data: "surfaceCondition",
        defaultContent: "",
        orderable: false,
    },
];

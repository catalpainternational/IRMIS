import { toChainageFormat } from "./assets/protoBufUtilities";
import { getRoadReports } from "./assets/reportsAPI";

export function getRoadReport(filters) {
    return Promise.resolve(getRoadReports(filters))
        .then((surveyReportList) => { return surveyReportList; });
}

/** The various columns shared between the different reports */
export const reportColumns = {
    title: {
        // Title needs to be set per data type
        title: window.gettext("Title"),
        data: "title",
        defaultContent: "",
        orderable: false,
    },
    distance: {
        title: window.gettext("Length (km)"),
        data: "distance",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data, type) => {
            return (type === "display")
                ? (data / 1000).toFixed(2)
                : data;
        },
    },
    percent: {
        title: window.gettext("Percentages (%)"),
        data: "percent",
        defaultContent: "",
        className: "text-right",
        orderable: false,
    },
    chainageStart: {
        title: window.gettext("Chainage Start"),
        data: "chainageStart",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data, type) => {
            return (type === "display") ? toChainageFormat(data) : data;
        },
    },
    chainageEnd: {
        title: window.gettext("Chainage End"),
        data: "chainageEnd",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data, type) => {
            return (type === "display") ? toChainageFormat(data) : data;
        },
    },
    municipality: {
        title: window.gettext("Municipality"),
        data: "municipality",
        defaultContent: "",
        orderable: false,
    },
    assetClass: {
        title: window.gettext("Asset Class"),
        data: "assetClass",
        defaultContent: "",
        orderable: false,
    },
    assetCondition: {
        title: window.gettext("Surface Condition (SDI)"),
        data: "assetCondition",
        defaultContent: "",
        orderable: false,
    },
    surfaceType: {
        title: window.gettext("Surface Type"),
        data: "surfaceType",
        defaultContent: "",
        orderable: false,
    },
    surveyDate: {
        title: window.gettext("Survey Date"),
        data: "dateSurveyed",
        defaultContent: "",
        orderable: false,
    },
};

/** The names given to the dataTables used in the reports */
export const reportTableIds = {
    municipality: "report-municipality-table",
    assetClass: "report-asset-class-table",
    surfaceType: "report-surface-type-table",
    roadStatus: "report-road-status-table",
    technicalClass: "report-technical-class-table",
    assetCondition: "report-asset-condition-table",
};

/** The names of the stacked bars used in the reports */
export const reportBarIds = {
    assetClass: "report-asset-class-bar",
    roadStatus: "report-road-status-bar",
    technicalClass: "report-technical-class-bar",
    assetCondition: "report-asset-condition-bar",
    pavementClass: "report-pavement-class-bar",
};

/** The definitions of the different reports
 * Note:
 * - fixedFilters uses snake_case for various field names
 * this excludes 'primaryattribute' and 'secondaryattribute' because they are not field names
 * within report.riot.html it also excludes several fields that a heavily verified/manipulated as filters
 * - visibleFilters uses camelCase for various html id names within report.riot.html
*/
export const reportContent = {
    1: {
        title: window.gettext("Road Network Length"),
        description: window.gettext("A report on the total length of the road network. The report provides total length in kilometers and percentages according to Road Status and Technical Class. A number of filters can be selected in order to generate a length report according to the required criteria"),
        noReportTitle: window.gettext("Click on Create Report button to access the Road Network Length report"),
        noReportDescription: window.gettext("The report will be shown in this area and will provide you with detailed Road Network Length information. You can use filters to generate a customized report"),
        noReportData: window.gettext("Sorry, data for the road network is not available yet"),
        fixedFilter: {
            primaryattribute: ["road_status", "technical_class"],
        },
        visibleFilters: {
            municipality: true,
            assetClass: true,
            surfaceType: true,
            assetCondition: true,
            reportDate: true,
        },
        reportElements: { filters: true, totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    2: {
        title: window.gettext("Road Network Length Breakdown"),
        description: window.gettext("A breakdown report on the total length of the road network. The report provides information on total length in kilometers and percentages as well as Road Status and Technical Class, according to a breakdown by Municipality, Road Class and Surface Type"),
        noReportTitle: window.gettext("Click on Create Report button to access the Road Network Length Breakdown report"),
        noReportDescription: window.gettext("The report will be shown in this area and will provide you with detailed Road Network Length Breakdown information. You can use filters to generate a customized report"),
        noReportData: window.gettext("Sorry, data for the road network is not available yet"),
        fixedFilter: {
            primaryattribute: ["municipality", "asset_class", "surface_type"],
            secondaryattribute: {
                "municipality": ["road_status", "technical_class"],
                "asset_class": ["road_status", "technical_class"],
                "surface_type": ["road_status", "technical_class"],
            },
        },
        visibleFilters: {
            // municipality: true,
            // assetClass: true,
            // surfaceType: true,
            // assetCondition: true,
            reportDate: true,
        },
        reportElements: { filters: true, totalLength: true, dataTables: [reportTableIds.municipality, reportTableIds.assetClass, reportTableIds.surfaceType] },
    },
    3: {
        title: window.gettext("Surface Condition"),
        description: window.gettext("A report on Road Surface Condition. This report provides detailed Surface Condition information per segment"),
        noReportTitle: window.gettext("Please select a road above to view Surface Condition reports"),
        noReportDescription: window.gettext("The report will be shown in this area and will provide you with detailed Surface Condition information per segment of the selected road"),
        noReportData: window.gettext("Sorry, Surface Condition data is not available for the selected road"),
        fixedFilter: {
            primaryattribute: ["asset_condition"],
        },
        visibleFilters: {
            roadCode: true,
            reportDate: true,
        },
        reportElements: { roadCodeAndChainage: true, stackedBars: [reportBarIds.assetCondition], dataTables: [reportTableIds.assetCondition] },
    },
    4: {
        title: window.gettext("IRI Roughness"),
        description: window.gettext("A report on Road IRI data. This report provides detailed information on a Road's Roughness per segment"),
        noReportTitle: window.gettext("Please select a road above to view IRI Roughness reports"),
        noReportDescription: window.gettext("The report will be shown in this area and will provide you with detailed IRI Roughness information per segment of the selected road"),
        noReportData: window.gettext("Sorry, IRI Roughness data is not available for the selected road"),
        fixedFilter: {},
        visibleFilters: {
            roadCode: true,
            reportDate: true,
        },
        reportElements: { roadCodeAndChainage: true },
    },
    5: {
        title: window.gettext("Road Network Length - National Class"),
        description: window.gettext("A report on the total length of National Class roads. The report provides total length in kilometers and percentages according to Road Status and Technical Class for National Roads"),
        noReportTitle: window.gettext("Click on Create Report button to access the Road Network Length report for National roads"),
        noReportDescription: window.gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for National class roads"),
        noReportData: window.gettext("Sorry, data for National Class roads is not available yet"),
        fixedFilter: {
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "NAT",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    6: {
        title: window.gettext("Road Network Length - Municipal Class"),
        description: window.gettext("A report on the total length of Municipal Class roads. The report provides total length in kilometers and percentages according to Road Status and Technical Class for Municipal Roads"),
        noReportTitle: window.gettext("Click on Create Report button to access the Road Network Length report for Municipal roads"),
        noReportDescription: window.gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for Municipal class roads"),
        noReportData: window.gettext("Sorry, data for Municipal Class roads is not available yet"),
        fixedFilter: {
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "MUN",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    7: {
        title: window.gettext("Road Network Length - Rural Class"),
        description: window.gettext("A report on the total length of Rural Class roads. The report provides total length in kilometers and percentages according to Road Status and Technical Class for Rural Roads"),
        noReportTitle: window.gettext("Click on Create Report button to access the Road Network Length report for Rural roads"),
        noReportDescription: window.gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for Rural class roads"),
        noReportData: window.gettext("Sorry, data for Rural Class roads is not available yet"),
        fixedFilter: {
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "RUR",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    8: {
        title: window.gettext("Road Network Length - Highway Class"),
        description: window.gettext("A report on the total length of Highways. The report provides total length in kilometers and percentages according to Road Status and Technical Class for Highways"),
        noReportTitle: window.gettext("Click on Create Report button to access the Road Network Length report for Highways"),
        noReportDescription: window.gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for Highway class roads"),
        noReportData: window.gettext("Sorry, data for Highway Class roads is not available yet"),
        fixedFilter: {
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "HIGH",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    9: {
        title: window.gettext("Road Network Length - Urban Class"),
        description: window.gettext("A report on the total length of Urban Class roads. The report provides total length in kilometers and percentages according to Road Status and Technical Class for Urban Roads"),
        noReportTitle: window.gettext("Click on Create Report button to access the Road Network Length report for Urban roads"),
        noReportDescription: window.gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for Urban class roads"),
        noReportData: window.gettext("Sorry, data for Urban Class roads is not available yet"),
        fixedFilter: {
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "URB",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
};

import { toChainageFormat } from "./assets/protoBufUtilities";

// tslint:disable: object-literal-sort-keys

/** The list of sections for the different types of asset reports */
export const reportAssetsSections: { [name: string]: string }[] = [
    { section: "network", title: (window as any).gettext("Road Network Report") },
    { section: "condition", title: (window as any).gettext("Road Condition Report") },
    { section: "roadClass", title: (window as any).gettext("Road Network Reports by Road Class") },
    { section: "structures", title: (window as any).gettext("Structures Reports") },
];

/** assetReports.id matches the definitions in reportAssetsContent below */
export const assetReports: { [name: string]: number | string }[] = [
    { id: 1, section: "network", title: (window as any).gettext("Road Network Length") },
    { id: 2, section: "network", title: (window as any).gettext("Road Network Length Breakdown") },
    { id: 3, section: "condition", title: (window as any).gettext("Surface Condition (SDI)") },
    { id: 4, section: "condition", title: (window as any).gettext("IRI Roughness") },
    { id: 5, section: "roadClass", title: (window as any).gettext("Road Network Length - National Class") },
    { id: 6, section: "roadClass", title: (window as any).gettext("Road Network Length - Municipal Class") },
    { id: 7, section: "roadClass", title: (window as any).gettext("Road Network Length - Rural Class") },
    { id: 8, section: "roadClass", title: (window as any).gettext("Road Network Length - Highway Class") },
    { id: 9, section: "roadClass", title: (window as any).gettext("Road Network Length - Urban Class") },
    { id: 10, section: "structures", title: (window as any).gettext("Structures Overview Report") },
    { id: 11, section: "structures", title: (window as any).gettext("Structures Condition Report") },
];

/** The names given to the dataTables used in the asset reports */
export const reportTableIds: { [name: string]: string } = {
    municipality: "report-municipality-table",
    assetClass: "report-asset-class-table",
    surfaceType: "report-surface-type-table",
    roadStatus: "report-road-status-table",
    technicalClass: "report-technical-class-table",
    assetCondition: "report-asset-condition-table",
    assetRoughness: "report-asset-roughness-table",
    structureForm: "report-structure-form-table",
    structureClass: "report-structure-class-table",
    structureCondition: "report-structure-condition-table",
};

/** The names of the stacked bars used in the asset reports */
export const reportBarIds: { [name: string]: string } = {
    assetClass: "report-asset-class-bar",
    roadStatus: "report-road-status-bar",
    technicalClass: "report-technical-class-bar",
    assetCondition: "report-asset-condition-bar",
    assetRoughnessCondition: "report-roughness-condition-bar",
    pavementClass: "report-pavement-class-bar",
};

/** The various titles given to the dataTables used in the asset reports */
export const reportTitleColumnMapping: { [name: string]: string } = {
    municipality: "Municipality",
    asset_class: "Asset Class",
    asset_type: "Asset Type",
    road_status: "Road Status",
    // road_asset_condition: no title column for (Road) asset condition
    surface_type: "Surface Type",
    technical_class: "Technical Class",
    terrain_class: "Terrain Class",
    structure_asset_condition: "Structure Condition",
};

/** The various columns shared between the different asset reports */
export const reportColumns: { [name: string]: any } = {
    title: {
        // Title needs to be set per data type
        title: (window as any).gettext("Title"),
        data: "title",
        defaultContent: "",
        orderable: false,
    },
    distance: {
        title: (window as any).gettext("Length (km)"),
        data: "distance",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data: any, type: string) => {
            return (type === "display")
                ? (data / 1000).toFixed(2)
                : data;
        },
    },
    count: {
        title: (window as any).gettext("Total"),
        data: "distance",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data: any, type: string) => {
            return (type === "display")
                ? data.toFixed(0)
                : data;
        },
    },
    number: {
        title: (window as any).gettext("Number of structures"),
        data: "distance",
        defaultContent: "",
        className: "text-right",
        orderable: false,
    },
    percent: {
        title: (window as any).gettext("Percentages (%)"),
        data: "percent",
        defaultContent: "",
        className: "text-right",
        orderable: false,
    },
    chainageStart: {
        title: (window as any).gettext("Chainage Start"),
        data: "chainageStart",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data: any, type: string) => {
            return (type === "display") ? toChainageFormat(data) : data;
        },
    },
    chainageEnd: {
        title: (window as any).gettext("Chainage End"),
        data: "chainageEnd",
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data: any, type: string) => {
            return (type === "display") ? toChainageFormat(data) : data;
        },
    },
    municipality: {
        title: (window as any).gettext("Municipality"),
        data: "municipality",
        defaultContent: "",
        orderable: false,
    },
    assetClass: {
        title: (window as any).gettext("Asset Class"),
        data: "assetClass",
        defaultContent: "",
        orderable: false,
    },
    assetCondition: {
        title: (window as any).gettext("Surface Condition (SDI)"),
        data: "assetCondition",
        defaultContent: "",
        orderable: false,
    },
    roughness: {
        title: (window as any).gettext("Roughness (IRI)"),
        data: "sourceRoughness",
        defaultContent: "",
        orderable: false,
    },
    roughnessCondition: {
        title: (window as any).gettext("Roughness Condition"),
        data: "roughness",
        defaultContent: "",
        orderable: false,
    },
    surfaceType: {
        title: (window as any).gettext("Surface Type"),
        data: "surfaceType",
        defaultContent: "",
        orderable: false,
    },
    surveyDate: {
        title: (window as any).gettext("Survey Date"),
        data: "dateSurveyed",
        defaultContent: "",
        orderable: false,
    },
};

/**
 * These are the default column sets for each report type,
 * they are overriden for any report that specifies fixedFilter.secondaryattribute
 * A column title is usually reset by the columns functions below
 */
export const reportColumnSets: { [name: string]: string[] } = {
    municipality: [reportColumns.title, reportColumns.distance, reportColumns.percent],
    asset_class: [reportColumns.title, reportColumns.distance, reportColumns.percent],
    asset_type: [reportColumns.title, reportColumns.distance, reportColumns.percent],
    road_status: [reportColumns.title, reportColumns.distance, reportColumns.percent],
    asset_condition: [
        reportColumns.chainageStart, reportColumns.chainageEnd,
        reportColumns.assetCondition, reportColumns.surveyDate,
    ],
    road_asset_condition: [
        reportColumns.chainageStart, reportColumns.chainageEnd,
        reportColumns.assetCondition, reportColumns.surveyDate,
    ],
    asset_roughness: [
        reportColumns.chainageStart, reportColumns.chainageEnd,
        reportColumns.roughness, reportColumns.roughnessCondition,
        reportColumns.surveyDate,
    ],
    surface_type: [reportColumns.title, reportColumns.distance, reportColumns.percent],
    technical_class: [reportColumns.title, reportColumns.distance, reportColumns.percent],
    terrain_class: [reportColumns.title, reportColumns.distance, reportColumns.percent],
    structure_asset_condition: [reportColumns.title, reportColumns.count, reportColumns.percent],
    structure_asset_class: [reportColumns.title, reportColumns.number, reportColumns.percent],
};

/** The definitions of the different asset reports
 * Note:
 * - fixedFilters uses snake_case for various field names
 * this excludes 'reportassettype', 'primaryattribute' and 'secondaryattribute' because they are not field names
 * within report_assets.riot.html it also excludes several fields that a heavily verified/manipulated as filters
 * - visibleFilters uses camelCase for various html id names within report.riot.html
 */
export const reportAssetsContent: { [name: string]: any } = {
    1: {
        title: (window as any).gettext("Road Network Length"),
        description: (window as any).gettext("A report on the total length of the road network. The report provides total length in kilometers and percentages according to Road Status and Technical Class. A number of filters can be selected in order to generate a length report according to the required criteria"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the Road Network Length report"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Road Network Length information. You can use filters to generate a customized report"),
        noReportData: (window as any).gettext("Sorry, data for the road network is not available yet"),
        fixedFilter: {
            reportassettype: ["ROAD"],
            primaryattribute: ["road_status", "technical_class"],
        },
        visibleFilters: {
            municipality: true,
            assetClass: true,
            surfaceType: true,
            assetCondition: true,
            reportDate: true,
        },
        reportElements: {
            filters: true,
            totalLength: true,
            dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass],
        },
    },
    2: {
        title: (window as any).gettext("Road Network Length Breakdown"),
        description: (window as any).gettext("A breakdown report on the total length of the road network. The report provides information on total length in kilometers and percentages as well as Road Status and Technical Class, according to a breakdown by Municipality, Road Class and Surface Type"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the Road Network Length Breakdown report"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Road Network Length Breakdown information. You can use filters to generate a customized report"),
        noReportData: (window as any).gettext("Sorry, data for the road network is not available yet"),
        fixedFilter: {
            reportassettype: ["ROAD"],
            primaryattribute: ["municipality", "asset_class", "surface_type"],
            secondaryattribute: {
                municipality: ["road_status", "technical_class"],
                asset_class: ["road_status", "technical_class"],
                surface_type: ["road_status", "technical_class"],
            },
        },
        visibleFilters: {
            // municipality: true,
            // assetClass: true,
            // surfaceType: true,
            // assetCondition: true,
            reportDate: true,
        },
        reportElements: {
            filters: true,
            totalLength: true,
            dataTables: [reportTableIds.municipality,
            reportTableIds.assetClass, reportTableIds.surfaceType],
        },
    },
    3: {
        title: (window as any).gettext("Surface Condition"),
        description: (window as any).gettext("A report on Road Surface Condition. This report provides detailed Surface Condition information per segment"),
        noReportTitle: (window as any).gettext("Please select a road above to view Surface Condition reports"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Surface Condition information per segment of the selected road"),
        noReportData: (window as any).gettext("Sorry, Surface Condition data is not available for the selected road"),
        fixedFilter: {
            reportassettype: ["ROAD"],
            primaryattribute: ["asset_condition"],
        },
        visibleFilters: {
            roadCode: true,
            reportDate: true,
        },
        reportElements: {
            roadCodeAndChainage: true,
            stackedBars: [reportBarIds.assetCondition],
            dataTables: [reportTableIds.assetCondition],
        },
    },
    4: {
        title: (window as any).gettext("IRI Roughness"),
        description: (window as any).gettext("A report on Road IRI data. This report provides detailed information on a Road's Roughness per segment"),
        noReportTitle: (window as any).gettext("Please select a road above to view IRI Roughness reports"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed IRI Roughness information per segment of the selected road"),
        noReportData: (window as any).gettext("Sorry, IRI Roughness data is not available for the selected road"),
        fixedFilter: {
            reportassettype: ["ROAD"],
            primaryattribute: ["source_roughness", "roughness"],
        },
        visibleFilters: {
            roadCode: true,
            reportDate: true,
        },
        reportElements: {
            filters: true,
            roadCodeAndChainage: true,
            stackedBars: [reportBarIds.assetRoughnessCondition],
            dataTables: [reportTableIds.assetRoughness],
        },
    },
    5: {
        title: (window as any).gettext("Road Network Length - National Class"),
        description: (window as any).gettext("A report on the total length of National Class roads. The report provides total length in kilometers and percentages according to Road Status and Technical Class for National Roads"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the Road Network Length report for National roads"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for National class roads"),
        noReportData: (window as any).gettext("Sorry, data for National Class roads is not available yet"),
        fixedFilter: {
            reportassettype: ["ROAD"],
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "NAT",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    6: {
        title: (window as any).gettext("Road Network Length - Municipal Class"),
        description: (window as any).gettext("A report on the total length of Municipal Class roads. The report provides total length in kilometers and percentages according to Road Status and Technical Class for Municipal Roads"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the Road Network Length report for Municipal roads"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for Municipal class roads"),
        noReportData: (window as any).gettext("Sorry, data for Municipal Class roads is not available yet"),
        fixedFilter: {
            reportassettype: ["ROAD"],
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "MUN",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    7: {
        title: (window as any).gettext("Road Network Length - Rural Class"),
        description: (window as any).gettext("A report on the total length of Rural Class roads. The report provides total length in kilometers and percentages according to Road Status and Technical Class for Rural Roads"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the Road Network Length report for Rural roads"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for Rural class roads"),
        noReportData: (window as any).gettext("Sorry, data for Rural Class roads is not available yet"),
        fixedFilter: {
            reportassettype: ["ROAD"],
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "RUR",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    8: {
        title: (window as any).gettext("Road Network Length - Highway Class"),
        description: (window as any).gettext("A report on the total length of Highways. The report provides total length in kilometers and percentages according to Road Status and Technical Class for Highways"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the Road Network Length report for Highways"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for Highway class roads"),
        noReportData: (window as any).gettext("Sorry, data for Highway Class roads is not available yet"),
        fixedFilter: {
            reportassettype: ["ROAD"],
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "HIGH",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    9: {
        title: (window as any).gettext("Road Network Length - Urban Class"),
        description: (window as any).gettext("A report on the total length of Urban Class roads. The report provides total length in kilometers and percentages according to Road Status and Technical Class for Urban Roads"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the Road Network Length report for Urban roads"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Road Network Length information for Urban class roads"),
        noReportData: (window as any).gettext("Sorry, data for Urban Class roads is not available yet"),
        fixedFilter: {
            reportassettype: ["ROAD"],
            primaryattribute: ["road_status", "technical_class"],
            asset_class: "URB",
        },
        visibleFilters: {
            reportDate: true,
        },
        reportElements: { totalLength: true, dataTables: [reportTableIds.roadStatus, reportTableIds.technicalClass] },
    },
    10: {
        title: (window as any).gettext("Structures"),
        description: (window as any).gettext("A report on Structures data. This report provides detailed Structure totals and percentages according to structure type as well as by structure class"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the Structure Class Report for structures"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Structure Class information for structures"),
        noReportData: (window as any).gettext("Sorry, data for structures is not available yet"),
        fixedFilter: {
            reportassettype: ["BRDG", "CULV", "DRFT"],
            primaryattribute: ["asset_type"],
            secondaryattribute: {
                asset_type: ["asset_class"],
            },
            asset_type: ["BRDG", "CULV", "DRFT"],
        },
        visibleFilters: {
            municipality: true,
            assetCondition: true,
            assetType: true,
        },
        reportElements: {
            filters: true,
            totalCount: true,
            dataTables: [reportTableIds.structureForm, reportTableIds.structureClass],
        },
    },
    11: {
        title: (window as any).gettext("Condition of Structures"),
        description: (window as any).gettext("A report on Structures conditions. This report provides detailed Structure condition information by structure type"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the Structure Condition Report for structures"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed Structure Condition information for structures"),
        noReportData: (window as any).gettext("Sorry, data for structures is not available yet"),
        fixedFilter: {
            reportassettype: ["BRDG", "CULV", "DRFT"],
            primaryattribute: ["asset_type"],
            secondaryattribute: {
                asset_type: ["asset_condition"],
            },
            asset_type: ["BRDG", "CULV", "DRFT"],
        },
        visibleFilters: {
            municipality: true,
            assetType: true,
        },
        reportElements: {
            filters: true,
            totalCount: true,
            dataTables: [reportTableIds.structureCondition],
        },
    },
};

/** IDs of the asset report elements */
export const allAssetReportElements = {
    stackedBars: [
        reportBarIds.roadStatus,
        reportBarIds.technicalClass,
        reportBarIds.assetCondition,
        reportBarIds.assetRoughnessCondition
    ],
    tables: [
        reportTableIds.municipality,
        reportTableIds.assetClass,
        reportTableIds.surfaceType,
        reportTableIds.roadStatus,
        reportTableIds.technicalClass,
        reportTableIds.assetCondition,
        reportTableIds.structureClass,
        reportTableIds.structureForm,
        reportTableIds.structureCondition,
    ],
};

/** The list of sections for the different types of contract reports */
export const reportContractsSections: { [name: string]: string }[] = [
    { section: "contract", title: (window as any).gettext("Contract Reports") },
    { section: "socialSafeguard", title: (window as any).gettext("Social Safeguard Reports") },
];

/** contractReports.id matches the definitions in reportTableDefinitions */
export const contractReports: { [name: string]: number | string }[] = [
    { id: 1, section: "contract", title: (window as any).gettext("Financial and Physical Progress Summary") },
    { id: 2, section: "contract", title: (window as any).gettext("Financial and Physical Progress") },
    { id: 3, section: "contract", title: (window as any).gettext("Completed Contracts") },
    { id: 4, section: "socialSafeguard", title: (window as any).gettext("Social Safeguard") },
    { id: 5, section: "socialSafeguard", title: (window as any).gettext("Contract's Social Safeguard") },
];

/** The names given to the dataTables used in the contract reports */
export const reportContractsTableIds: { [name: string]: string } = {
    program: "report-program-table",
    contractCode: "report-contract-code-table",
    assetClassTypeOfWork: "report-asset-class-type-work-table",
    typeOfWorkYear: "report-type-work-year-table",
    assetClassYear: "report-asset-class-year-table",
    numberEmployees: "report-number-employees-table",
    wages: "report-wages-table",
    workedDays: "report-worked-days-table",
};

/** The various titles given to the dataTables used in the contract reports */
export const reportContractsTitleColumnMapping: { [name: string]: string } = {
    program: (window as any).gettext("Program name"),
    contractCode: (window as any).gettext("Contract code"),
    assetClassTypeOfWork: (window as any).gettext("Asset class"),
    typeOfWorkYear: (window as any).gettext("Type of work"),
    assetClassYear: (window as any).gettext("Asset class"),
    numberEmployees: (window as any).gettext("Number of employees"),
    wages: (window as any).gettext("Wages"),
    workedDays: (window as any).gettext("Worker-days"),
};

/** The various columns shared between the different contract reports */
export const reportContractsTableColumns: { [name: string]: any } = {
    title: {
        title: (window as any).gettext("Title"),
        data: "title",
        defaultContent: "",
        orderable: false,
    },
    programName: {
        title: (window as any).gettext("Program name"),
        data: "programname",
        defaultContent: "",
        orderable: false,
    },
    projectName: {
        title: (window as any).gettext("Project names"),
        data: "projectname",
        defaultContent: "",
        orderable: false,
    },
    typeOfWork: {
        title: (window as any).gettext("Type of work"),
        data: "typeofwork",
        defaultContent: "",
        orderable: false,
    },
    fundingSource: {
        title: (window as any).gettext("Funding source"),
        data: "fundingsource",
        defaultContent: "",
        orderable: false,
    },
    assets: {
        title: (window as any).gettext("Number of assets"),
        data: "assets",
        defaultContent: "",
        orderable: false,
    },
    projects: {
        title: (window as any).gettext("Number of projects"),
        data: "projects",
        defaultContent: "",
        orderable: false,
    },
    contracts: {
        title: (window as any).gettext("Number of contracts"),
        data: "contracts",
        defaultContent: "",
        orderable: false,
    },
    companies: {
        title: (window as any).gettext("Number of companies"),
        data: "companies",
        defaultContent: "",
        orderable: false,
    },
    contractor: {
        title: (window as any).gettext("Contractor"),
        data: "contractor",
        defaultContent: "",
        orderable: false,
    },
    budget: {
        title: (window as any).gettext("Budget current year ($)"),
        data: "budget",
        defaultContent: "",
        orderable: false,
    },
    totalBudget: {
        title: (window as any).gettext("Total budget ($)"),
        data: "totalbudget",
        defaultContent: "",
        orderable: false,
    },
    totalContractValue: {
        title: (window as any).gettext("Total contract value ($)"),
        data: "totalcontractvalue",
        defaultContent: "",
        orderable: false,
    },
    contractValue: {
        title: (window as any).gettext("Value of the contract - including variations (amendments) ($)"),
        data: "contractvalue",
        defaultContent: "",
        orderable: false,
    },
    paymentPreviousYear: {
        title: (window as any).gettext("Payments previous year ($)"),
        data: "paymentpreviousyear",
        defaultContent: "",
        orderable: false,
    },
    paymentCurrentYear: {
        title: (window as any).gettext("Payments current year ($)"),
        data: "paymentcurrentyear",
        defaultContent: "",
        orderable: false,
    },
    totalPayment: {
        title: (window as any).gettext("Total payment ($)"),
        data: "totalpayment",
        defaultContent: "",
        orderable: false,
    },
    totalProgressPayment: {
        title: (window as any).gettext("Total progress payment (%)"),
        data: "totalprogresspayment",
        defaultContent: "",
        orderable: false,
    },
    balance: {
        title: (window as any).gettext("Balance"),
        data: "balance",
        defaultContent: "",
        orderable: false,
    },
    physicalProgress: {
        title: (window as any).gettext("Physical progress"),
        data: "physicalprogress",
        defaultContent: "",
        orderable: false,
    },
    status: {
        title: (window as any).gettext("Status"),
        data: "status",
        defaultContent: "",
        orderable: false,
    },
    startDate: {
        title: (window as any).gettext("Start date"),
        data: "startdate",
        defaultContent: "",
        orderable: false,
    },
    amendmentStartDate: {
        title: (window as any).gettext("Amendment start date"),
        data: "amendmentstartdate",
        defaultContent: "",
        orderable: false,
    },
    endDate: {
        title: (window as any).gettext("End date"),
        data: "enddate",
        defaultContent: "",
        orderable: false,
    },
    amendmentEndDate: {
        title: (window as any).gettext("Amendment end date"),
        data: "amendmentenddate",
        defaultContent: "",
        orderable: false,
    },
    lastUpdateDate: {
        title: (window as any).gettext("Date of last update"),
        data: "lastupdatedate",
        defaultContent: "",
        orderable: false,
    },
    dlpStartDate: {
        title: (window as any).gettext("DLP start date"),
        data: "dlpstartdate",
        defaultContent: "",
        orderable: false,
    },
    dlpEndDate: {
        title: (window as any).gettext("DLP end date"),
        data: "dlpenddate",
        defaultContent: "",
        orderable: false,
    },
    year: {
        title: (window as any).gettext("Year"),
        data: "year",
        defaultContent: "",
        orderable: false,
    },
    assetClass: {
        title: (window as any).gettext("Asset Class"),
        data: "assetclass",
        defaultContent: "",
        orderable: false,
    },
    totalEmployees: {
        title: (window as any).gettext("Total Employees"),
        data: "totalemployees",
        defaultContent: "",
        orderable: false,
    },
    internationalEmployees: {
        title: (window as any).gettext("International Employees"),
        data: "internationalemployees",
        defaultContent: "",
        orderable: false,
    },
    nationalEmployees: {
        title: (window as any).gettext("National Employees"),
        data: "nationalemployees",
        defaultContent: "",
        orderable: false,
    },
    employeesWithDisabilities: {
        title: (window as any).gettext("Employees With Disabilities"),
        data: "employeeswithdisabilities",
        defaultContent: "",
        orderable: false,
    },
    femaleEmployeesWithDisabilities: {
        title: (window as any).gettext("Female Employees With Disabilities"),
        data: "femaleemployeeswithdisabilities",
        defaultContent: "",
        orderable: false,
    },
    youngEmployees: {
        title: (window as any).gettext("Young Employees"),
        data: "youngemployees",
        defaultContent: "",
        orderable: false,
    },
    youngFemaleEmployees: {
        title: (window as any).gettext("Young Female Employees"),
        data: "youngfemaleemployees",
        defaultContent: "",
        orderable: false,
    },
    femaleEmployees: {
        title: (window as any).gettext("Female Employees"),
        data: "femaleemployees",
        defaultContent: "",
        orderable: false,
    },
    // employeesTotalPercentage: {
    //     title: "%",
    //     data: "employeestotalpercentage",
    //     defaultContent: "",
    //     orderable: false,
    // },
    totalWage: {
        title: (window as any).gettext("Total Wage"),
        data: "totalwage",
        defaultContent: "",
        orderable: false,
    },
    averageGrossWage: {
        title: (window as any).gettext("Average Gross Wage"),
        data: "averagegrosswage",
        defaultContent: "",
        orderable: false,
    },
    averageNetWage: {
        title: (window as any).gettext("Average Net Wage"),
        data: "averagenetwage",
        defaultContent: "",
        orderable: false,
    },
    totalWorkedDays: {
        title: (window as any).gettext("Worked Days"),
        data: "totalworkeddays",
        defaultContent: "",
        orderable: false,
    },
    femaleEmployeesWorkedDays: {
        title: (window as any).gettext("Female Employees"),
        data: "femaleemployeesworkeddays",
        defaultContent: "",
        orderable: false,
    },
    employeesWithDisabilitiesWorkedDays: {
        title: (window as any).gettext("Employees With Disabilities"),
        data: "employeeswithdisabilitiesworkeddays",
        defaultContent: "",
        orderable: false,
    },
    femaleEmployeesWithDisabilitiesWorkedDays: {
        title: (window as any).gettext("Female Employees With Disabilities"),
        data: "femaleemployeeswithdisabilitiesworkeddays",
        defaultContent: "",
        orderable: false,
    },
    youngEmployeesWorkedDays: {
        title: (window as any).gettext("Young Employees"),
        data: "youngemployeesworkeddays",
        defaultContent: "",
        orderable: false,
    },
    youngFemaleEmployeesWorkedDay: {
        title: (window as any).gettext("Young Female Employees"),
        data: "youngfemaleemployeesworkedday",
        defaultContent: "",
        orderable: false,
    },

};

/** The various columns for each dataTable used in the contract reports */
export const reportContractsColumnSets: { [name: string]: string[] } = {
    program: [
        reportContractsTableColumns.title,
        reportContractsTableColumns.fundingSource,
        reportContractsTableColumns.projects,
        reportContractsTableColumns.contracts,
        reportContractsTableColumns.companies,
        reportContractsTableColumns.budget,
        reportContractsTableColumns.contractValue,
        reportContractsTableColumns.paymentPreviousYear,
        reportContractsTableColumns.paymentCurrentYear,
        reportContractsTableColumns.totalPayment,
        reportContractsTableColumns.totalProgressPayment,
        reportContractsTableColumns.balance,
        reportContractsTableColumns.physicalProgress,
        reportContractsTableColumns.status,
    ],
    contractCode: [
        reportContractsTableColumns.title,
        reportContractsTableColumns.status,
        reportContractsTableColumns.programName,
        reportContractsTableColumns.fundingSource,
        reportContractsTableColumns.projectName,
        reportContractsTableColumns.typeOfWork,
        reportContractsTableColumns.projects,
        reportContractsTableColumns.assets,
        reportContractsTableColumns.contractor,
        // reportContractsTableColumns.totalBudget,
        // reportContractsTableColumns.budget,
        // reportContractsTableColumns.totalContractValue,
        reportContractsTableColumns.contractValue,
        reportContractsTableColumns.paymentPreviousYear,
        reportContractsTableColumns.paymentCurrentYear,
        reportContractsTableColumns.totalPayment,
        reportContractsTableColumns.totalProgressPayment,
        reportContractsTableColumns.balance,
        // reportContractsTableColumns.startDate,
        // reportContractsTableColumns.amendmentStartDate,
        // reportContractsTableColumns.endDate,
        // reportContractsTableColumns.amendmentEndDate,
        reportContractsTableColumns.physicalProgress,
        reportContractsTableColumns.lastUpdateDate,
        reportContractsTableColumns.dlpStartDate,
        reportContractsTableColumns.dlpEndDate,
    ],
    assetClassTypeOfWork: [
        reportContractsTableColumns.assetClass,
        reportContractsTableColumns.typeOfWork,
    ],
    typeOfWorkYear: [
        reportContractsTableColumns.typeOfWork,
        reportContractsTableColumns.year,
        reportContractsTableColumns.year,
        reportContractsTableColumns.year,
        reportContractsTableColumns.year,
        reportContractsTableColumns.year,
    ],
    assetClassYear: [
        reportContractsTableColumns.assetClass,
        reportContractsTableColumns.year,
        reportContractsTableColumns.year,
        reportContractsTableColumns.year,
        reportContractsTableColumns.year,
        reportContractsTableColumns.year,
    ],
    numberEmployees: [
        reportContractsTableColumns.title,
        reportContractsTableColumns.totalEmployees,
        reportContractsTableColumns.internationalEmployees,
        reportContractsTableColumns.nationalEmployees,
        reportContractsTableColumns.employeesWithDisabilities,
        reportContractsTableColumns.femaleEmployeesWithDisabilities,
        reportContractsTableColumns.youngEmployees,
        reportContractsTableColumns.youngFemaleEmployees,
        reportContractsTableColumns.femaleEmployees,

    ],
    wages: [
        reportContractsTableColumns.title,
        reportContractsTableColumns.totalWage,
        reportContractsTableColumns.averageGrossWage,
        reportContractsTableColumns.averageNetWage,
    ],
    workedDays: [
        reportContractsTableColumns.title,
        reportContractsTableColumns.totalWorkedDays,
        reportContractsTableColumns.femaleEmployeesWorkedDays,
        reportContractsTableColumns.employeesWithDisabilitiesWorkedDays,
        reportContractsTableColumns.femaleEmployeesWithDisabilitiesWorkedDays,
        reportContractsTableColumns.youngEmployeesWorkedDays,
        reportContractsTableColumns.youngFemaleEmployeesWorkedDay,
    ],
};

/** The definitions of the different contract reports */
export const reportContractsContent: { [name: string]: any } = {
    1: {
        title: (window as any).gettext("Financial and Physical Progress Summary"),
        description: (window as any).gettext("A report on the financial and physical progress of all projects and contracts. This report provides detailed information per contract"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the financial and physical progress summary report"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed financial and physical progress information. You can use filters to generate a customized report"),
        noReportData: (window as any).gettext("Sorry, data for financial and physical progress is not available yet"),
        fixedFilter: {},
        visibleFilters: {
            // assetClass: true,
            // typeOfWork: true,
            // program: true,
            // fundingSource: true,
            // donor: true,
            // fromDate: true,
            // toDate: true,
        },
        reportElements: {
            filters: true,
            total: true,
            attributeNames: ["program"],
            dataTables: [reportContractsTableIds.program],
        },
    },
    2: {
        title: (window as any).gettext("Financial and Physical Progress"),
        description: (window as any).gettext("A summary report on the financial and physical progress of all projects and contracts. This report provides aggregated information per program"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the financial and physical progress report"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed financial and physical progress information. You can use filters to generate a customized report"),
        noReportData: (window as any).gettext("Sorry, data for financial and physical progress is not available yet"),
        fixedFilter: {},
        visibleFilters: {
            // assetClass: true,
            // typeOfWork: true,
            // program: true,
            // fundingSource: true,
            // donor: true,
            // fromDate: true,
            // toDate: true,
        },
        reportElements: {
            filters: true,
            total: true,
            attributeNames: ["contractCode"],
            dataTables: [reportContractsTableIds.contractCode],
        },
    },
    3: {
        title: (window as any).gettext("Completed Contracts"),
        description: (window as any).gettext("A summary report on the total length of works completed by type of work, breakdown by road class and year"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access the completed contracts report"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed completed contracts information. You can use filters to generate a customized report"),
        noReportData: (window as any).gettext("Sorry, data for completed contracts is not available yet"),
        fixedFilter: {},
        visibleFilters: {
            // fundingSource: true,
            // donor: true,
        },
        reportElements: {
            filters: true,
            total: true,
            attributeNames: ["assetClassTypeOfWork", "typeOfWorkYear", "assetClassYear"],
            dataTables: [
                reportContractsTableIds.assetClassTypeOfWork,
                reportContractsTableIds.typeOfWorkYear,
                reportContractsTableIds.assetClassYear,
            ],
        },
    },
    4: {
        title: (window as any).gettext("Social Safeguard"),
        description: (window as any).gettext("A summary report on the social safeguard data for all contracts for the selected period. The report provides information on number of employees, wages and number of worker-days, with a breakdown by gender, age and disabilities"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access social safeguard report"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed social safeguard information. You can use filters to generate a customized report"),
        noReportData: (window as any).gettext("Sorry, data for social safeguard is not available yet"),
        fixedFilter: {},
        visibleFilters: {
            // year: true,
            // quarter: true,
            // month: true,
        },
        reportElements: {
            filters: true,
            attributeNames: ["numberEmployees", "wages", "workedDays"],
            dataTables: [
                reportContractsTableIds.numberEmployees,
                reportContractsTableIds.wages,
                reportContractsTableIds.workedDays
            ],
        },
    },
    5: {
        title: (window as any).gettext("Contract's Social Safeguard"),
        description: (window as any).gettext("A report on the social safeguard data for a selected contract and period. The report provides information on number of employees, wages and number of worker-days, with a breakdown by gender, age and disabilities"),
        noReportTitle: (window as any).gettext("Click on Create Report button to access social safeguard contracts report"),
        noReportDescription: (window as any).gettext("The report will be shown in this area and will provide you with detailed social safeguard information. You can use filters to generate a customized report"),
        noReportData: (window as any).gettext("Sorry, data for social safeguard is not available yet"),
        fixedFilter: {},
        visibleFilters: {
            contractCode: true,
            // fromDate: true,
            // toDate: true,
        },
        reportElements: {
            filters: true,
            attributeNames: ["numberEmployees", "wages", "workedDays"],
            dataTables: [
                reportContractsTableIds.numberEmployees,
                reportContractsTableIds.wages,
                reportContractsTableIds.workedDays
            ],
        },
    },
};

/** IDs of the contract report elements */
export const allContractReportElements = {
    tables: [
        reportContractsTableIds.program,
        reportContractsTableIds.contractCode,
        reportContractsTableIds.assetClassTypeOfWork,
        reportContractsTableIds.typeOfWorkYear,
        reportContractsTableIds.assetClassYear,
        reportContractsTableIds.numberEmployees,
        reportContractsTableIds.wages,
        reportContractsTableIds.workedDays,
    ],
};

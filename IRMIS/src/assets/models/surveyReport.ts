import dayjs from "dayjs";
import { isArray } from "util";

import { Timestamp } from "google-protobuf/google/protobuf/timestamp_pb";
import { Attribute, Report } from "../../../protobuf/report_pb";

import { reportColumns } from "../../reportTableDefinitions";
import { choice_or_default, getFieldName, getHelpText, invertChoices, makeEstradaObject } from "../protoBufUtilities";

import { ADMINISTRATIVE_AREA_CHOICES, ASSET_CLASS_CHOICES, ASSET_CONDITION_CHOICES, IEstrada } from "./estradaBase";
import {
    PAVEMENT_CLASS_CHOICES, ROAD_STATUS_CHOICES, SURFACE_TYPE_CHOICES,
    TECHNICAL_CLASS_CHOICES,
    TERRAIN_CLASS_CHOICES, TRAFFIC_LEVEL_CHOICES,
} from "./road";

// tslint:disable: object-literal-sort-keys
// tslint:disable: max-classes-per-file

// All Ids in the following schemas are generated
const networkReportSchema: { [name: string]: any } = {
    id: { display: "Id" },
    filter: { display: (window as any).gettext("Filter") },
    lengths: { display: (window as any).gettext("Lengths") },
};

const roadReportSchema: { [name: string]: any } = {
    id: { display: "Id" },
    roadCode: { display: (window as any).gettext("Road Code") },
    reportChainageStart: { display: (window as any).gettext("Chainage Start") },
    reportChainageEnd: { display: (window as any).gettext("Chainage End") },
    lengths: { display: (window as any).gettext("Lengths") },
    attributeTableList: { display: (window as any).gettext("Attribute Tables") },
};

const attributeSchema: { [name: string]: any } = {
    roadId: { display: (window as any).gettext("Road Id") },
    roadCode: { display: (window as any).gettext("Road Code") },
    primaryAttribute: { display: (window as any).gettext("Attribute") },
    chainageStart: { display: (window as any).gettext("Chainage Start") },
    chainageEnd: { display: (window as any).gettext("Chainage End") },
    surveyId: { display: "Survey Id" },
    userId: { display: "User Id" },
    dateSurveyed: { display: (window as any).gettext("Survey Date") },
    addedBy: { display: (window as any).gettext("Added By") },
    value: { display: (window as any).gettext("Value") },
};

// These are the response filters returned from reports.py and views.py
const filterTitles: { [name: string]: any } = {
    road_id: { display: (window as any).gettext("Road Id") },
    asset_class: { display: (window as any).gettext("Asset Class"), choices: ASSET_CLASS_CHOICES },
    asset_condition: { display: (window as any).gettext("Surface Condition"), choices: ASSET_CONDITION_CHOICES },
    surface_type: { display: (window as any).gettext("Surface Type"), choices: SURFACE_TYPE_CHOICES },
    municipality: { display: (window as any).gettext("Municipality"), choices: ADMINISTRATIVE_AREA_CHOICES },
    pavement_class: { display: (window as any).gettext("Pavement Class"), choices: PAVEMENT_CLASS_CHOICES },
    date_surveyed: { display: (window as any).gettext("Date Surveyed") },
    // The following filters are handled 'specially'
    // primary_attribute: { display: (window as any).gettext("Attribute") },
    // road_code: { display: (window as any).gettext("Road Code") },
    // report_chainage: { display: (window as any).gettext("Report Chainage") },
};

const lengthTypeChoices: { [name: string]: any } = {
    municipality: ADMINISTRATIVE_AREA_CHOICES,
    number_lanes: {},
    pavement_class: PAVEMENT_CLASS_CHOICES,
    rainfall: {},
    asset_class: ASSET_CLASS_CHOICES,
    road_status: ROAD_STATUS_CHOICES,
    asset_condition: ASSET_CONDITION_CHOICES,
    surface_type: SURFACE_TYPE_CHOICES,
    technical_class: TECHNICAL_CLASS_CHOICES,
    terrain_class: TERRAIN_CLASS_CHOICES,
    traffic_level: TRAFFIC_LEVEL_CHOICES,
};

export function testKeyIsReal(key: any): boolean {
    return ["0", "none", "unknown", "nan", "null", "undefined", "false", ""].indexOf(`${key}`.toLowerCase()) === -1;
}

/** Define a new report column based on the supplied title and columnData */
function defineReportColumn(title: string, columnData: string): void {
    if (reportColumns[columnData]) {
        return;
    }

    // It is assumed that "title" has already been translated
    const newColumn = {
        title,
        data: columnData,
        defaultContent: "",
        className: "text-right",
        orderable: false,
        render: (data: any, type: string) => {
            return (type === "display" && typeof data === "number")
                ? (data / 1000).toFixed(2)
                : data;
        },
    };
    reportColumns[columnData] = newColumn;
}

function extractTitle(lengthKey: string, choices: { [name: string]: any }, useLengthKeyAsDefault = false) {
    let title = choice_or_default(lengthKey, choices, useLengthKeyAsDefault ? lengthKey : "Unknown").toLowerCase();

    if (title === "unknown") {
        // check if we've actually received the title instead of the key
        const invertedChoices = invertChoices(choices);
        const alternateTitle = choice_or_default(lengthKey, invertedChoices, "Unknown").toLowerCase();
        const lengthKeyHasValue = testKeyIsReal(lengthKey);
        if (alternateTitle !== "unknown") {
            title = lengthKey;
            lengthKey = alternateTitle;
        } else if (lengthKeyHasValue) {
            // We do have some kind of supplied key name - so we'll use it.
            title = lengthKey.toLowerCase();
        }
    }
    title = title.length > 1
        ? title[0].toUpperCase() + title.substring(1)
        : title;

    return [title, lengthKey];
}

function extractCountData(
    allLengths: { [name: string]: any },
    primaryAttribute: string,
    useLengthKeyAsDefault = false,
): any[] {
    const lengths: any[] = [];
    const lengthsForType = allLengths[primaryAttribute] || [];
    const choices = lengthTypeChoices[primaryAttribute] || {};
    if (lengthsForType && Object.keys(lengthsForType).length) {
        Object.keys(lengthsForType).forEach((key) => {
            const lengthKeyHasValue = testKeyIsReal(key);
            const [title, lengthKey] = extractTitle(key, choices, useLengthKeyAsDefault);

            if (typeof lengthsForType[key] === "number") {
                lengthsForType[key] = { value: lengthsForType[key] };
            }
            const distance = lengthsForType[key].value;

            // Start building the new 'length' ready for reporting
            const newLength: { [name: string]: any } = { key: lengthKeyHasValue ? lengthKey : 0, title, distance };
            Object.keys(lengthsForType[key]).forEach((attrKey) => {
                if (attrKey === "value") {
                    // Skip the primary attribute value
                    return;
                }
                const attrChoices = lengthTypeChoices[attrKey] || {};
                Object.keys(lengthsForType[key][attrKey]).forEach((attrTerm) => {
                    const [attrTermTitle, attrLengthKey] = extractTitle(attrTerm, attrChoices, useLengthKeyAsDefault);
                    const fullAttrTerm = `${attrKey}|${attrTermTitle}`;
                    newLength[fullAttrTerm] = lengthsForType[key][attrKey][attrTerm];
                    defineReportColumn(attrTermTitle, fullAttrTerm);
                });
            });
            lengths.push(newLength);
        });
    }

    return lengths;
}

function getAssetConditionName(lengths: { [name: string]: any }) {
    const assetConditionNames = ["asset_condition", "surface_condition", "structure_condition"];
    let assetConditionName = "asset_condition";

    if (!lengths) {
        return assetConditionName;
    }

    for (let ix = 0; ix < assetConditionNames.length; ix++) {
        if (lengths[assetConditionNames[ix]]) {
            assetConditionName = assetConditionNames[ix];
            break;
        }
    }

    return assetConditionName;
}

export class EstradaNetworkSurveyReport extends Report implements IEstrada {
    public static getFieldName(field: string) {
        return getFieldName(roadReportSchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(roadReportSchema, field);
    }

    public getId() {
        if (this.roadCodes.length === 1) {
            return `${this.roadCodes}_${this.reportChainage[0]}-${this.reportChainage[1]}`;
        }

        return (this.assetClasses && this.assetClasses.length > 0)
            ? `${this.assetClasses.join(",")}`
            : "";
    }

    get id() {
        return this.getId();
    }

    /** filter is an object(dict) of lists {"key": [values,...]}
     * except for the special "secondary_attribute" which is itself an object of lists
     */
    get filter() {
        const filter = this.getFilter() || "{}";
        return JSON.parse(filter);
    }

    /** Clears the filter, leaving it with a 'primary_attribute' member with an empty list */
    public clearFilter() {
        this.setFilter(JSON.stringify({primary_attribute: []}));
    }

    /** Sets a key (member) in the filter to a specific list of values
     * If values is undefined - then the key will be deleted
     * If values is not an array and key is not "secondary_attribute"
     *  - then it will be converted to an array with a single value
     * If key is "secondary_attribute" we assume value is OK if it's an object or undefined
     */
    public setFilterKey(key: any, values: any) {
        // Verify/correct input parameters
        const hasKey = (key || key === 0);
        if (!hasKey) {
            // no supplied key - so nothing to do
            return;
        }
        if (key === "secondary_attribute") {
            const hasValidSecondaryValues = typeof values === "object" && values !== null;
            if (!hasValidSecondaryValues) {
                return;
            }
        } else {
            if (!isArray(values)) {
                values = [values];
            }
        }

        const currentReportFilter = this.filter;
        currentReportFilter[key] = values;

        this.setFilter(JSON.stringify(currentReportFilter));
    }

    /** Adds a value to the list that is in the filter key
     *
     * Note: this does NOT support "secondary_attribute" filters, use setFilterKey instead
     */
    public filterKeyAddItem(key: any, value: any) {
        // Verify/correct input parameters
        const hasKey = (key || key === 0) && key !== "secondary_attribute";
        const hasValue = (typeof value === "string" || typeof value === "number");
        if (!hasKey || !hasValue) {
            // no supplied key or value  - so nothing to do
            return;
        }

        const currentReportFilter = this.filter;
        currentReportFilter[key] = currentReportFilter[key] || [];
        if (!currentReportFilter[key].includes(value)) {
            currentReportFilter[key].push(value);
            this.setFilter(JSON.stringify(currentReportFilter));
        }
    }

    get formattedFilters(): any[] {
        const rawFilters = this.filter;

        const filterKeys = Object.keys(rawFilters);
        if (filterKeys.length === 0) {
            return [];
        }

        const formattedFilters: any[] = [];
        filterKeys.forEach((key) => {
            let values = rawFilters[key];
            const filterTitle: { [name: string]: any } = filterTitles[key];
            if (values && values.length > 0 && filterTitle) {
                if (!isArray(values)) {
                    values = [values];
                }
                const title = filterTitle.display;
                if (title) {
                    if (filterTitle.choices) {
                        values = values.map((value: any) => (choice_or_default(value, filterTitle.choices || [])));
                    }
                    formattedFilters.push({ key, title, values });
                }
            }
        });

        return formattedFilters;
    }

    /** lengths is an object(dict) of term:value pairs where value is an object of the form:
     * - {"value": numeric} for simple reports (no secondary attribute)
     * - {"value": numeric, "secondary_attribute": {"term": numeric}}
     */
    get lengths() {
        let lengths = "";

        try {
            lengths = this.getLengths();
        } catch {
            lengths = "";
        }

        // We can change the following to
        // whatever we consider an appropriate 'empty' collection of lengths
        const emptyLengths = [
            "municipality",
            "number_lanes",
            "pavement_class",
            "rainfall",
            "asset_class",
            "asset_condition",
            "surface_type",
            "technical_class",
            "terrain_class"
        ].map((attribute) => `"${attribute}": { "None": { "value": 0 } }`);

        lengths = lengths || `{ ${emptyLengths.join(", ")} }`;

        return JSON.parse(lengths);
    }

    /** Clears the lengths */
    public clearLengths() {
        this.setLengths(JSON.stringify({}));
    }

    /** Sets a term:value pair in the lengths[key]
     * If value is undefined or not numeric, or not an object that at least specifies {value: numeric}
     *    then nothing is done
     * If value is numeric or {value: numeric} then the term:value pair is set/appended in lengths[key]
     * If value is undefined then the term is removed from lengths[key]
     * If lengths[key] has no more terms then the key is removed from lengths
     */
    public lengthsKeyAddItem(key: any, term: any, value?: any) {
        // Verify/correct input parameters
        const hasKey = (key || key === 0);
        const hasTerm = (term || term === 0);
        const hasValue = (typeof value === "undefined" || typeof value === "number" || (value && typeof value.value === "number"));
        if (!hasKey || !hasTerm || !hasValue) {
            // no supplied key, term or valid value  - so nothing to do
            return;
        }
        if (typeof value === "number") {
            value = { value };
        }

        const currentLengths = this.lengths;
        const keyExists = currentLengths[key];
        const termExists = keyExists && currentLengths[key][term];

        if (typeof value === "undefined") {
            let isDirty = false;
            if (termExists) {
                currentLengths[key][term] = undefined; // delete the term
                isDirty = true;
            }
            if (keyExists && Object.keys(currentLengths[key]).length === 0) {
                currentLengths[key] = undefined; // delete the key
                isDirty = true;
            }
            if (!isDirty) {
                // nothing to do
                return;
            }
        } else {
            currentLengths[key] = currentLengths[key] || {};
            currentLengths[key][term] = value;
        }

        this.setLengths(JSON.stringify(currentLengths));
    }

    get roadCodes() {
        return this.filter.road_code || [];
    }

    get assetClass() {
        return this.filter.asset_class || [];
    }

    get reportChainage() {
        return this.filter.report_chainage || [];
    }

    // ==================
    // from here on is 'v2' of the reports proto
    get attributesList() {
        const attributesRaw = this.getAttributesList();
        return attributesRaw.map(makeEstradaSurveyAttribute);
    }

    get municipalities() {
        return this.makeSpecificLengths("municipality");
    }

    get numberLanes() {
        return this.makeSpecificLengths("number_lanes");
    }

    get pavementClasses() {
        return this.makeSpecificLengths("pavement_class");
    }

    get rainfalls() {
        return this.makeSpecificLengths("rainfall");
    }

    get assetClasses() {
        return this.makeSpecificLengths("asset_class");
    }

    get roadStatuses() {
        return this.makeSpecificLengths("road_status");
    }

    get assetConditions() {
        const assetConditionName = getAssetConditionName(this.lengths);
        return this.makeSpecificLengths(assetConditionName);
    }

    get surfaceTypes() {
        return this.makeSpecificLengths("surface_type");
    }

    get technicalClasses() {
        return this.makeSpecificLengths("technical_class");
    }

    get terrainClasses() {
        return this.makeSpecificLengths("terrain_class");
    }

    get trafficLevels() {
        return this.makeSpecificLengths("traffic_level");
    }

    /** Returns a collection of attributes matching the criteria
     * @param {string} primaryAttribute The primaryAttribute (within all of the attributes) to search for
     * @param {Timestamp} [dateSurveyed=null] All attributes up to and including this date are acceptable
     *     (null = take them all)
     * @param {boolean} [returnAllDates=false] Return all matching attributes,
     *     false means only return the most recent
     * @param {boolean} [returnAllEntries=false] Return all entries,
     *     false means return nothing if there are only 'generated' entries
     * @return {object[]} An array of simplified attribute objects
     */
    public attributes(
        primaryAttribute: string,
        dateSurveyed?: Timestamp,
        returnAllDates = false,
        returnAllEntries = false,
    ): {
        date_surveyed: Timestamp | undefined;
        attributeEntries: EstradaSurveyAttribute[];
    } {
        let filteredAttributes = this.attributesList.filter((attribute) => {
            return attribute.primaryAttribute === primaryAttribute;
        });

        if (filteredAttributes.length === 0) {
            return {date_surveyed: undefined, attributeEntries: []};
        }

        // Descending sort most recent dateSurveyed, down to null dateSurveyed
        filteredAttributes.sort((a, b) => {
            if (a.dateSurveyed && b.dateSurveyed) {
                return (a.dateSurveyed > b.dateSurveyed) ? -1 : 1;
            }
            if (a.dateSurveyed && !b.dateSurveyed) {
                return -1;
            }
            if (!a.dateSurveyed && b.dateSurveyed) {
                return 1;
            }

            // If we're here it's actually bad data
            return 0;
        });

        if (dateSurveyed) {
            filteredAttributes = filteredAttributes.filter((attribute) => {
                const attributeDateSurveyed = attribute.getDateSurveyed();

                return !attributeDateSurveyed
                    ? true
                    : (attributeDateSurveyed <= dateSurveyed);
            });
        }

        // Temporarily commented out until actual date_filtering done
        // if (!returnAllDates) {
        //     filteredAttributes = [filteredAttributes];
        // }

        if (!returnAllEntries) {
            const allGenerated = filteredAttributes.filter((attribute) => {
                return attribute.userId;
            }).length === 0;

            if (allGenerated) {
                filteredAttributes = [];
            }
        }

        return {
            date_surveyed: dateSurveyed,
            attributeEntries: filteredAttributes,
        };
    }

    private makeSpecificLengths(primaryAttribute: string, useLengthKeyAsDefault = false) {
        return extractCountData(this.lengths, primaryAttribute, useLengthKeyAsDefault);
    }
}

export class EstradaSurveyAttribute extends Attribute implements IEstrada {
    public static getFieldName(field: string) {
        return getFieldName(attributeSchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(attributeSchema, field);
    }

    public getId() {
        return `${this.roadId}_${this.primaryAttribute}-${this.surveyId}`;
    }

    get id() {
        return this.getId();
    }

    get roadId() {
        return this.getRoadId();
    }

    get roadCode() {
        return this.getRoadCode();
    }

    get primaryAttribute() {
        return this.getPrimaryAttribute() || "";
    }

    get chainageStart() {
        return this.getChainageStart() || 0;
    }

    get chainageEnd() {
        return this.getChainageEnd();
    }

    get surveyId() {
        return this.getSurveyId();
    }

    get userId() {
        return this.getUserId();
    }

    get dateSurveyed() {
        // Note getDateSurveyed doesn't actually return a proper Timestamp object
        const pbufData = this.getDateSurveyed() as ({ [name: string]: any } | undefined);
        if (!pbufData || !pbufData.array || !pbufData.array.length) {
            return "";
        }
        const date = dayjs(new Date(pbufData.array[0] * 1000));
        return date.isValid() ? date.format("YYYY-MM-DD") : "";
    }

    get addedBy() {
        return this.getAddedBy() || "";
    }

    get value() {
        return this.getValue() || "";
    }

    get length() {
        return this.chainageEnd - this.chainageStart;
    }

    get municipality(): string {
        return this.primaryAttribute === "municipality" && this.value
            ? this.value : this.unknownI8n();
    }

    get carriagewayWidth(): number | string {
        const numericValue = parseFloat(this.value);
        return this.primaryAttribute === "carriageway_width" && numericValue
            ? numericValue.toFixed(1) : this.unknownI8n();
    }

    get numberLanes(): number | string {
        const numericValue = parseInt(this.value, 10);
        return this.primaryAttribute === "number_lanes" && numericValue
            ? numericValue.toFixed(0) : this.unknownI8n();
    }

    get pavementClass(): string {
        return this.primaryAttribute === "pavement_class"
            ? (window as any).gettext(choice_or_default(this.value, PAVEMENT_CLASS_CHOICES, "Unknown")) as string
            : this.unknownI8n();
    }

    get rainfall(): number | string {
        const numericValue = parseInt(this.value, 10);
        return this.primaryAttribute === "rainfall" && numericValue
            ? numericValue.toFixed(0) : this.unknownI8n();
    }

    get trafficCounts(): { [name: string]: any }  {
        return this.value ? JSON.parse(this.value).counts : {} || {};
    }

    get trafficCountTotal(): number {
        return this.value ? JSON.parse(this.value).countTotal : 0 || 0;
    }

    get trafficDataType(): string {
        return this.value
            ? JSON.parse(this.value).trafficType
            : this.unknownI8n() || this.unknownI8n();
    }

    get assetClass(): string {
        // "structure_class", "road_class", "road_type" have all been deprecated
        return this.primaryAttribute === "asset_class"
            ? (window as any).gettext(choice_or_default(this.value, ASSET_CLASS_CHOICES, "Unknown")) as string
            : this.unknownI8n();
    }

    get assetCondition(): string {
        return ["asset_condition", "surface_condition", "structure_condition"].includes(this.primaryAttribute)
            ? (window as any).gettext(choice_or_default(this.value, ASSET_CONDITION_CHOICES, "Unknown")) as string
            : this.unknownI8n();
    }

    get surfaceType(): string {
        return this.primaryAttribute === "surface_type"
            ? (window as any).gettext(choice_or_default(this.value, SURFACE_TYPE_CHOICES, "Unknown")) as string
            : this.unknownI8n();
    }

    get technicalClass(): string {
        return this.primaryAttribute === "technical_class"
            ? (window as any).gettext(choice_or_default(this.value, TECHNICAL_CLASS_CHOICES, "Unknown")) as string
            : this.unknownI8n();
    }

    get terrainClass(): string {
        return this.primaryAttribute === "terrain_class"
            ? (window as any).gettext(choice_or_default(this.value, TERRAIN_CLASS_CHOICES, "Unknown")) as string
            : this.unknownI8n();
    }

    get trafficLevel(): string {
        return this.primaryAttribute === "traffic_level"
            ? (window as any).gettext(choice_or_default(this.value, TRAFFIC_LEVEL_CHOICES, "Unknown")) as string
            : this.unknownI8n();
    }

    private unknownI8n(): string {
        return (window as any).gettext("Unknown") as string;
    }
}

export function makeEstradaNetworkSurveyReport(pbsurveyreport?: { [name: string]: any }) {
    return makeEstradaObject(EstradaNetworkSurveyReport, pbsurveyreport) as EstradaNetworkSurveyReport;
}

export function makeEstradaSurveyAttribute(pbattribute: { [name: string]: any }) {
    return makeEstradaObject(EstradaSurveyAttribute, pbattribute) as EstradaSurveyAttribute;
}

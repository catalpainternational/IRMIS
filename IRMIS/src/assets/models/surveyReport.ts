import dayjs from "dayjs";
import { isArray } from "util";

import { Timestamp } from "google-protobuf/google/protobuf/timestamp_pb";
import { Attribute, Report } from "../../../protobuf/report_pb";
import { makeEstradaPhoto, EstradaPhoto } from "./photo";

import { reportColumns } from "../../reportTableDefinitions";
import { choice_or_default, getFieldName, getHelpText, invertChoices, makeEstradaObject } from "../protoBufUtilities";

import { ADMINISTRATIVE_AREA_CHOICES, ASSET_CLASS_CHOICES, ASSET_CONDITION_CHOICES, ASSET_TYPE_CHOICES, IEstrada } from "./estradaBase";
import {
    PAVEMENT_CLASS_CHOICES, ROAD_STATUS_CHOICES, SURFACE_TYPE_CHOICES,
    TECHNICAL_CLASS_CHOICES,
    TERRAIN_CLASS_CHOICES, TRAFFIC_LEVEL_CHOICES,
} from "./road";

// tslint:disable: object-literal-sort-keys
// tslint:disable: max-classes-per-file

// All Ids in the following schemas are generated
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
    assetType: { display: (window as any).gettext("Asset Type") },
};

// These are the response filters returned from reports.py and views.py
const filterTitles: { [name: string]: any } = {
    road_id: { display: (window as any).gettext("Road Id") },
    asset_id: { display: (window as any).gettext("Asset Id") },
    asset_code: { display: (window as any).gettext("Asset Code") },
    asset_type: { display: (window as any).gettext("Asset Type"), choices: ASSET_TYPE_CHOICES },
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
    asset_type: ASSET_TYPE_CHOICES,
    asset_class: ASSET_CLASS_CHOICES,
    road_status: ROAD_STATUS_CHOICES,
    asset_condition: ASSET_CONDITION_CHOICES,
    surface_type: SURFACE_TYPE_CHOICES,
    technical_class: TECHNICAL_CLASS_CHOICES,
    terrain_class: TERRAIN_CLASS_CHOICES,
    traffic_level: TRAFFIC_LEVEL_CHOICES,
    source_roughness: {},
    roughness: {},
};

export function testKeyIsReal(key: any): boolean {
    return ["0", "none", "unknown", "nan", "null", "undefined", "false", ""].indexOf(`${key}`.toLowerCase()) === -1;
}

/** Define a new report column based on the supplied title and columnData */
function defineReportColumn(title: string, columnData: string, isCount = false): void {
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
                ? isCount ? data.toFixed(0) : (data / 1000).toFixed(2)
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
    isCount = false,
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
                    defineReportColumn(attrTermTitle, fullAttrTerm, isCount);
                });
            });
            lengths.push(newLength);
        });
    }

    return lengths;
}

export class EstradaNetworkSurveyReport extends Report implements IEstrada {
    public static getFieldName(field: string) {
        return getFieldName(roadReportSchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(roadReportSchema, field);
    }

    /** A 'nominal' Id for the data returned in this report */
    public getId() {
        if (this.assetTypeList.length === 0) {
            return "";
        }

        if (this.assetTypeList.length === 1) {
            const assetType = this.assetTypeList[0];
            if (this.assetCodes.length === 1) {
                const idPrefix = `${assetType}_${this.assetCodes}`;
                if (assetType !== "ROAD") {
                    return idPrefix;
                }
                return `${idPrefix}_${this.reportChainage[0]}-${this.reportChainage[1]}`;
            }
        }
        const assetTypes = this.assetTypeList.join(",");
        const assetClasses = this.assetClasses.join(",");
        return (assetTypes.length && assetClasses.length)
            ? `${assetTypes}_${assetClasses}`
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

    /** Clears the filter, leaving it with 'report_asset_type' and 'primary_attribute' members with empty lists */
    public clearFilter() {
        this.setFilter(JSON.stringify({report_asset_type: [], primary_attribute: []}));
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
            "terrain_class",
            "roughness",
            "source_roughness",
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
    public lengthsKeyAddItem(key: any, term: any, assetSchema: { [name: string]: any }, value?: any) {
        // Verify/correct input parameters
        const hasKey = (key || key === 0);
        const hasTerm = (term || term === 0 || (Array.isArray(term) && term.length));
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
            // get the terms translation
            if (Array.isArray(term) && term.length === 1) {
                term = term[0];
            }
            let transTerm = term;
            if (assetSchema[key] && assetSchema[key].options) {
                const selectedOption =
                    assetSchema[key].options.filter((option: any) => {
                        const optionTerm = (Array.isArray(option) ? option[0] : option.code);
                        return optionTerm === term;
                    });
                if (selectedOption.length === 1) {
                    transTerm = Array.isArray(selectedOption)
                        ? selectedOption[0][1]
                        : selectedOption.name;
                }
            }

            value.title = transTerm;

            currentLengths[key] = currentLengths[key] || {};
            currentLengths[key][term] = value;
        }

        this.setLengths(JSON.stringify(currentLengths));
    }

    get assetTypeList() {
        return [...new Set(this.assetIds.map((assetId) => assetId.substr(0, 4)))];
    }

    get assetIds(): string[] {
        return this.filter.asset_id || [];
    }

    get assetCodes(): string[] {
        return this.filter.asset_code || [];
    }

    /** road codes are only relevant when the asset(s) reported on are structures
     * It identifies the road(s) related to the structure(s)
     */
    get roadCodes(): string[] {
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

    get mergedAttributes() {
        const allAttributes = this.attributesList;

        const mergeSet: { [name: number]: EstradaSurveyAttribute } = {};
        allAttributes.forEach((attribute) => {
            const surveyId = attribute.surveyId;
            mergeSet[surveyId] = mergeSet[surveyId] || makeEstradaSurveyAttribute(attribute);
            const newPrimaryAttributeList = `["${attribute.primaryAttribute}"]`;

            const newValue = attribute.getValue();

            if (mergeSet[surveyId].primaryAttribute !== attribute.primaryAttribute
                && mergeSet[surveyId].primaryAttribute !== newPrimaryAttributeList) {
                const currentAttributes = JSON.parse(mergeSet[surveyId].getPrimaryAttribute());
                currentAttributes.push(attribute.primaryAttribute);
                mergeSet[surveyId].setPrimaryAttribute(JSON.stringify(currentAttributes));
                const currentValues = JSON.parse(mergeSet[surveyId].getValue());
                currentValues[attribute.primaryAttribute] = newValue;
                mergeSet[surveyId].setValue(JSON.stringify(currentValues));
            } else {
                mergeSet[surveyId].setPrimaryAttribute(`["${attribute.primaryAttribute}"]`);
                mergeSet[surveyId].setValue(`{"${attribute.primaryAttribute}": "${newValue}"}`);
            }
        });

        return Object.values(mergeSet);
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
        return this.makeSpecificLengths("asset_condition");
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

    get roughnesses() {
        return this.makeSpecificLengths("roughness");
    }

    get sourceRoughnesses() {
        return this.makeSpecificLengths("source_roughness");
    }

    get assetTypes() {
        return this.makeSpecificLengths("asset_type", false, true);
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

    private makeSpecificLengths(primaryAttribute: string, useLengthKeyAsDefault = false, isCount = false) {
        return extractCountData(this.lengths, primaryAttribute, useLengthKeyAsDefault, isCount);
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
        return `${this.assetId}_${this.primaryAttribute}-${this.surveyId}`;
    }

    get id() {
        return this.getId();
    }

    get assetType() {
        return this.assetId.substr(0, 4);
    }

    get assetId() {
        return this.getAssetId();
    }

    get assetCode() {
        return this.getAssetCode();
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
        return this.extractStringValue("municipality");
    }

    get carriagewayWidth(): number | string {
        return this.extractFloatValue("carriageway_width");
    }

    get totalWidth(): number | string {
        return this.extractFloatValue("total_width");
    }

    get numberLanes(): number | string {
        return this.extractIntValue("number_lanes");
    }

    get pavementClass(): string {
        return this.extractChoiceValue("pavement_class", PAVEMENT_CLASS_CHOICES);
    }

    get rainfall(): number | string {
        return this.extractIntValue("rainfall");
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
        return this.extractChoiceValue("asset_class", ASSET_CLASS_CHOICES);
    }

    get assetCondition(): string {
        return this.extractChoiceValue("asset_condition", ASSET_CONDITION_CHOICES);
    }

    get surfaceType(): string {
        return this.extractChoiceValue("surface_type", SURFACE_TYPE_CHOICES);
    }

    get technicalClass(): string {
        return this.extractChoiceValue("technical_class", TECHNICAL_CLASS_CHOICES);
    }

    get terrainClass(): string {
        return this.extractChoiceValue("terrain_class", TERRAIN_CLASS_CHOICES);
    }

    get trafficLevel(): string {
        return this.extractChoiceValue("traffic_level", TRAFFIC_LEVEL_CHOICES);
    }

    get sourceRoughness(): number | string {
        return this.extractFloatValue("source_roughness");
    }

    get roughness(): string {
        return this.extractStringValue("roughness");
    }

    get photos(): EstradaPhoto[] | undefined {
        const photosListRaw = this.getPhotosList();
        return photosListRaw ? photosListRaw.map(makeEstradaPhoto) : photosListRaw;
    }

    set photos(values: EstradaPhoto[] | undefined) {
        this.setPhotosList(values as Photo[]);
    }

    private unknownI8n(): string {
        return (window as any).gettext("Unknown") as string;
    }

    private extractAnyValue(primaryAttribute: string): string | null {
        const simpleMatch = this.primaryAttribute === primaryAttribute;
        const arrayMatch = !simpleMatch && this.primaryAttribute.indexOf(`"${primaryAttribute}`) !== -1;
        if (!simpleMatch && !arrayMatch) {
            return null;
        }
        let extractedValue: string | null = this.value;
        if (arrayMatch) {
            let valueObj: { [name: string]: string } = {};
            try {
                valueObj = JSON.parse(extractedValue);
                extractedValue = valueObj[primaryAttribute] || null;
            }
            catch {
                extractedValue = null;
            }
        }

        return extractedValue;
    }

    private extractStringValue(primaryAttribute: string): string {
        const extractedValue = this.extractAnyValue(primaryAttribute);

        if (!extractedValue) {
            return this.unknownI8n();
        }
        return (window as any).gettext(extractedValue) as string;
    }

    private extractFloatValue(primaryAttribute: string): number | string {
        const extractedValue = this.extractAnyValue(primaryAttribute);

        if (!extractedValue) {
            return this.unknownI8n();
        }
        const numericValue = parseFloat(extractedValue);
        return numericValue
            ? numericValue.toFixed(1) : this.unknownI8n();
    }

    private extractIntValue(primaryAttribute: string): number | string {
        const extractedValue = this.extractAnyValue(primaryAttribute);

        if (!extractedValue) {
            return this.unknownI8n();
        }
        const numericValue = parseInt(extractedValue, 10);
        return numericValue
            ? numericValue.toFixed(0) : this.unknownI8n();
    }

    private extractChoiceValue(primaryAttribute: string, choices: {[name: string]: any}): string {
        const extractedValue = this.extractAnyValue(primaryAttribute);

        if (!extractedValue) {
            return this.unknownI8n();
        }

        return (window as any).gettext(choice_or_default(extractedValue, choices, "Unknown")) as string;
    }
}

export function makeEstradaNetworkSurveyReport(pbsurveyreport?: { [name: string]: any }) {
    return makeEstradaObject(EstradaNetworkSurveyReport, pbsurveyreport) as EstradaNetworkSurveyReport;
}

export function makeEstradaSurveyAttribute(pbattribute: { [name: string]: any }) {
    return makeEstradaObject(EstradaSurveyAttribute, pbattribute) as EstradaSurveyAttribute;
}

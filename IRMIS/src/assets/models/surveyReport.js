import dayjs from "dayjs";
import { isArray } from "util";

import { Timestamp } from "google-protobuf/google/protobuf/timestamp_pb";
import { Attribute, Report } from "../../../protobuf/report_pb";

import { choice_or_default, getFieldName, getHelpText, invertChoices, makeEstradaObject } from "../protoBufUtilities";
import { reportColumns } from "../../reportManager";

import {
    ROAD_STATUS_CHOICES, ROAD_TYPE_CHOICES,
    SURFACE_CONDITION_CHOICES, SURFACE_TYPE_CHOICES,
    TECHNICAL_CLASS_CHOICES, TRAFFIC_LEVEL_CHOICES,
    PAVEMENT_CLASS_CHOICES, TERRAIN_CLASS_CHOICES
} from "./road";

// All Ids in the following schemas are generated
const networkReportSchema = {
    id: { display: "Id" },
    filter: { display: gettext("Filter") },
    lengths: { display: gettext("Lengths") },
};

const roadReportSchema = {
    id: { display: "Id" },
    roadCode: { display: gettext("Road Code") },
    reportChainageStart: { display: gettext("Chainage Start") },
    reportChainageEnd: { display: gettext("Chainage End") },
    lengths: { display: gettext("Lengths") },
    attributeTableList: { display: gettext("Attribute Tables") },
};

const attributeSchema = {
    roadId: { display: gettext("Road Id") },
    roadCode: { display: gettext("Road Code") },
    primaryAttribute: { display: gettext("Attribute") },
    chainageStart: { display: gettext("Chainage Start") },
    chainageEnd: { display: gettext("Chainage End") },
    surveyId: { display: "Survey Id" },
    userId: { display: "User Id" },
    dateSurveyed: { display: gettext("Survey Date") },
    addedBy: { display: gettext("Added By") },
    value: { display: gettext("Value") },
};

function AdminAreaChoices() {
    const adminAreaChoices = {};
    window.asset_schema.administrative_area.options.forEach((option) => {
        adminAreaChoices[option.id] = option.name || option.id;
    });

    return adminAreaChoices;
}

// These are the response filters returned from reports.py and views.py
const filterTitles = {
    road_id: { display: gettext("Road Id") },
    road_type: { display: gettext("Road Class"), choices: ROAD_TYPE_CHOICES },
    surface_condition: { display: gettext("Surface Condition"), choices: SURFACE_CONDITION_CHOICES },
    surface_type: { display: gettext("Surface Type"), choices: SURFACE_TYPE_CHOICES },
    municipality: { display: gettext("Municipality"), choices: AdminAreaChoices() },
    pavement_class: { display: gettext("Pavement Class"), choices: PAVEMENT_CLASS_CHOICES },
    date_surveyed: { display: gettext("Date Surveyed") },
    // The following filters are handled 'specially'
    // primary_attribute: { display: gettext("Attribute") },
    // road_code: { display: gettext("Road Code") },
    // report_chainage: { display: gettext("Report Chainage") },
};

const lengthTypeChoices = {
    municipality: AdminAreaChoices(),
    number_lanes: {},
    pavement_class: PAVEMENT_CLASS_CHOICES,
    rainfall: {},
    // road_class is an alias for road_type
    road_class: ROAD_TYPE_CHOICES,
    road_status: ROAD_STATUS_CHOICES,
    road_type: ROAD_TYPE_CHOICES,
    surface_condition: SURFACE_CONDITION_CHOICES,
    surface_type: SURFACE_TYPE_CHOICES,
    technical_class: TECHNICAL_CLASS_CHOICES,
    terrain_class: TERRAIN_CLASS_CHOICES,
    traffic_level: TRAFFIC_LEVEL_CHOICES,
};

export function testKeyIsReal(key) {
    return ["0", "none", "unknown", "nan", "null", "undefined", "false"].indexOf(`${key}`.toLowerCase()) === -1;
}

/** Define a new report column based on the supplied title and columnData */
function defineReportColumn(title, columnData) {
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
        render: (data, type) => {
            return (type === 'display')
                ? (data / 1000).toFixed(2)
                : data;
        },
    };
    reportColumns[columnData] = newColumn;
}

function extractTitle(lengthKey, choices, useLengthKeyAsDefault) {
    let title = choice_or_default(lengthKey, choices, useLengthKeyAsDefault ? lengthKey : "Unknown").toLowerCase();

    if (title === "unknown") {
        // check if we've actually received the title instead of the key
        const invertedChoices = invertChoices(choices);
        let alternateTitle = choice_or_default(lengthKey, invertedChoices, "Unknown").toLowerCase();
        let lengthKeyHasValue = testKeyIsReal(lengthKey);
        if (alternateTitle !== "unknown") {
            title = lengthKey;
            lengthKey = alternateTitle;
        } else if (lengthKeyHasValue) {
            // We do have some kind of supplied key name - so we'll use it.
            title = lengthKey.toLowerCase();
        }
    }
    title = title[0].toUpperCase() + title.substring(1);

    return [title, lengthKey];
}

function extractCountData(allLengths, primary_attribute, useLengthKeyAsDefault = false) {
    const lengths = [];
    const lengthsForType = allLengths[primary_attribute] || [];
    const choices = lengthTypeChoices[primary_attribute] || {};
    if (lengthsForType && Object.keys(lengthsForType).length) {
        Object.keys(lengthsForType).forEach((key) => {
            let lengthKeyHasValue = testKeyIsReal(key);
            let [title, lengthKey] = extractTitle(key, choices, useLengthKeyAsDefault);

            if (typeof lengthsForType[key] === "number") {
                lengthsForType[key] = { "value": lengthsForType[key]}
            }
            const distance = lengthsForType[key].value;

            // Start building the new 'length' ready for reporting 
            const newLength = { key: lengthKeyHasValue ? lengthKey : 0, title, distance };
            Object.keys(lengthsForType[key]).forEach((attrKey) => {
                if (attrKey === "value") {
                    // Skip the primary attribute value
                    return;
                }
                const attrChoices = lengthTypeChoices[attrKey] || {};
                Object.keys(lengthsForType[key][attrKey]).forEach((attrTerm) => {
                    let [attrTermTitle, attrLengthKey] = extractTitle(attrTerm, attrChoices, useLengthKeyAsDefault);
                    const fullAttrTerm = `${attrKey}.${attrTermTitle}`;
                    newLength[fullAttrTerm] = lengthsForType[key][attrKey][attrTerm];
                    defineReportColumn(attrTermTitle, fullAttrTerm);
                });
            });
            lengths.push(newLength);
        });
    }

    return lengths;
}

export class EstradaNetworkSurveyReport extends Report {
    getId() {
        if (this.roadCodes.length === 1) {
            return `${this.roadCodes}_${this.reportChainage[0]}-${this.reportChainage[1]}`;
        }

        return (this.roadTypes && this.roadTypes.length > 0)
            ? `${this.roadTypes.join(",")}`
            : null;
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
    clearFilter() {
        this.setFilter(JSON.stringify({"primary_attribute": []}));
    }

    /** Sets a key (member) in the filter to a specific list of values
     * If values is undefined - then the key will be deleted
     * If values is not an array and key is not "secondary_attribute"
     *  - then it will be converted to an array with a single value
     * If key is "secondary_attribute" we assume value is OK if it's an object or undefined
     */
    setFilterKey(key, values) {
        // Verify/correct input parameters
        const hasKey = (key || key === 0);
        if (!hasKey) {
            // no supplied key - so nothing to do
            return;
        }
        if (key === "secondary_attribute") {
            let hasValidSecondaryValues = typeof values === "object" && values !== null;
            if (!hasValidSecondaryValues) {
                return;
            }
        } else {
            if (!isArray(values)) {
                values = [values];
            }
        }

        const currentFilter = this.filter;
        currentFilter[key] = values;
        
        this.setFilter(JSON.stringify(currentFilter));
    }

    /** Adds a value to the list that is in the filter key
     * 
     * Note: this does NOT support "secondary_attribute" filters, use setFilterKey instead
     */
    filterKeyAddItem(key, value) {
        // Verify/correct input parameters
        const hasKey = (key || key === 0) && key !== "secondary_attribute";
        const hasValue = (typeof value === "string" || typeof value === "number");
        if (!hasKey || !hasValue) {
            // no supplied key or value  - so nothing to do
            return;
        }

        const currentFilter = this.filter;
        currentFilter[key] = currentFilter[key] || [];
        if (!currentFilter[key].includes(value)) {
            currentFilter[key].push(value);
            this.setFilter(JSON.stringify(currentFilter));
        }
    }

    get formattedFilters() {
        const rawFilters = this.filter;

        const filterKeys = Object.keys(rawFilters);
        if (filterKeys.length === 0) {
            return [];
        }

        const formattedFilters = [];
        filterKeys.forEach((key) => {
            let values = rawFilters[key];
            let filterTitle = filterTitles[key];
            if (values && values.length > 0 && filterTitle) {
                if (!isArray(values)) {
                    values = [values];
                }
                const title = filterTitle.display;
                if (title) {
                    if (filterTitle.choices) {
                        values = values.map((value) => (choice_or_default(value, filterTitle.choices || [])));
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
            "road_type",
            "surface_condition",
            "surface_type",
            "technical_class",
            "terrain_class"
        ].map((attribute) => `"${attribute}": { "None": { "value": 0 } }`);

        lengths = lengths || `{ ${emptyLengths.join(", ")} }`;

        return JSON.parse(lengths);
    }

    /** Clears the lengths */
    clearLengths() {
        this.setLengths(JSON.stringify({}));
    }

    /** Sets a key (member) in the lengths specified object of term:value pairs
     * If termValues is undefined - then the key will be deleted
     */
    setLengthsKey(key, termValues = undefined) {
        // Verify/correct input parameters
        const hasKey = (key || key === 0);
        let hasValidTermValues = typeof termValues === "object" && termValues !== null;
        if (hasValidTermValues) {
            const tempTermValues = {};
            Object.keys(termValues).forEach((term) => {
                if (typeof termValues[term] === "number") {
                    tempTermValues[term] = { "value": termValues[term] };
                } else if (termValues[term] && typeof termValues[term].value === "number") {
                    tempTermValues[term] = termValues[term];
                }
            });
            termValues = tempTermValues;
            // Reassess whether we have valid term:value pairs
            hasValidTermValues = Object.keys(termValues).length > 0;
        } else if (typeof termValues === "undefined") {
            // "undefined" termValues is a valid termValues
            hasValidTermValues = true;
        }
        if (!hasKey || !hasValidTermValues) {
            // no supplied key and/or no valid termValues - so nothing to do
            return;
        }
        
        const currentLengths = this.lengths;
        const keyExists = currentLengths[key];
        if (!keyExists && typeof termValues === "undefined") {
            // nothing to do
            return;
        }
        currentLengths[key] = termValues;
        
        this.setLengths(JSON.stringify(currentLengths));
    }

    /** Sets a term:value pair in the lengths[key]
     * If value is undefined or not numeric, or not an object that at least specifies {value: numeric} then nothing is done
     * If value is numeric or {value: numeric} then the term:value pair is set/appended in lengths[key]
     * If value is undefined then the term is removed from lengths[key]
     * If lengths[key] has no more terms then the key is removed from lengths
     */
    lengthsKeyAddItem(key, term, value = undefined) {
        // Verify/correct input parameters
        const hasKey = (key || key === 0);
        const hasTerm = (term || term === 0);
        const hasValue = (typeof value === "undefined" || typeof value === "number" || (value && typeof value.value === "number"));
        if (!hasKey || !hasTerm || !hasValue) {
            // no supplied key, term or valid value  - so nothing to do
            return;
        }
        if (typeof value === "number") {
            value = { "value": value };
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

    get roadTypes() {
        return this.filter.road_type || [];
    }

    get reportChainage() {
        return this.filter.report_chainage || [];
    }

    get municipalities() {
        return extractCountData(this.lengths, "municipality");
    }

    get numberLanes() {
        return extractCountData(this.lengths, "number_lanes");
    }

    get pavementClasses() {
        return extractCountData(this.lengths, "pavement_class");
    }

    get rainfall() {
        return extractCountData(this.lengths, "rainfall");
    }

    /** roadClasses is an alias for roadTypes */
    get roadClasses() {
        return this.roadTypes;
    }

    get roadStatuses() {
        return extractCountData(this.lengths, "road_status");
    }

    get roadTypes() {
        return extractCountData(this.lengths, "road_type");
    }

    get surfaceConditions() {
        return extractCountData(this.lengths, "surface_condition");
    }

    get surfaceTypes() {
        return extractCountData(this.lengths, "surface_type");
    }

    get technicalClasses() {
        return extractCountData(this.lengths, "technical_class");
    }

    get terrainClasses() {
        return extractCountData(this.lengths, "terrain_class");
    }

    get trafficLevels() {
        return extractCountData(this.lengths, "traffic_level");
    }

    static getFieldName(field) {
        return getFieldName(networkReportSchema, field);
    }

    static getHelpText(field) {
        return getHelpText(networkReportSchema, field);
    }
}

export class EstradaRoadSurveyReport extends EstradaNetworkSurveyReport {
    /// 'v2' of the reports proto
    get attributesList() {
        const attributesRaw = this.getAttributesList();
        return attributesRaw.map(this.makeEstradaSurveyAttribute);
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

    get roadClasses() {
        return this.roadTypes;
    }

    get roadTypes() {
        return this.makeSpecificLengths("road_type");
    }

    get roadStatuses() {
        return this.makeSpecificLengths("road_status");
    }

    get surfaceConditions() {
        return this.makeSpecificLengths("surface_condition");
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

    /** Returns one or more collections of attributes matching the criteria
     * @param {string} primaryAttribute The primaryAttribute (within all of the attributes) to search for
     * @param {Timestamp} [date_surveyed=null] All attributes up to and including this date are acceptable (null = take them all)
     * @param {boolean} [returnAllDates=false] Return all matching attributes, false means only return the most recent
     * @param {boolean} [returnAllEntries=false] Return all entries, false means return nothing if there are only 'generated' entries
     * @return {object[]} An array of simplified attribute objects
     */
    attributes(primaryAttribute, date_surveyed = null, returnAllDates = false, returnAllEntries = false) {
        let filteredAttributes = this.attributesList.filter((attribute) => {
            return attribute.primaryAttribute === primaryAttribute;
        });

        if (filteredAttributes.length === 0) {
            return [{date_surveyed: null, attributeEntries: []}];
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

        if (date_surveyed) {
            filteredAttributes = filteredAttributes.filter((attribute) => {
                if (!attribute.dateSurveyed) {
                    return true;
                }

                return (attribute.dateSurveyed <= date_surveyed);
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
            date_surveyed: date_surveyed,
            attributeEntries: filteredAttributes
        };
    }

    static getFieldName(field) {
        return getFieldName(roadReportSchema, field);
    }

    static getHelpText(field) {
        return getHelpText(roadReportSchema, field);
    }

    makeSpecificLengths(primary_attribute, useLengthKeyAsDefault = false) {
        return extractCountData(this.lengths, primary_attribute, useLengthKeyAsDefault);
    }

    makeEstradaSurveyAttribute(pbattribute) {
        return makeEstradaObject(EstradaSurveyAttribute, pbattribute);
    }
}

export class EstradaSurveyAttribute extends Attribute {
    getId() {
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
        const pbufData = this.getDateSurveyed();
        if (!pbufData || !pbufData.getSeconds()) {
            return "";
        }
        const date = dayjs(new Date(pbufData.getSeconds() * 1000));
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

    get municipality() {
        return this.primaryAttribute === "municipality" ? this.value || gettext("Unknown") : gettext("Unknown");
    }

    get carriagewayWidth() {
        return this.primaryAttribute === "carriageway_width" ? this.value || gettext("Unknown") : gettext("Unknown");
    }

    get numberLanes() {
        return this.primaryAttribute === "number_lanes" ? this.value || gettext("Unknown") : gettext("Unknown");
    }

    get pavementClass() {
        return this.primaryAttribute === "pavement_class"
            ? gettext(choice_or_default(this.value, PAVEMENT_CLASS_CHOICES, "Unknown"))
            : gettext("Unknown");
    }

    get rainfall() {
        return this.primaryAttribute === "rainfall"
            ? gettext(this.value || "Unknown")
            : gettext("Unknown");
    }

    get trafficCounts() {
        return this.values.counts || {};
    }

    get trafficCountTotal() {
        return this.values.countTotal || 0;
    }

    get trafficDataType() {
        return this.values.trafficType || "Unknown";
    }

    get roadClass() {
        return this.roadType;
    }

    get roadType() {
        return this.primaryAttribute === "road_type"
            ? gettext(choice_or_default(this.value, ROAD_TYPE_CHOICES, "Unknown"))
            : gettext("Unknown");
    }

    get surfaceCondition() {
        return this.primaryAttribute === "surface_condition"
            ? gettext(choice_or_default(this.value, SURFACE_CONDITION_CHOICES, "Unknown"))
            : gettext("Unknown");
    }

    get surfaceType() {
        return this.primaryAttribute === "surface_type"
            ? gettext(choice_or_default(this.value, SURFACE_TYPE_CHOICES, "Unknown"))
            : gettext("Unknown");
    }

    get technicalClass() {
        return this.primaryAttribute === "technical_class"
            ? gettext(choice_or_default(this.value, TECHNICAL_CLASS_CHOICES, "Unknown"))
            : gettext("Unknown");
    }

    get terrainClass() {
        return this.primaryAttribute === "terrain_class"
            ? gettext(choice_or_default(this.value, TERRAIN_CLASS_CHOICES, "Unknown"))
            : gettext("Unknown");
    }

    get trafficLevel() {
        return this.primaryAttribute === "traffic_level"
            ? gettext(choice_or_default(this.value, TRAFFIC_LEVEL_CHOICES, "Unknown"))
            : gettext("Unknown");
    }

    static getFieldName(field) {
        return getFieldName(attributeSchema, field);
    }

    static getHelpText(field) {
        return getHelpText(attributeSchema, field);
    }
}

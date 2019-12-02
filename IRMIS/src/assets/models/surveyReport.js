import dayjs from "dayjs";

import { AttributeEntry, AttributeTable, Report } from "../../../protobuf/report_pb";

import { choice_or_default, getFieldName, getHelpText, makeEstradaObject } from "../protoBufUtilities";

import {
    ROAD_STATUS_CHOICES,
    SURFACE_CONDITION_CHOICES, SURFACE_TYPE_CHOICES,
    TECHNICAL_CLASS_CHOICES, TRAFFIC_LEVEL_CHOICES,
    PAVEMENT_CLASS_CHOICES
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

const attributeTableSchema = {
    id: { display: "Id" },
    primaryAttribute: { display: gettext("Attribute") },
    secondaryAttribute: { display: gettext("Other Attributes") },
    attributeEntries: { display: gettext("Lengths") },
};

const attributeEntrySchema = {
    id: { display: "Id" },
    surveyId: { display: "Survey Id" },
    chainageStart: { display: gettext("Chainage Start") },
    chainageEnd: { display: gettext("Chainage End") },
    lengths: { display: gettext("Lengths") },
    dateSurveyed: { display: gettext("Survey Date") },
    addedBy: { display: gettext("Added By") },
    primaryAttribute: { display: gettext("Attribute") },
    // secondaryAttributes are implied by the contents of `lengths`
};

function testKeyIsReal(key) {
    return ["0", "none", "unknown", "nan", "null", "undefined", "false"].indexOf(`${key}`.toLowerCase()) === -1;
}

function extractCountData(lengthsForType, choices) {
    const lengths = [];
    if (lengthsForType) {
        Object.keys(lengthsForType).forEach((key) => {
            let lengthKey = key;
            let lengthKeyHasValue = testKeyIsReal(lengthKey);
            let title = choice_or_default(lengthKey, choices, "Unknown").toLowerCase();

            if (title === "unknown") {
                // check if we've actually received the title instead of the key
                const invertedChoices = invertChoices(choices);
                let alternateTitle = choice_or_default(lengthKey, invertedChoices, "Unknown").toLowerCase();
                if (alternateTitle !== "unknown") {
                    title = lengthKey;
                    lengthKey = alternateTitle;
                } else if (lengthKeyHasValue) {
                    // We do have some kind of supplied key name - so we'll use it.
                    title = lengthKey.toLowerCase();
                }
            }
            lengths.push({ key: lengthKeyHasValue ? lengthKey : 0, title, distance: lengthsForType[key] });
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

    /** filter is an object(dict) of lists */
    get filter() {
        const filter = this.getFilter() || "{}";
        return JSON.parse(filter);
    }

    get lengths() {
        let lengths = "";

        try {
            lengths = this.getLengths();
        } catch {
            lengths = "";
        }

        // We can change the following to
        // whatever we consider an appropriate 'empty' collection of lengths
        lengths = lengths || '{ "surface_condition": { "None": 0 },  "surface_type": { "None": 0 },  "pavement_class": { "None": 0 } }';

        return JSON.parse(lengths);
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

    get surfaceConditions() {
        return extractCountData(this.lengths.surface_condition, SURFACE_CONDITION_CHOICES);
    }

    get surfaceTypes() {
        return extractCountData(this.lengths.surface_type, SURFACE_TYPE_CHOICES);
    }

    get pavementClasses() {
        return extractCountData(this.lengths.pavement_class, PAVEMENT_CLASS_CHOICES);
    }

    get technicalClasses() {
        return extractCountData(this.lengths.technical_class, TECHNICAL_CLASS_CHOICES);
    }

    get trafficLevels() {
        return extractCountData(this.lengths.traffic_level, TRAFFIC_LEVEL_CHOICES);
    }

    get numberLanes() {
        if (!this.lengths.number_lanes || this.lengths.number_lanes.length) {
            return [];
        }
        return this.lengths.number_lanes;
    }

    static getFieldName(field) {
        return getFieldName(networkReportSchema, field);
    }

    static getHelpText(field) {
        return getHelpText(networkReportSchema, field);
    }
}

export class EstradaRoadSurveyReport extends EstradaNetworkSurveyReport {
    get attributeTablesList() {
        const attributeTablesRaw = this.getAttributeTablesList();
        return attributeTablesRaw.map(this.makeEstradaSurveyAttributeTable);
    }

    get roadStatuses() {
        return this.makeSpecificLengths("road_status", ROAD_STATUS_CHOICES);
    }

    get surfaceConditions() {
        return this.makeSpecificLengths("surface_condition", SURFACE_CONDITION_CHOICES);
    }

    get surfaceTypes() {
        return this.makeSpecificLengths("surface_type", SURFACE_TYPE_CHOICES);
    }

    get pavementClasses() {
        return this.makeSpecificLengths("pavement_class", PAVEMENT_CLASS_CHOICES);
    }

    get technicalClasses() {
        return this.makeSpecificLengths("technical_class", TECHNICAL_CLASS_CHOICES);
    }

    get trafficLevels() {
        return this.makeSpecificLengths("traffic_level", TRAFFIC_LEVEL_CHOICES);
    }

    attributeTable(primaryAttribute) {
        const attributeTableIndex = this.attributeTablesList.findIndex((attributeTable) => {
            return attributeTable.primaryAttribute === primaryAttribute;
        });

        if (attributeTableIndex === -1) {
            return [];
        }

        return this.attributeTablesList[attributeTableIndex].attributeEntriesList;
    }

    static getFieldName(field) {
        return getFieldName(roadReportSchema, field);
    }

    static getHelpText(field) {
        return getHelpText(roadReportSchema, field);
    }

    makeSpecificLengths(primary_attribute, choices) {
        const lengthsForType = this.lengths[primary_attribute] || {}

        return extractCountData(lengthsForType, choices);
    }

    makeEstradaSurveyAttributeTable(pbattributetable) {
        return makeEstradaObject(EstradaSurveyAttributeTable, pbattributetable);
    }
}

export class EstradaSurveyAttributeTable extends AttributeTable {
    getId() {
        return `${this.primaryAttribute} ${this.secondaryAttributeList.join(", ")}`.trim();
    }

    get id() {
        return this.getId();
    }

    /** Get the 'Primary' Attribute of this attribute table,
     * this name MUST occur in the attribute_entry lengths member
     */
    get primaryAttribute() {
        return this.getPrimaryAttribute() || "";
    }

    /** Get any 'Secondary' Attributes of this attribute table,
     * these names identify attributes that are 'averaged' relative to the primary attribute
     */
    get secondaryAttributeList() {
        return this.getSecondaryAttributeList() || [];
    }

    get attributeEntriesList() {
        const attributeEntriesRaw = this.getAttributeEntriesList();
        if (attributeEntriesRaw.length === 1 && attributeEntriesRaw[0].getSurveyId() === 0) {
            // Only a single generated attribute table
            // Which means that there are actually no real attribute tables
            return [];
        }
        return attributeEntriesRaw.map(this.makeEstradaSurveyAttributeEntry);
    }

    static getFieldName(field) {
        return getFieldName(attributeTableSchema, field);
    }

    static getHelpText(field) {
        return getHelpText(attributeTableSchema, field);
    }

    makeEstradaSurveyAttributeEntry(pbattributeentry) {
        return makeEstradaObject(EstradaSurveyAttributeEntry, pbattributeentry);
    }
}

export class EstradaSurveyAttributeEntry extends AttributeEntry {
    getId() {
        return this.getSurveyId();
    }

    get id() {
        return this.getId();
    }

    get surveyId() {
        return this.getSurveyId();
    }

    get addedBy() {
        return this.getAddedBy() || "";
    }

    get chainageStart() {
        return this.getChainageStart() || 0;
    }

    get chainageEnd() {
        return this.getChainageEnd();
    }

    get length() {
        return this.chainageEnd - this.chainageStart;
    }

    get dateSurveyed() {
        const pbufData = this.getDateSurveyed();
        if (!pbufData || !pbufData.getSeconds()) {
            return "";
        }
        const date = dayjs(new Date(pbufData.getSeconds() * 1000));
        return date.isValid() ? date.format("YYYY-MM-DD") : "";
    }

    /** Get the 'Primary' Attribute of this attribute table,
     * this name MUST occur in the lengths member
     */
    get primaryAttribute() {
        return this.getPrimaryAttribute() || "";
    }

    /** Get any 'Secondary' Attributes of this attribute table,
     * these names identify attributes that are 'averaged' relative to the primary attribute
     */
    get secondaryAttributeList() {
        const allAttributes = Object.keys(this.values) || [];
        return allAttributes.filter((attribute) => attribute !== this.primaryAttribute);
    }

    get surfaceCondition() {
        return gettext(choice_or_default(this.values.surface_condition, SURFACE_CONDITION_CHOICES, "Unknown"));
    }

    get surfaceType() {
        return gettext(this.values.surface_type || "Unknown");
    }

    get pavementClass() {
        return gettext(this.values.pavement_class || "Unknown");
    }

    get technicalClass() {
        return gettext(this.values.technical_class || "Unknown");
    }

    get trafficLevel() {
        return choice_or_default(this.values.traffic_level, TRAFFIC_LEVEL_CHOICES);
    }

    get numberLanes() {
        return this.values.number_lanes || gettext("Unknown");
    }

    get values() {
        const jsonValues = this.getValues() || "{}";
        return JSON.parse(jsonValues);
    }

    static getFieldName(field) {
        return getFieldName(attributeEntrySchema, field);
    }

    static getHelpText(field) {
        return getHelpText(attributeEntrySchema, field);
    }
}

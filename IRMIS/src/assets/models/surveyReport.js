import dayjs from "dayjs";

import { Report, AttributeTable, AttributeEntry } from "../../../protobuf/report_pb";

import { choice_or_default, getFieldName, getHelpText, makeEstradaObject } from "../protoBufUtilities";

import { SURFACE_CONDITION_CHOICES, SURFACE_TYPE_CHOICES, TECHNICAL_CLASS_CHOICES, TRAFFIC_LEVEL_CHOICES } from "./road";

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

function extractCountData(lengthsForType, choices) {
    const lengths = [];
    if (lengthsForType) {
        Object.keys(lengthsForType).forEach((key) => {
            const title = choice_or_default(key, choices, "Unknown").toLowerCase();
            lengths.push({ title, distance: lengthsForType[key] });
        });
    }

    return lengths;
}

export class EstradaNetworkSurveyReport extends Report {
    getId() {
        // TODO: we want to assemble something (anything) out of the filters as an ID
        return "Network Report";
    }

    get id() {
        return this.getId();
    }

    get filter() {
        const filter = this.getFilter() || "{}";
        return JSON.parse(filter);
    }

    get lengths() {
        const lengths = this.getLengths() || { surface_condition: { None: 0 } };
        return JSON.parse(lengths);
    }

    get surfaceConditions() {
        return extractCountData(this.lengths.surface_condition, SURFACE_CONDITION_CHOICES);
    }

    get surfaceTypes() {
        return extractCountData(this.lengths.surface_type, SURFACE_TYPE_CHOICES);
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
    getId() {
        return `${this.roadCode}_${this.reportChainageStart}-${this.reportChainageEnd}`;
    }

    get id() {
        return this.getId();
    }

    get roadCode() {
        return this.filter.road_code || "";
    }

    get reportChainageStart() {
        return this.filter.report_chainage_start || 0;
    }

    get reportChainageEnd() {
        return this.filter.report_chainage_end || 0;
    }

    get attributeTablesList() {
        const attributeTablesRaw = this.getAttributeTablesList();
        return attributeTablesRaw.map(this.makeEstradaSurveyAttributeTable);
    }
    
    get surfaceConditions() {
        const primary_attribute = "surface_condition";

        const lengthsForType = {}
        this.surfaceConditionsList.attributeEntriesList.forEach((attributeEntry) => {
            const typeKey = attributeEntry.values[primary_attribute];
            lengthsForType[typeKey] = (lengthsForType[typeKey] || 0) + attributeEntry.length;
        });
        console.log(JSON.stringify(lengthsForType));
           
        return extractCountData(lengthsForType, SURFACE_CONDITION_CHOICES);
    }

    get surfaceConditionsList() {
        const primary_attribute = "surface_condition";
        const attributes = this.attributeTablesList.find((attributeTable) => {
            return attributeTable.primaryAttribute === primary_attribute;
        }) || [];

        return attributes
    }

    static getFieldName(field) {
        return getFieldName(roadReportSchema, field);
    }
    
    static getHelpText(field) {
        return getHelpText(roadReportSchema, field);
    }
        
    makeEstradaSurveyAttributeTable (pbattributetable) {
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
     * */
    get primaryAttribute() {
        return this.getPrimaryAttribute() || "";
    }

    /** Get any 'Secondary' Attributes of this attribute table,
     * these names identify attributes that are 'averaged' relative to the primary attribute
     * */
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

    makeEstradaSurveyAttributeEntry (pbattributeentry) {
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
        if (!pbufData || !pbufData.array) {
            return "";
        }
        let date = dayjs(new Date(pbufData.array[0] * 1000));
        return date.isValid() ? date.format('YYYY-MM-DD') : "";
    }

    /** Get the 'Primary' Attribute of this attribute table,
     * this name MUST occur in the lengths member
     * */
    get primaryAttribute() {
        return this.getPrimaryAttribute() || "";
    }

    /** Get any 'Secondary' Attributes of this attribute table,
     * these names identify attributes that are 'averaged' relative to the primary attribute
     * */
    get secondaryAttributeList() {
        const allAttributes = Object.keys(this.values) || [];
        return allAttributes.filter((attribute) => attribute != this.primaryAttribute);
    }

    get surfaceCondition() {
        return window.gettext(choice_or_default(this.values.surface_condition, SURFACE_CONDITION_CHOICES, "Unknown"));
    }

    get surfaceType() {
        return choice_or_default(this.values.surface_type, SURFACE_TYPE_CHOICES);
    }

    get technicalClass() {
        return choice_or_default(this.values.technical_class, TECHNICAL_CLASS_CHOICES);
    }

    get trafficLevel() {
        return choice_or_default(this.values.traffic_level, TRAFFIC_LEVEL_CHOICES);
    }

    get numberLanes() {
        return this.values.number_lanes;
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

import dayjs from "dayjs";

import { Report, TableEntry } from "../../../protobuf/survey_pb";

import { choice_or_default, getFieldName, getHelpText, makeEstradaObject } from "../protoBufUtilities";

import { SURFACE_CONDITION_CHOICES } from "./road";

const surveyReportSchema = {
    id: { display: "Id" },
    roadCode: { display: gettext("Road Code") },
    reportChainageStart: { display: gettext("Chainage Start") },
    reportChainageEnd: { display: gettext("Chainage End") },
    counts: { display: gettext("Counts") },
    percentages: { display: gettext("Percentages") },
    tableList: { display: gettext("Table") },
};

const attributeEntrySchema = {
    id: { display: "Id" },
    surveyId: { display: "Survey Id" },
    chainageStart: { display: gettext("Chainage Start") },
    chainageEnd: { display: gettext("Chainage End") },
    surfaceCondition: { display: gettext("Surface Condition") },
    dateSurveyed: { display: gettext("Survey Date") },
    addedBy: { display: gettext("Added By") },
};

export class EstradaSurveyReport extends Report {
    getId() {
        return `${this.getRoadCode()}_${this.getReportChainageStart()}-${this.getReportChainageEnd()}`;
    }

    get id() {
        return this.getId();
    }

    get roadCode() {
        return this.getRoadCode();
    }

    get reportChainageStart() {
        return this.getReportChainageStart();
    }

    get reportChainageEnd() {
        return this.getReportChainageEnd();
    }

    get counts() {
        let counts = [];
        try {
            counts = JSON.parse(this.getCounts());
        } catch {
            // This is the correct response on error
            counts = {None:0};
        }
        return counts;
    }

    get conditions() {
        const conditions = [];
        const counts = this.counts;
        Object.keys(counts).forEach((key) => {
            let conditionTitle = (choice_or_empty(key, SURFACE_CONDITION_CHOICES) || key).toLowerCase();
            let newKey = key;
            if (conditionTitle === "none") {
                conditionTitle = window.gettext("unknown");
                newKey = "0";
            }
            conditions.push({ key: newKey, title: conditionTitle, distance: counts[key] });
        });
        return conditions;
    }

    get percentages() {
        let percentages = [];
        try {
            percentages = JSON.parse(this.getPercentages());
        } catch {
            percentages = [];
        }
        return percentages;
    }

    get tableList() {
        const tableListRaw = this.getTableList();
        if (tableListRaw.length === 1 && tableListRaw[0].getSurveyId() === 0) {
            // Only a single generated survey segment
            // Which means that there are actually no real survey segments
            return [];
        }
        return tableListRaw.map(this.makeEstradaSurveyReportTableEntry);
    }
    
    makeEstradaSurveyReportTableEntry (pbtableentry) {
        return makeEstradaObject(EstradaSurveyReportTableEntry, pbtableentry);
    }

    static getFieldName(field) {
        return getFieldName(surveyReportSchema, field);
    }
    
    static getHelpText(field) {
        return getHelpText(surveyReportSchema, field);
    }
}

export class EstradaSurveyReportTableEntry extends TableEntry {
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
        return this.getChainageStart();
    }

    get chainageEnd() {
        return this.getChainageEnd();
    }

    get dateSurveyed() {
        const pbufData = this.getDateSurveyed();
        if (!pbufData || !pbufData.array) {
            return "";
        }
        let date = dayjs(new Date(pbufData.array[0] * 1000));
        return date.isValid() ? date.format('YYYY-MM-DD') : "";
    }

    get surfaceCondition() {
        return gettext(choice_or_default(this.values.surface_condition, SURFACE_CONDITION_CHOICES, "Unknown"));
    }
    
    static getFieldName(field) {
        return getFieldName(attributeEntrySchema, field);
    }

    static getHelpText(field) {
        return getHelpText(attributeEntrySchema, field);
    }
}

import dayjs from "dayjs";

import { Report, TableEntry } from "../protobuf/survey_pb";

import { choice_or_empty, makeEstradaObject } from "./assets/protoBufUtilities";

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

export class EstradaSurveyReport extends Report {
    getId() {
        return this.getRoadCode()
            ? `${this.getRoadCode()}_${this.getReportChainageStart()}-${this.getReportChainageEnd()}`
            : null;
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
        let tableListRaw = [];
        try {
            let tableListRaw = this.getTableList();
            if (tableListRaw.length === 0 || (tableListRaw.length === 1 && tableListRaw[0].getSurveyId() === 0)) {
                // If there's only a single generated survey segment
                // that means that there are actually no real survey segments
                tableListRaw = [];
            } else {
                tableListRaw = tableListRaw.map(makeEstradaSurveyReportTableEntry);
            }
        } catch {
            // This is the correct response on error
            tableListRaw = [];
        }
        return tableListRaw;
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
        let conditionTitle = (choice_or_empty(this.getSurfaceCondition(), SURFACE_CONDITION_CHOICES) || this.getSurfaceCondition()).toLowerCase();
        if (conditionTitle === "none") {
            conditionTitle = "unknown";
        }
        return window.gettext(conditionTitle[0].toUpperCase() + conditionTitle.substring(1));
    }
}

export function getFieldName(field) {
    return (surveyReportSchema[field]) ? surveyReportSchema[field].display : "";
}

export function getHelpText(field) {
    return (surveyReportSchema[field]) ? surveyReportSchema[field].help_text : "";
}

export function makeEstradaSurveyReportTableEntry (pbtableentry) {
    return makeEstradaObject(EstradaSurveyReportTableEntry, pbtableentry);
}

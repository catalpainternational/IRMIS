import { Report, TableEntry } from "../protobuf/survey_pb";

import { choice_or_empty } from "./assets/protoBufUtilities";

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
            // Use dummy data
            counts = JSON.parse('[["1", 25600], ["2", 60000], ["3", 25300], ["4", 30000], ["0", 45000]]');
            // This is the correct response on error
            // counts = [];
        }

        return counts;
    }

    get conditions() {
        const conditions = [];
        this.counts.forEach((record) => {
            let conditionTitle = choice_or_empty(record[0], SURFACE_CONDITION_CHOICES) || record[0];
            if (conditionTitle === "0") {
                // What is the correct code for 'unknown'?
                conditionTitle = "unknown";
            }
            conditions.push({ surface: conditionTitle.toLowerCase(), distance: record[1] });
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
        return this.getTableList();
    }
}

export function getFieldName(field) {
    return (surveyReportSchema[field]) ? surveyReportSchema[field].display : "";
}

export function getHelpText(field) {
    return (surveyReportSchema[field]) ? surveyReportSchema[field].help_text : "";
}

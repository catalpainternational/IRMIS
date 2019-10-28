import { Report, TableEntry } from "../protobuf/survey_pb";

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
        return this.getCounts();
    }

    get percentages() {
        return this.getPercentages();
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

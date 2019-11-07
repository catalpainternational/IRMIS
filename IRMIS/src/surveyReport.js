import dayjs from "dayjs";

import { Report, TableEntry } from "../protobuf/report_pb";

import { choice_or_default, getFieldName, getHelpText, makeEstradaObject } from "./assets/protoBufUtilities";

import { SURFACE_CONDITION_CHOICES } from "./road";

const networkReportSchema = {
    filter: { display: gettext("Filter") },
    counts: { display: gettext("Counts") },
};

const roadReportSchema = {
    id: { display: "Id" },
    roadCode: { display: gettext("Road Code") },
    reportChainageStart: { display: gettext("Chainage Start") },
    reportChainageEnd: { display: gettext("Chainage End") },
    counts: { display: gettext("Counts") },
    tableList: { display: gettext("Table") },
};

function extractCountData(countsForType, choices) {
    const counts = [];
    if (countsForType) {
        Object.keys(countsForType).forEach((key) => {
            const title = choice_or_default(key, choices, "Unknown").toLowerCase();
            counts.push({ title, distance: countsForType[key] });
        });
    }

    return counts;
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

    get counts() {
        const counts = this.getCounts() || { surface_condition: { None: 0 } };
        return JSON.parse(counts);
    }

    get surfaceConditions() {
        return extractCountData(this.counts.surface_condition, SURFACE_CONDITION_CHOICES);
    }

    get surfaceTypes() {
        return extractCountData(this.counts.surface_type, SURFACE_TYPE_CHOICES);
    }

    get technicalClasses() {
        return extractCountData(this.counts.technical_class, TECHNICAL_CLASS_CHOICES);
    }

    get trafficLevels() {
        return extractCountData(this.counts.traffic_level, TRAFFIC_LEVEL_CHOICES);
    }

    get numberLanes() {
        if (!this.counts.number_lanes || this.counts.number_lanes.length) {
            return [];
        }
        return this.counts.number_lanes;
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

    get roadCode() {
        return this.filter.road_code || "";
    }

    get reportChainageStart() {
        return this.filter.report_chainage_start || 0;
    }

    get reportChainageEnd() {
        return this.filter.report_chainage_end || 0;
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
    
    static getFieldName(field) {
        return getFieldName(roadReportSchema, field);
    }
    
    static getHelpText(field) {
        return getHelpText(roadReportSchema, field);
    }
        
    makeEstradaSurveyReportTableEntry (pbtableentry) {
        return makeEstradaObject(EstradaSurveyReportTableEntry, pbtableentry);
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
}

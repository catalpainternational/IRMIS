import { getRoadSurveyReports, getSurveyMetadata, getSurveysMetadata, postSurveyData, putSurveyData } from "./assets/surveyAPI";

let surveys = {}

export function getSurvey(id) {
    let survey = surveys[id];
    if(survey) return Promise.resolve(survey);
    return getSurveyMetadata(id);
}

export function getRoadSurveys(roadId) {
    return Promise.resolve(getSurveysMetadata(roadId))
        .then(surveys => {
            return surveys;
        });
}

export function createSurvey(survey) {
    return Promise.resolve(postSurveyData(survey))
        .then(survey => {
            surveys[survey.getId()] = survey;
            return survey;
        });
}

export function updateSurvey(survey) {
    return Promise.resolve(putSurveyData(survey))
        .then(survey => {
            surveys[survey.getId()] = survey;
            return survey;
        });
}

export function getRoadSurveyReport(roadCode) {
    return Promise.resolve(getRoadSurveyReports(roadCode))
        .then((surveyReportList) => {
            // document.dispatchEvent(new CustomEvent("estrada.auditTable.roadAuditDataAdded", {detail: {auditList}}));
            return surveyReportList;
        });
}
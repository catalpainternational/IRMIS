import { getSurveyMetadata, getSurveysMetadata, getSurveysMetadataChunks, postSurveyData } from "./assets/surveyAPI";

let surveys = {}

// Get the survey metadata chunk details
// getSurveysMetadataChunks()
//     .then(chunks => {
//         // for each chunk, download the surveys
//         chunks.forEach(chunk => {
//             getSurveysMetadata(chunk.survey_type)
//             .then(surveyList => {
//                 // add the surveys to the survey manager
//                 addSurveyMetadata(surveyList);
//             });
//         });
//     });

export function getSurvey(id) {
    let survey = surveys[id];
    if(survey) return Promise.resolve(survey);
    return getSurveyMetadata(id);
}

export function getRoadSurveys(roadId) {
    return Promise.resolve(getSurveysMetadata(roadId))
        .then(surveys => {
            // document.dispatchEvent(new CustomEvent("estrada.table.surveyMetaDataUpdated", {detail: {survey}}));
            return surveys;
        });
}

export function saveSurvey(survey) {
    return Promise.resolve(postSurveyData(survey))
        .then(survey => {
            surveys[survey.getId()] = survey;
            // document.dispatchEvent(new CustomEvent("estrada.table.surveyMetaDataUpdated", {detail: {survey}}));
            return survey;
        });
}

import {getAssetSurveys} from "../surveyManager";
import {getAssetReport} from "../reportManager";
import {updateReportAttributeSummary} from "../roadAttributes";


export function getSurveysForAsset(
    state: { [name: string]: any }, identifiers: { [name: string]: any }) {
    const roadId = state.road.id;

    return getAssetSurveys(roadId, identifiers.primaryAttribute)
        .then((surveyData) => {
            if (surveyData) {
                state.pendingRows = surveyData.map((data) => {
                    // @ts-ignore ts(7053) on the part `data[identifiers.reportAttribute]`
                    data.title = data[identifiers.reportAttribute] as string
                        || data.values[identifiers.primaryAttribute] as string
                        || "";
                    return data;
                });

                const eventName = `${identifiers.allDataTableId}.dataAdded`;
                const eventDetail = {detail: {pendingRows: state.pendingRows, clearRows: true}};
                document.dispatchEvent(new CustomEvent(eventName, eventDetail));

                state.error = false;
            } else {
                state.error = true;
            }
            state.loading = false;
            return Promise.resolve(state.error);
        }).catch(() => {
            state.loading = false;
            state.error = true;
            return Promise.resolve(state.error);
        });
}

function getSurveyReportsForAsset(state: { [name: string]: any }, identifiers: { [name: string]: any }) {
    const editingRoad = state.editingRoad || state.road;
    const filters = {
        reportassettype: ["ROAD"],
        primaryattribute: identifiers.primaryAttribute,
        asset_code: editingRoad.code,
        // Use the raw chainage (not the formatted one)
        chainagestart: editingRoad.getLinkStartChainage(),
        chainageend: editingRoad.getLinkEndChainage(),
    };

    return getAssetReport(filters)
        .then((surveyReportData) => {
            if (surveyReportData) {
                const haveLengths = !!surveyReportData.lengths;
                // @ts-ignore ts(7053) on the part `surveyReportData[identifiers.reportAttribute]`
                let reportAttributes = surveyReportData[identifiers.reportAttribute];
                if (!reportAttributes || !reportAttributes.length) {
                    reportAttributes = identifiers.emptyAttributes;
                }

                if (haveLengths && reportAttributes.length) {
                    updateReportAttributeSummary(state, identifiers.reportAttribute, reportAttributes);

                    if (identifiers.stackedBarId) {
                        const barEventName = `${identifiers.stackedBarId}.dataUpdated`;
                        const barEventDetail = { detail: { entries: state[identifiers.reportAttribute] } };
                        document.dispatchEvent(new CustomEvent(barEventName, barEventDetail));
                    }

                    state.reportRows = surveyReportData.attributes(identifiers.primaryAttribute).attributeEntries;

                    const eventName = `${identifiers.reportDataTableId}.dataAdded`;
                    const eventDetail = {detail: {pendingRows: state.reportRows, clearRows: true}};
                    document.dispatchEvent(new CustomEvent(eventName, eventDetail));

                    if (surveyReportData.id === null) {
                        // An id of null should tell us that there was an error fetching the data
                        state.error = true;
                        state.showFeedback = true;
                    }
                }
                state.error = false;
            } else {
                state.error = true;
            }
            state.loading = false;
            return Promise.resolve(state.error);
        }).catch(() => {
            state.loading = false;
            state.error = true;
            return Promise.resolve(state.error);
        });
}

export function surveysAndReportRefresh(state: { [name: string]: any }, identifiers: { [name: string]: any }) {
    // updateReportAttributeSummary is called a second time within getSurveyReportsForAsset
    // once we have all of the data
    updateReportAttributeSummary(state, identifiers.reportAttribute, identifiers.emptyAttributes);

    const surveyPromise = getSurveysForAsset(
        state, identifiers);
    const surveyReportsPromise = getSurveyReportsForAsset(
        state, identifiers);

    return Promise.all([surveyPromise, surveyReportsPromise]);
}


export function checkRequiredFields(fieldNames: string[], data: { [name: string]: any }) {
    return fieldNames.filter((fieldName) => {
        return typeof data[fieldName] === "undefined" || data[fieldName] === null;
    });
}
export function updateReportAttributeSummary(state, reportAttribute, reportAttributes) {
    state[reportAttribute] = state[reportAttribute] || [];
    state[reportAttribute].length = 0;
    reportAttributes.forEach((attribute) => {
        state[reportAttribute].push(attribute);
    });
    drawReportAttributeSummary(state, reportAttribute);
}

function drawReportAttributeSummary(state, reportAttribute) {
    // First just clean all the distance values and get the total
    state.surveyTotalDistance = 0;
    state[reportAttribute] = state[reportAttribute] || [];
    state[reportAttribute].forEach((attribute) => {
        // all distances are in meters
        attribute.distance = Math.round(attribute.distance);
        state.surveyTotalDistance += attribute.distance;
    });
    state.surveyTotalDistance = Math.round(state.surveyTotalDistance);

    // Then calculate everything else
    state[reportAttribute].forEach((attribute) => {
        const surfaceTitle = window.gettext(attribute.title[0].toUpperCase() + attribute.title.substring(1));
        if (state.surveyTotalDistance > 0) {
            attribute.percent = Math.round((attribute.distance / state.surveyTotalDistance) * 10000) / 100;
            // the calculated label shows distance in km
            attribute.label = `${surfaceTitle} (${attribute.distance / 1000}km/${attribute.percent}%)`;
        } else {
            // 100% of 0km - but this won't appear in the label
            attribute.percent = 100;
            // the calculated label shows distance in km
            attribute.label = `${surfaceTitle} (0km)`;
        }
    });
}

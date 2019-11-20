export function updateReportAttributeSummary(state, reportAttribute, reportAttributes) {
    state[reportAttribute] = state[reportAttribute] || [];
    state[reportAttribute].length = 0;
    reportAttributes.forEach((attribute) => {
        state[reportAttribute].push(attribute);
    });
}

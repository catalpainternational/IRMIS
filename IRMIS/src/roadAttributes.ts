export function updateReportAttributeSummary(
    state: { [name: string]: any }, reportAttribute: string, reportAttributes: string[]) {
    state[reportAttribute] = state[reportAttribute] || [];
    state[reportAttribute].length = 0;
    reportAttributes.forEach((attribute) => {
        state[reportAttribute].push(attribute);
    });
}

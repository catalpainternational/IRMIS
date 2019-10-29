/** utility function to pick from choices if value is truthy, or return empty string */
export function choice_or_empty(value, choices) {
    return value ? choices[value] : "";
}

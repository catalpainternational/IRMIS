/** utility function to pick from choices if value is truthy, or return default string
 * the default for defaultValue is empty string ""
*/
export function choice_or_default(value, choices, defaultValue = "") {
    return value ? choices[value] || defaultValue : defaultValue;
}

export function toChainageFormat(value) {
    const distance = parseFloat(value).toFixed(0);
    const meters = `000${distance.substr(-3)}`.substr(-3);
    const kilometers = `${distance.substr(0, distance.length - 3)}` || 0;

    return `${kilometers}+${meters}`;
}

export function makeEstradaObject(estradaObjectType, protoBufSource) {
    let estradaObject = Object.create(estradaObjectType.prototype);
    Object.assign(estradaObject, protoBufSource);

    return estradaObject;
}

export function getFieldName(schema, field) {
    return (schema[field]) ? schema[field].display : "";
}

export function getHelpText(schema, field) {
    return (schema[field]) ? schema[field].help_text : "";
}

export function humanizeChoices(schema, field, valueKey = false, displayKey = false) {
    let values = {};
    valueKey = valueKey || 0;
    displayKey = displayKey || 1;
    schema[field].options.forEach((o) => { values[o[valueKey]] = o[displayKey]; });

    return values;
}

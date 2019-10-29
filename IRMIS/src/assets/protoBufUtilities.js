/** utility function to pick from choices if value is truthy, or return empty string */
export function choice_or_empty(value, choices) {
    return value ? choices[value] : "";
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


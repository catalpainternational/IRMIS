import { Projection } from "../../protobuf/roads_pb";

/** utility function to pick from choices if value is truthy, or return default string
 * the default for defaultValue is empty string ""
 */
export function choice_or_default(value: string, choices: { [name: string]: any }, defaultValue = ""): string {
    return "" + (value ? choices[value] || defaultValue : defaultValue);
}

export function invertChoices(choices: { [name: string]: any }) {
    const invertedChoices: { [name: string]: any } = {};
    Object.keys(choices).forEach((key) => {
        invertedChoices[choices[key]] = key;
    });

    return invertedChoices;
}

export function toChainageFormat(value: any, thousandsSeparator = ",") {
    if (typeof value === "undefined" || value === null) {
        return "";
    }

    const distance = parseFloat(value).toFixed(0);
    const meters = `000${distance.substr(-3)}`.substr(-3);
    const kilometers = (`${distance.substr(0, distance.length - 3)}` || 0)
        .toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, `$1${thousandsSeparator}`);

    return `${kilometers}+${meters}`;
}

export function makeEstradaObject(
    estradaObjectType: { [name: string]: any },
    protoBufSource: { [name: string]: any },
): { [name: string]: any } {
    const estradaObject = Object.create(estradaObjectType.prototype);
    Object.assign(estradaObject, protoBufSource);

    return estradaObject;
}

export function getFieldName(schema: { [name: string]: any }, field: string): string {
    return (schema[field]) ? schema[field].display : "";
}

export function getHelpText(schema: { [name: string]: any }, field: string): string {
    return (schema[field]) ? schema[field].help_text : "";
}

export function humanizeChoices(
    schema: { [name: string]: any },
    field: string,
    valueKey: any = false,
    displayKey: any = false,
) {
    const values: { [name: string]: any } = {};
    valueKey = valueKey || 0;
    displayKey = displayKey || 1;
    if (schema[field] && schema[field].options) {
        schema[field].options.forEach((o: any) => { values[o[valueKey]] = o[displayKey]; });
    }

    return values;
}

/** Deep copy the supplied data to a new object
 *  Prefers to use protobuf .cloneMessage
 */
export function cloneData(data: { [name: string]: any }): { [name: string]: any } {
    if (data.cloneMessage) {
        return data.cloneMessage();
    }

    return JSON.parse(JSON.stringify(data));
}

export function projectionToCoordinates(proj: Projection): [number, number] {
    return [proj.getX(), proj.getY()];
}

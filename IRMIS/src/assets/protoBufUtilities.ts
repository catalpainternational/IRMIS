import { Projection } from "../../protobuf/roads_pb";
import { Point } from "../../protobuf/structure_pb";
import { EstradaProjection } from "./models/road";
import { EstradaPoint } from "./models/structures";

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
    protoBufSource?: { [name: string]: any },
): { [name: string]: any } {
    const estradaObject = Object.create(estradaObjectType.prototype);
    if (protoBufSource) {
        const protoBufDeepClone = JSON.parse(JSON.stringify(protoBufSource));
        Object.assign(estradaObject, protoBufDeepClone);
    }

    return estradaObject;
}

/** This compares two objects assumed to be protobuf type objects for data equivalence
 *
 * Note: This only compares the `array` member of each object (assuming they have one)
 * If they do not have an `array` member then a dummy array is compared which will result
 * in a false being returned for the comparison
 */
export function compareProtoBufObjects(a: { [name: string]: any }, b: { [name: string]: any }) {
    const aJson = JSON.stringify(JSON.parse(JSON.stringify(a)).array || ["a"]);
    const bJson = JSON.stringify(JSON.parse(JSON.stringify(b)).array || ["b"]);

    return aJson !== bJson;
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
        schema[field].options.forEach((o: any) => {
            const newValueKey = o[valueKey].toString();
            values[newValueKey] = o[displayKey];
        });
    }

    return values;
}

export function projectionToCoordinates(
    proj: Projection | Point | EstradaProjection | EstradaPoint): [number, number] {
    return [proj.getX(), proj.getY()];
}

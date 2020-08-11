/** Dispatch a CustomEvent
 * @param {string} eventName - the name of the event to raise
 * @param {object} eventDetail - the detail to provide with the event, set to undefined if no detail to be provided
 * @param {boolean} [fireAndForget = true] - whether to send the event asychronously or not
 * @param {EventTarget} [eventTarget = document] - the event target to 'use' to dispatch the event from
 */
export function dispatch(
    eventName: string,
    eventDetail: EventDetail,
    fireAndForget: boolean = true,
    eventTarget: EventTarget = document): void {
    if (fireAndForget) {
        setTimeout(() => {
            eventTarget.dispatchEvent(new CustomEvent(eventName, eventDetail));
        }, 0);
    } else {
        eventTarget.dispatchEvent(new CustomEvent(eventName, eventDetail));
    }
}

export class EventDetail {
    public detail: { [name: string]: any } = {};
}

/** Test the supplied string meets the numeric field requirements
 * @param {string} text - the supplied string to test
 * @param {number} limit - the maximum number of digits allowed (including after the decimal place)
 * @param {number} [decimals = 0] - the maximum number of digits allowed after the decimal point
 */
export function withinMaxDigits(text: string, limit: number, decimals: number = 0): boolean {
    if (limit < 1 || limit > 20) {
        throw new RangeError("limit must be greater than 0 and less than 20");
    }
    if (decimals < 0 || decimals > limit) {
        throw new RangeError("decimals must be greater than or equal to 0 and less than limit");
    }
    return (new RegExp(`^\\d{0,${(limit - decimals)}}(\\.\\d{0,${decimals}})?$`).test(text));
}

/** Test the supplied string meets the requirements
 * @param {string} text - the supplied string to test
 */
export function containsWhiteSpaces(text: string) {
    return /\s/.test(text);
}

/** Deep copy the supplied data to a new object
 */
export function copyData<T>(data: T): T {
    return JSON.parse(JSON.stringify(data)) as T;
};

/** Format the supplied number with dots for thousands separator and comma for decimal points
 * Works for numbers with 3 decimal points maximum
 * @param {number} value -the value to be formatted
 */
export function formatNumber(value: any) {
    return value.toString().replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, ".");
};

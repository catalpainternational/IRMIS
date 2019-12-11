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

import dayjs from "dayjs";

export function maxDate() {
    return new Date().toISOString().substring(0, 10);
}

export function currentDate() {
    return dayjs(new Date()).format('YYYY-MM-DD');
}

export function currentDateTime() {
    return dayjs(new Date()).format('DD MMMM YYYY [at] HH:mm');
}

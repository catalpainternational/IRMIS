import { formatNumber } from "../assets/utilities";

window.addEventListener("load", () => {
    const valuesToFormat = document.getElementsByClassName("to-format");

    for (const element of valuesToFormat) {
        const elementText = element.innerText;

        if (elementText) {
            const value = element.innerText.split(" ");
            let formattedValue;

            if (value.length === 1) { // e.g. 90000
                formattedValue = formatNumber(value[0]);
                element.innerText = formattedValue;
            } else if (value.length === 2) { // e.g. $ 90000 or 25 %
                if (value[0] === "$") {
                    formattedValue = formatNumber(value[1]);
                    element.innerText = value[0] + " " + formattedValue;
                } else {
                    formattedValue = formatNumber(value[0]);
                    element.innerText = formattedValue + " " + value[1];
                }
            }
        }
    }
});

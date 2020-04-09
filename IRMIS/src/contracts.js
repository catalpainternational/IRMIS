import "./contracts/side_menu";
import "./contracts/feedback";
import "./contracts/select2";
import "./contracts/table";
import "./contracts/modal";
import "./contracts/form";
import "./contracts/nav";
import "./top_menu";

window.addEventListener("load", () => {
    const printButton = document.getElementsByClassName("print-profile").item(0);
    const navigationLink = document.getElementsByClassName("discard-link");

    window.goBack = () => window.location.pathname = "";

    if (printButton) {
        printButton.addEventListener("click", () => {
            window.print();
        });
    }

    navigationLink.forEach(link => {
        link.addEventListener("click", () => {
            document.dispatchEvent(new CustomEvent("compare-changes", { detail: { nextUrl: link.dataset.back } }));
        });
    });
});

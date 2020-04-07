import "./contracts/side_menu";
import "./contracts/select2";
import "./contracts/table";
import "./contracts/modal";
import "./contracts/form";
import "./top_menu";

const printButton = document.getElementsByClassName("print-profile").item(0);

window.goBack = () => window.location.pathname = "";

if (printButton) {
    printButton.addEventListener("click", () => {
        window.print();
    });
}

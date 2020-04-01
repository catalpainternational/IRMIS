import "select2/dist/js/select2.full.min.js";
import $ from "jquery";

window.addEventListener("load", () => {
    $("#id_projects").select2({
        width: "100%",
        containerCssClass: "form-control contracts-select2",
        dropdownCssClass: "contracts-dropdown-select2",
    });
    $("#id_projects").on('select2:select', toggleMultipleSelect2);
    $("#id_projects").on('select2:unselect', toggleMultipleSelect2);
});

function toggleMultipleSelect2(e) {
    const selectElement = e.currentTarget;
    const inputElement = selectElement.nextSibling.children.item(0).firstElementChild;

    if (selectElement.value !== "") {
        inputElement.classList.add("active");
    } else {
        inputElement.classList.remove("active");
    }
};

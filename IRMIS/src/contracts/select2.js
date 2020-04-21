import "select2/dist/js/select2.full.min.js";
import $ from "jquery";

const contractSelects = {
    id_projects: {
        style: {
            width: "100%",
            containerCssClass: "form-control contracts-select2",
            dropdownCssClass: "contracts-dropdown-select2",
        },
        on: toggleMultipleSelect2,
        off: toggleMultipleSelect2,
    }
};

window.addEventListener("load", () => {
    Object.keys(contractSelects).forEach((selectKey) => {
        const tagId = `#${selectKey}`;
        $(tagId).select2(contractSelects[selectKey].style);
        $(tagId).on('select2:select', contractSelects[selectKey].on);
        $(tagId).on('select2:unselect', contractSelects[selectKey].off);
    });
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

const asset_manager = document.getElementById("asset_manager_button");
const reports = document.getElementById("reports_button");
const menuToggle = document.getElementById("topmenu_toggle");
const dropdown = document.getElementById("settings");

window.addEventListener("load", function() {
    menuToggle.addEventListener("click", () => {
        function clickOutside(e) {
            if (!menuToggle.contains(e.target)) {
                dropdown.hidden = true;
            }
        }

        if (dropdown.hidden) document.addEventListener("click", clickOutside);
        else document.removeEventListener("click", clickOutside);

        dropdown.hidden = !dropdown.hidden;
    });

    dropdown.addEventListener("click", (e) => {
        e.stopPropagation();
    });

    asset_manager.addEventListener("click", (e) => {
        if (!asset_manager.classList.contains("selected")) {
            asset_manager.classList.add("selected");
            reports.classList.remove("selected");
        }
    });

    reports.addEventListener("click", (e) => {
        if (!reports.classList.contains("selected")) {
            reports.classList.add("selected");
            asset_manager.classList.remove("selected");
        }
    });

    hashCheck();
});

function hashCheck() {
    if (/#reports/.exec(location.hash)) reports.classList.add("selected");
    else asset_manager.classList.add("selected");
}

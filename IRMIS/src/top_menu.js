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
});

dropdown.addEventListener("click", (e) => {
    e.stopPropagation();
});

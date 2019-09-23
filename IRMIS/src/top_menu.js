window.addEventListener("load", function() {
    document.getElementById("topmenu_toggle").addEventListener("click", () => {
        var dropdown = document.getElementById("settings");
        dropdown.hidden = !dropdown.hidden;
    });
});

document.getElementById("settings").addEventListener("click", (e) => {
    e.stopPropagation();
});

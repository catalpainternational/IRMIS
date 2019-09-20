window.addEventListener('load', function() {
    document.querySelector('#topmenu_toggle').addEventListener('click', () => {
        var dropdown = document.getElementById("settings");
        dropdown.hidden = !dropdown.hidden;
    });
});

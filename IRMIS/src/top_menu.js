window.addEventListener('load', function() {
    document.querySelector('#topmenu_toggle').addEventListener('click', () => {
        var dropdown = document.getElementById("dropdown-menu");
        dropdown.hidden = !dropdown.hidden;
    });
});

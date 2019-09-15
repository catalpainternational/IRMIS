import $ from "jquery";

$(document).ready(function(){
    $('#topmenu_toggle').click(() => {
        var dropdown = document.getElementById("dropdown-menu");
        dropdown.hidden = !dropdown.hidden;
    });
});


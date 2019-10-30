function desplegar(nombre_desplegable) {
    $('[id="div_' + nombre_desplegable + '"]').toggle();
}

function check_pass(element) {
    pass = element.value.toString();

    level1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];
    level2 = ['$', '#', '@', '!', '(', ')', '|', ':', '"', '}', '{'];

    // Check level2
    for (cha2 in level2) {
        console.log("Testing: " + level2[cha2]);
        if (pass.includes(level2[cha2])) {
            $("#anal").text('VERY GOOD!');
            return;
        }
    }

    // Check level1
    for (cha1 in level1) {
        console.log("Testing: " + level1[cha1]);
        if (pass.includes(level1[cha1])) {
            $("#anal").text('Not bad');
            return;
        }
    }

    $("#anal").text('Weak password');
}

// Call inc on the start
$(document).ready(function () {
    (function () {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#current").text(this.responseText);
            }
        };
        xhttp.open("GET", "increment", true);
        xhttp.send();
    
        // Call yourself in 3 secs
        setTimeout(arguments.callee, 3000);
    })();
});
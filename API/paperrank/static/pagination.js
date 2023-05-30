var table = document.getElementById("journal-table-body");
var paginationContainer = document.getElementById("pagination-container");
var paginationButtons = paginationContainer.getElementsByClassName("btn-pag");

// Define la cantidad de revistas por página
var itemsPerPage = 9 * 2;
var pageCount = Math.ceil(table.rows.length / itemsPerPage);
var contador = 1;

// Función para mostrar la página específica
function showPage(page) {
    var startIndex = (page - 1) * itemsPerPage;
    var endIndex = startIndex + itemsPerPage;

    // Oculta todas las filas de la tabla
    for (var i = 0; i < table.rows.length; i++) {
        table.rows[i].style.display = "none";
    }

    // Muestra las filas de la página actual
    for (var j = startIndex; j < endIndex && j < table.rows.length; j++) {
        table.rows[j].style.display = "";
    }

    // Actualiza la clase "active" en los botones de paginación
    for (var k = 0; k < paginationButtons.length; k++) {
        paginationButtons[k].classList.remove("active");
    }
    paginationButtons[page - 1].classList.add("active");
}


function previousPage() {
    var currentPage = contador;
    if (currentPage > 1) {
        contador = contador - 1;
        showPage(currentPage - 1);
    }
}

function nextPage() {
    var currentPage = contador;
    if (currentPage < pageCount) {
        contador = contador + 1;
        showPage(currentPage + 1);
    }
}

function firstPage() {
    if (contador > 1) {
        contador = 1;
        showPage(1);
    }
}

function lastPage() {
    if (contador < pageCount) {
        contador = pageCount;
        showPage(pageCount);
    }
}

// Mostrar la primera página al cargar la página
showPage(1);



// Cambio del botón de acceso a la lista de revistas
$(function () {
    $('#prev-pag').hover(
        function () {
            $(this).css("color", "#7453c3");
        },
        function () {
            $(this).css("color", "black");
        }
    );
});

$(function () {
    $('#last-pag').hover(
        function () {
            $(this).css("color", "#7453c3");
        },
        function () {
            $(this).css("color", "black");
        }
    );
});

$(function () {
    $('#next-pag').hover(
        function () {
            $(this).css("color", "#7453c3");
        },
        function () {
            $(this).css("color", "black");
        }
    );
});

$(function () {
    $('#first-pag').hover(
        function () {
            $(this).css("color", "#7453c3");
        },
        function () {
            $(this).css("color", "black");
        }
    );
});

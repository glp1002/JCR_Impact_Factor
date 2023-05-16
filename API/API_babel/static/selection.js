// Función para comprobar si todos los elementos están seleccionados
function checkSelection() {
  const categoria = document.getElementById('categoria').value;
  const revista = document.getElementById('revista').value;
  const anio = document.getElementById('anio').value;
  const modelos = document.querySelectorAll('input[name="modelo[]"]:checked');

  // Habilitar el botón si todas las selecciones están hechas
  if (categoria && revista && anio && modelos.length > 0) {
    document.getElementById('calcular-btn').disabled = false;
    $('#calcular-btn').tooltip('hide').tooltip('disable');
  } else {
    document.getElementById('calcular-btn').disabled = true;
    $('#calcular-btn').tooltip('enable').tooltip('show');
  }
}

// Inicializar el tooltip de Bootstrap
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

// Escuchar los eventos de cambio en los elementos del formulario
document.getElementById('categoria').addEventListener('change', checkSelection);
document.getElementById('revista').addEventListener('change', checkSelection);
document.getElementById('anio').addEventListener('change', checkSelection);
document.querySelectorAll('input[name="modelo[]"]').forEach((checkbox) => {
  checkbox.addEventListener('change', checkSelection);
});


// Cambio del botón de acceso a la lista de revistas
$(function () {
  $('#lista-rev').hover(
    function () {
      $(this).attr('src', '/static/images/lista-rev.png');
    },
    function () {
      $(this).attr('src', '/static/images/lista-rev-2.png');
    }
  );
});


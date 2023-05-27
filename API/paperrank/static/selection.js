// Función para comprobar si se seleccionó categoría y revista
function checkSelectionForConsultar() {
  const categoria = document.getElementById('categoria').value;
  const revista = document.getElementById('revista').value;

  // Habilitar el botón si se seleccionó categoría y revista
  if (categoria && revista) {
    document.getElementById('calcular-btn-consultar').disabled = false;
    $('#calcular-btn-consultar').tooltip('hide').tooltip('disable');
  } else {
    document.getElementById('calcular-btn-consultar').disabled = true;
    $('#calcular-btn-consultar').tooltip('enable').tooltip('show');
  }
}

// Función para comprobar si todos los campos están seleccionados
function checkSelectionForPredecir() {
  const categoria = document.getElementById('categoria').value;
  const revista = document.getElementById('revista').value;
  const modelos = document.querySelectorAll('input[name="modelo[]"]:checked');

  // Habilitar el botón si todas las selecciones están hechas
  if (categoria && revista && modelos.length > 0) {
    document.getElementById('calcular-btn-predecir').disabled = false;
    $('#calcular-btn-predecir').tooltip('hide').tooltip('disable');
  } else {
    document.getElementById('calcular-btn-predecir').disabled = true;
    $('#calcular-btn-predecir').tooltip('enable').tooltip('show');
  }
}

// Inicializar el tooltip de Bootstrap
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

// Escuchar los eventos de cambio en los elementos del formulario
document.getElementById('categoria').addEventListener('change', checkSelectionForConsultar);
document.getElementById('revista').addEventListener('change', checkSelectionForConsultar);
document.querySelectorAll('input[name="modelo[]"]').forEach((checkbox) => {
  checkbox.addEventListener('change', checkSelectionForPredecir);
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


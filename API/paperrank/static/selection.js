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


$(document).ready(function () {
  // Obtener referencia al elemento de selección de categoría
  var categoriaSelect = document.getElementById('categoria');

  // Agregar listener para el evento "change" (cambio de selección)
  categoriaSelect.addEventListener('change', function () {
    // Obtener el valor seleccionado de la categoría
    var categoria = categoriaSelect.value;

    // Realizar la solicitud fetch para obtener la lista de revistas según la categoría seleccionada
    fetch('/journal/' + categoria)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // Limpiar la lista de revistas actual
        var revistaSelect = document.getElementById('revista');
        revistaSelect.innerHTML = '';

        // Agregar las nuevas opciones de revistas según los datos obtenidos
        var revistas = data.revistas;
        revistas.forEach(function (revista) {
          var option = document.createElement('option');
          option.value = revista;
          option.text = revista;
          revistaSelect.appendChild(option);
        });
      })
      .catch(function (error) {
        console.error('Error al obtener las revistas:', error);
      });
  });
});
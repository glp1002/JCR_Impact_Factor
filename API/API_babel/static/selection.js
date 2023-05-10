// Función para comprobar si todos los elementos están seleccionados
function checkSelection() {
  const categoria = document.getElementById('categoria').value;
  const revista = document.getElementById('revista').value;
  const anio = document.getElementById('anio').value;
  const modelos = document.querySelectorAll('input[name="modelo[]"]:checked');

  // Habilitar el botón si todas las selecciones están hechas
  if (categoria && revista && anio && modelos.length > 0) {
      document.getElementById('calcular-btn').disabled = false;
  } else {
      document.getElementById('calcular-btn').disabled = true;
  }
}

// Escuchar los eventos de cambio en los elementos del formulario
document.getElementById('categoria').addEventListener('change', checkSelection);
document.getElementById('revista').addEventListener('change', checkSelection);
document.getElementById('anio').addEventListener('change', checkSelection);
document.querySelectorAll('input[name="modelo[]"]').forEach((checkbox) => {
  checkbox.addEventListener('change', checkSelection);
});

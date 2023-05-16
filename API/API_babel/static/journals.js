
$(document).ready(function() {
  $('.collapse.show').slideUp();
  $('.collapse.show').hide();

  // Evento de clic en el nombre de la revista
  $('.accordion-toggle').on('click', function() {
    var target = $(this).closest('tr').next('.collapse');
    target.toggle();
  });

  // Evento de entrada en la barra de búsqueda
  $('#search-input').on('input', function() {
    var searchText = $(this).val().trim().toLowerCase(); // Obtener el texto de búsqueda sin espacios en blanco

    $('.collapse.show').slideUp(); // Cerrar todos los acordeones abiertos
    $('#journal-table-body tr').hide(); // Ocultar todas las filas de la tabla

    // Mostrar solo las filas que coinciden con el texto de búsqueda
    $('#journal-table-body tr').each(function() {
      var rowText = $(this).text().toLowerCase();
      if (rowText.indexOf(searchText) !== -1) {
        $('.collapse').slideUp();
        $(this).show();        
      }
    });
  });
});

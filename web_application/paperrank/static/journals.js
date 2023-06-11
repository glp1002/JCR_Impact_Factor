
$(document).ready(function () {
  $('.collapse.show').slideUp();
  $('.collapse.show').hide();

  // Evento de clic en el nombre de la revista
  $('.accordion-toggle').on('click', function () {
    var target = $(this).closest('tr').next('.collapse');
    target.toggle();

    // Obtener el nombre de la revista
    var revista = $(this).text();

    // Realizar las solicitudes fetch a los endpoint de Flask

    // Datos del JCR y cuartiles de los últimos 5 años
    fetch('/consultJSON/' + revista)
      .then(response => response.json())
      .then(data => {
        // Rellenar la información adicional dentro del acordeón
        var jcrValues = data.jcrValues.reverse();
        var years = data.years.reverse();
        var lista_jcr = '';

        fetch('/quartileJSON/' + revista)
          .then(response => response.json())
          .then(data => {
            // Rellenar la información adicional dentro del acordeón
            var cuartiles = data.quartil_list.reverse();
            var lista_combined = '';

            for (var i = 0; i < jcrValues.length; i++) {
              lista_combined += '<li>' + years[i] + ' - ' + jcrValues[i] + ' - ' + cuartiles[i] + '</li>';
            }

            target.find('.lista-combined').html(lista_combined);
          })
          .catch(error => {
            console.log('Error:', error);
          });
      })
      .catch(error => {
        console.log('Error:', error);
      });

  });


  // Evento de entrada en la barra de búsqueda
  $('#search-input').on('input', function () {
    var searchText = $(this).val().trim().toLowerCase(); // Obtener el texto de búsqueda sin espacios en blanco

    $('.collapse.show').slideUp(); // Cerrar todos los acordeones abiertos
    $('#journal-table-body tr').hide(); // Ocultar todas las filas de la tabla

    // Mostrar solo las filas que coinciden con el texto de búsqueda
    $('#journal-table-body tr').each(function () {
      var rowText = $(this).text().toLowerCase();
      if (rowText.indexOf(searchText) !== -1) {
        $('.collapse').slideUp();
        $(this).show();
      }
    });
  });

});


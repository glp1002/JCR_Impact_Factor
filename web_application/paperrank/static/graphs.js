// Obtener el valor de "revista" de la URL
const urlParams = new URLSearchParams(window.location.search);
const revista = urlParams.get('revista');

// Realizar la llamada al endpoint consultJSON con el valor de "revista"
fetch(`/consultJSON/${encodeURIComponent(revista)}`)
  .then(response => {
    if (!response.ok) {
      throw new Error("Error en la respuesta de la petición.");
    }
    return response.json();
  })
  .then(data => {
    // Aquí puedes acceder a los datos de jcrValues y years y utilizarlos para crear la línea temporal con Chart.js
    const jcrValues = data.jcrValues.reverse();
    const years = data.years.reverse();

    // Código para crear la línea temporal con Chart.js utilizando los datos de jcrValues y years
    // Crear un contexto para el gráfico
    var ctx = document.getElementById('lineChart').getContext('2d');

    // Configurar el gráfico
    let lineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: years,  // Etiquetas en el eje X (años)
        datasets: [{
          label: 'JCR',  // Etiqueta de la línea
          data: jcrValues,  // Valores en el eje Y (JCR)
          borderColor: '#7453c3',  // Color de la línea
        }]
      },
      options: {
        responsive: true,  // Hacer el gráfico responsive
        maintainAspectRatio: false,  // No mantener el aspect ratio
        scales: {
          y: {
            beginAtZero: true  // Comenzar el eje Y en cero
          }
        },
        onClick: (event, legendItem) => {
          // Evitar la acción predeterminada (ocultar/mostrar línea)
          event.stopPropagation();
        }
      }
    });

  })
  .catch(error => {
    console.error(error);
  });



// Realizar la llamada al endpoint consultJSON con el valor de "revista"
fetch(`/quartileJSON/${encodeURIComponent(revista)}`)
  .then(response => {
    if (!response.ok) {
      throw new Error("Error en la respuesta de la petición.");
    }
    return response.json();
  })
  .then(data => {
    const quartil_list = data.quartil_list.reverse();
    const years = data.years.reverse();
    const cuartiles = ['Q1', 'Q2', 'Q3', 'Q4'];

    const datasets = [{
      label: 'Quartile',
      data: quartil_list.map(cuartil => cuartiles.indexOf(cuartil) + 1),
      backgroundColor: '#7453c3',
    }];

    var ctx = document.getElementById('barChart').getContext('2d');

    let barChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: years,  // Etiquetas en el eje X
        datasets: datasets,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            beginAtZero: true,  // Comenzar el eje X en cero
          },
          y: {
            beginAtZero: true,  // Comenzar el eje Y en cero
            ticks: {
              callback: function (value, index, values) {
                return cuartiles[value - 1];
              },
              stepSize: 1,
              max: 4,
              min: 1
            },
          },
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                return 'Q' + context.parsed.y + ': ' + cuartiles[context.parsed.y - 1];
              },
            },
          },
        },
      },
    });
  })
  .catch(error => {
    console.error(error);
  });


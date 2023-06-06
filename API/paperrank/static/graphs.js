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





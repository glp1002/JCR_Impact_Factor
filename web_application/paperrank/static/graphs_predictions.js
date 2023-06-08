// Obtener el valor de "revista" y "modelos" de la URL
const urlParams = new URLSearchParams(window.location.search);
const revista = urlParams.get('revista');
const modelos_deseados = urlParams.get('modelos');

// Realizar la solicitud al endpoint prediction
fetch(`/predictionJSON/${encodeURIComponent(revista)}/${encodeURIComponent(modelos_deseados)}`)
  .then(response => {
    if (!response.ok) {
      throw new Error("Error en la respuesta de la petición.");
    }
    return response.json();
  })
  .then(data => {
    // Extraer los datos de consulta, predicciones y años
    const jcrValues = data.jcrValues.reverse();
    const predictions = data.predictions;
    const years = data.years.reverse();

    // Agregar los dos siguientes años a la lista
    const addYears = 1; // Años extra en el eje X
    const nextYears = Array.from({ length: addYears }, (_, index) => String(Number(years[years.length - 1]) + index + 1));
    const allYears = [...years, ...nextYears];

    const datasets = [{
      label: 'Histórico JCR',
      data: jcrValues,
      borderColor: '#7453c3',
      lineTension: 0.1, // Ajustar la tensión de la línea para hacerla recta
      spanGaps: true    // Permitir que las líneas se salten puntos de datos nulos
    }]

    // Crear datasets
    var index = 0;
    predictions.forEach(tupla => {
      const modelo = tupla[0];
      const valor1 = tupla[1];
      const valor2 = tupla[2];

      // Crear el dataset para el modelo actual
      const dataset = {
        label: modelo,
        data: Array(years.length-1).fill(null).concat([valor1, valor2]),
        borderColor: getColorByIndex(index),
        lineTension: 0.1,
        spanGaps: true
      };
      index = index + 1;

      // Agregar el dataset a la lista de datasets
      datasets.push(dataset);
    });


    // Crear un contexto para el gráfico
    var ctx = document.getElementById('lineChart').getContext('2d');

    // Configurar el gráfico
    let lineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: allYears,  // Etiquetas en el eje X (años)
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'category',
            labels: allYears, // Usar la lista de todos los años
            beginAtZero: true,
            maxRotation: 0,
            grid: {
              drawBorder: false,
              display: false
            }
          },
          y: {
            beginAtZero: true
          }
        }
      }
    });
  })
  .catch(error => {
    console.error(error);
  });

// Función para obtener un color según el índice
function getColorByIndex(index) {
  const colors = ['#98FB98','#87CEEB', '#FFB6C1', '#FFDAB9'];
  return colors[index % colors.length];
}

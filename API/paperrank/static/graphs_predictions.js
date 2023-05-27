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
    const predictions2 = data.predictions2;
    const years = data.years.reverse();

    // Crear un contexto para el gráfico
    var ctx = document.getElementById('lineChart').getContext('2d');

    // Configurar el gráfico
    let lineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: years,  // Etiquetas en el eje X (años)
        datasets: [
          {
            label: 'Consulta',
            data: jcrValues,
            borderColor: '#7453c3',
            lineTension: 0.1, // Ajustar la tensión de la línea para hacerla recta
            spanGaps: true    // Permitir que las líneas se salten puntos de datos nulos
          },
          // Agregar líneas para cada modelo en diferentes colores
          ...predictions2.map((prediction, index) => ({
            label: prediction[0],
            data: Array(years.length - 1).fill(null).concat([prediction[1]]), 
            borderColor: getColorByIndex(index),
            fill: false,
            lineTension: 0,  // Unir puntos con una línea recta
            spanGaps: false  
          })),
          ...predictions.map((prediction, index) => ({
            label: prediction[0],
            data: Array(years.length ).fill(null).concat([prediction[1]]), // Rellenar con null hasta el último año y agregar el valor de la predicción para el último año
            borderColor: getColorByIndex(index),
            fill: false,
            lineTension: 0,  // Unir puntos con una línea recta
            spanGaps: false  
          }))
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'category',
            labels: [...years, '2023', '2024'], // Agregar dos etiquetas vacías al final para ampliar el rango
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
  const colors = ['#ff0000', '#00ff00', '#0000ff', '#ff00ff', '#00ffff']; // Colores de ejemplo, puedes agregar más colores según la cantidad de modelos
  return colors[index % colors.length];
}

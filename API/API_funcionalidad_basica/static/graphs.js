// Datos para el gráfico
let yearsJSON = JSON.parse({{ years | tojson }});
var jcrValues = yearsJSON

// Crear un contexto para el gráfico
var ctx = document.getElementById('lineChart').getContext('2d');

// Configurar el gráfico
let lineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: years,  // Etiquetas en el eje X (años)
    datasets: [{
      label: 'JCR',  // Etiqueta de la línea
      data: yearsJSON,  // Valores en el eje Y (JCR)
      borderColor:  '#7453c3',  // Color de la línea
      fill: false  // Sin relleno debajo de la línea
    }]
  },
  options: {
    responsive: true,  // Hacer el gráfico responsive
    maintainAspectRatio: false,  // No mantener el aspect ratio
    scales: {
      y: {
        beginAtZero: true  // Comenzar el eje Y en cero
      }
    }
  }
});

// Obtener el elemento canvas
const canvas = document.getElementById('myChart');

// Obtener los datos de predictions desde el atributo data
const predictions = JSON.parse(canvas.getAttribute('data-predictions'));

const colors = ['rgb(75, 192, 192)', 'rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(153, 102, 255)'];

const datasets = [];

predictions.forEach(function(prediction, index) {
  const nombre = prediction[0];
  const data = prediction[1];
  const color = colors[index % colors.length];

  datasets.push({
    label: nombre,
    data: data.map((value, i) => ({ x: 2001 + i, y: value })),
    fill: false,
    borderColor: color,
    tension: 0.1
  });
});

// Crear gráfica de serie temporal
const ctx = canvas.getContext('2d');
const myChart = new Chart(ctx, {
  type: 'line',
  data: {
    datasets: datasets
  },
  options: {
    responsive: true,
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Año'
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'JCR'
        }
      }
    }
  }
});

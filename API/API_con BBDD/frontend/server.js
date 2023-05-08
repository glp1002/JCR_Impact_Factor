
const express = require('express');
const app = express();
axios = require('axios');

// configure server
function configureServer() {
    // handle GET requests on the root path
    app.get('/', function (req, res) {
        res.send('Conexión correcta');
    });
    app.get('/impact/:revista', (req, res) => {
        axios.get(`http://127.0.0.1:5000/api/indice_impacto/${req.params.revista}`)
        //axios.get(`http://localhost:5000/impact/${req.params.revista}`)
          .then(response => {
            res.send(response.data);
          })
          .catch(error => {
            res.send(error);
          });
      });
      app.get('/articulos/:revista', (req, res) => {
        axios.get(`http://127.0.0.1:5000/api/articulos/${req.params.revista}`)
        //axios.get(`http://localhost:5000/articulos/${req.params.revista}`)
          .then(response => {
            res.send(response.data);
          })
          .catch(error => {
            res.send(error);
          });
    });
    
}

configureServer();

// start server on port 3000
app.listen(3000, () => {
    console.log('Server listening on port 3000');
});

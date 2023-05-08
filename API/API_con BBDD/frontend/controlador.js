/*
En este ejemplo, la clase de Controlador tiene dos métodos estáticos, obtenerArticulos y 
obtenerIndiceImpacto que utilizan el objeto fetch de JavaScript para enviar peticiones 
HTTP a la API. Cada método toma como parámetro la revista seleccionada por el usuario y 
devuelve una promesa con la respuesta del servidor. Si la respuesta del servidor no es 
ok, se lanza una excepción con un mensaje de error que se puede manejar en la clase de 
Vista para mostrar el error al usuario. El método obtenerArticulos realiza una petición
 GET a la ruta /api/articulos/revista para obtener los artículos de una revista 
 específica, y el método obtenerIndiceImpacto realiza una petición GET a la ruta 
 /api/indice_impacto/revista para obtener el índice de impacto de una revista específica.
*/

// Controlador
class Controlador {
    static obtenerArticulos(revista) {
      return fetch(`/api/articulos/${revista}`)
        .then(response => {
          if (!response.ok) {
            throw new Error(response.statusText);
          }
          return response.json();
        })
    }
  
    static obtenerIndiceImpacto(revista) {
      return fetch(`/api/indice_impacto/${revista}`)
        .then(response => {
          if (!response.ok) {
            throw new Error(response.statusText);
          }
          return response.json();
        })
    }
}
  
"""
El archivo "app.py" es el archivo principal de tu aplicación donde se configura y ejecuta el servidor de backend. 
Este archivo crea una instancia de Flask y define dos rutas, /api/articulos/<revista> y 
/api/indice_impacto/<revista> que corresponden a las rutas que utilizan los métodos obtenerArticulos y 
obtenerIndiceImpacto de la clase Controlador del frontend. Cada ruta se asocia con un método de la aplicación
Flask que crea una instancia de la clase Modelo, llama al método correspondiente y devuelve la respuesta en 
formato JSON.
"""

from flask import Flask, jsonify, request
from modelo.modelo import Modelo
from controlador.controlador import Controlador

app = Flask(__name__)

# Crear una única instancia de Modelo al inicio de la aplicación
modelo = Modelo()
controlador = Controlador(modelo)

@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data:;"
    return resp

@app.route('/api/articulos/<revista>', methods=['GET'])
def obtener_articulos(revista):
    articulos = controlador.obtener_articulos(revista)    
    return jsonify(articulos)

@app.route('/api/indice_impacto/<revista>', methods=['GET'])
def obtener_indice_impacto(revista):
    indice_impacto = controlador.obtener_indice_impacto(revista)
    return jsonify(indice_impacto)

if __name__ == '__main__':
    app.run()

"""
La clase Vista tiene un constructor que recibe como parámetro una instancia del controlador.
Utiliza Flask para crear una aplicación web y define dos rutas, una para obtener los artículos
de una revista específica y otra para obtener el índice de impacto de una revista específica.
Cada ruta llama al método correspondiente del controlador para obtener la información necesaria 
y luego utiliza el método render_template de Flask para mostrar una plantilla HTML al usuario 
con los datos obtenidos.
"""

from flask import Flask, render_template

class Vista:
    def __init__(self, controlador):
        self.controlador = controlador
        self.app = Flask(__name__)

        @self.app.route("/articulos/<revista>")
        def articulos(revista):
            articulos = self.controlador.obtener_articulos(revista)
            return render_template("articulos.html", articulos=articulos)

        @self.app.route("/indice_impacto/<revista>")
        def indice_impacto(revista):
            indice_impacto = self.controlador.obtener_indice_impacto(revista)
            return render_template("indice_impacto.html", indice_impacto=indice_impacto)

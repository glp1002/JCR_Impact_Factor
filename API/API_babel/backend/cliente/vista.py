"""
La clase Vista tiene un constructor que recibe como parámetro una instancia del controlador.
Utiliza Flask para crear una aplicación web y define dos rutas, una para obtener los artículos
de una revista específica y otra para obtener el índice de impacto de una revista específica.
Cada ruta llama al método correspondiente del controlador para obtener la información necesaria 
y luego utiliza el método render_template de Flask para mostrar una plantilla HTML al usuario 
con los datos obtenidos.
"""

from flask import Flask, render_template

""" MANEJO DE ERRORES
Cada ruta llama al método correspondiente del controlador para obtener la información necesaria,
si la respuesta tiene un key "error" significa que hubo un problema, y se mostrará el error al
usuario, sino se mostrará la plantilla html con los datos obtenidos.
"""
class Vista:
    def __init__(self, controlador):
        self.controlador = controlador
        self.app = Flask(__name__)

  
        @self.app.route("/articulos/<revista>")
        def articulos(revista):
            result = self.controlador.obtener_articulos(revista)
            if "error" in result:
                return result["error"], 500
            return render_template("articulos.html", articulos=result)

        @self.app.route("/indice_impacto/<revista>")
        def indice_impacto(revista):
            result = self.controlador.obtener_indice_impacto(revista)
            if "error" in result:
                return result["error"], 500
            return render_template("indice_impacto.html", indice_impacto=result)


"""
La clase Controlador tiene un constructor que recibe como parámetro una instancia del modelo.
Luego tiene dos métodos, obtener_articulos y obtener_indice_impacto que reciben como parametro 
una revista y llaman a los métodos correspondientes del modelo para obtener los datos necesarios
y devolverlos al usuario.
"""
class Controlador:
    def __init__(self, modelo):
        self.modelo = modelo

    def obtener_articulos(self, revista):
        return self.modelo.obtener_articulos(revista)

    def obtener_indice_impacto(self, revista):
        return self.modelo.obtener_indice_impacto(revista)
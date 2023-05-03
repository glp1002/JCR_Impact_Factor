
"""
La clase Articulo es una clase de modelo para representar cada artículo en la base de datos. 
"""

class Articulo:
    def __init__(self, nombre, DOI, revista, ncitas, fecha):
        self.nombre = nombre
        self.DOI = DOI
        self.revista = revista
        self.ncitas = ncitas
        self.fecha = fecha
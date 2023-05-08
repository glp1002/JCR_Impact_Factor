"""
Esta clase modelo incluye las estructuras para representar cada tabla de la base de datos. 
"""

class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

class Articulo:
    def __init__(self, nombre, DOI, revista, ncitas, fecha):
        self.nombre = nombre
        self.DOI = DOI
        self.revista = revista
        self.ncitas = ncitas
        self.fecha = fecha

class Revista:
    def __init__(self, nombre, ISSN, pais, fecha):
        self.nombre = nombre
        self.ISSN = ISSN
        self.pais = pais
        self.fecha = fecha

class Citas:
    def __init__(self, doi_citante, doi_citado):
        self.doi_citante = doi_citante
        self.doi_citado = doi_citado
"""
Esta clase modelo incluye las estructuras para representar cada tabla de la base de datos. 
"""

class User:
    def __init__(self, id, username, password, email, admin):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin # boolean

    def __str__(self):
        return "User(id='%s')" % self.id

class Articulo:
    def __init__(self, nombre, DOI, revista, ncitas, fecha):
        self.nombre = nombre
        self.DOI = DOI
        self.revista = revista
        self.ncitas = ncitas
        self.fecha = fecha

    def __str__(self):
        return "Article(name='%s')" % self.nombre

class Revista:
    def __init__(self, nombre, ISSN, categoria):
        self.nombre = nombre
        self.ISSN = ISSN
        self.categoria = categoria

    def __str__(self):
        return "Revista(name='%s')" % self.nombre

class Citas:
    def __init__(self, doi_citante, doi_citado):
        self.doi_citante = doi_citante
        self.doi_citado = doi_citado

class RevistaJCR:
    def __init__(self, nombre, fecha, jcr, citas, diff):
        self.nombre = nombre
        self.fecha = fecha
        self.jcr = jcr
        self.citas = citas
        self.diff = diff

    def __str__(self):
        return f"RevistaJCR(nombre={self.nombre}, fecha={self.fecha}, jcr={self.jcr}, citas={self.citas}, diff={self.diff})"
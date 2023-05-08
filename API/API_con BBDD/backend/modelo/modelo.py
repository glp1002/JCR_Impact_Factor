""" AÑADIR EN MEMORIA
psycopg2 es un módulo de Python que proporciona una interfaz para conectarse y interactuar con bases de datos PostgreSQL. 
Es una de las librerías más populares y ampliamente utilizadas para trabajar con PostgreSQL en Python.
Es compatible con la mayoría de las versiones de Python y es muy fácil de utilizar, proporciona una interfaz similar a la
de las bases de datos relacionales como MySQL, además proporciona una gran cantidad de funciones útiles para trabajar con 
bases de datos.
"""
import psycopg2
from modelo.articulodb import Articulo

"""
La clase Modelo contiene métodos para interactuar con la base de datos y realizar operaciones específicas.
En este caso, tiene un método para obtener los artículos de una determinada revista y otro método para 
obtener el índice de impacto de una revista en particular.
"""

    
class Modelo:
    
    
    """
    Para configurar la conexión a la base de datos se proporcionarán los detalles de la conexión
    (nombre de usuario, contraseña, nombre de la base de datos, etc...) mediante la biblioteca psycopg2.
    """
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                port=5432,
                user="postgres",
                password="Hola=2910",
                dbname="BBDD"
            )
        except psycopg2.Error as e:
            raise Exception("Error al conectarse a la base de datos: " + str(e))

    def obtener_articulos(self, revista):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nombre, DOI, revista, ncitas, fecha FROM articulo WHERE revista = %s", (revista,))
            articulos = []
            for nombre, DOI, revista, ncitas, fecha in cur:
                articulos.append(Articulo(nombre, DOI, revista, ncitas, fecha))
            return articulos
        except psycopg2.Error as e:
            raise Exception("Error al obtener los artículos: " + str(e))

    def obtener_indice_impacto(self, revista):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT AVG(ncitas) FROM articulo WHERE revista = %s", (revista,))
            indice_impacto = cur.fetchone()[0]
            return indice_impacto
        except psycopg2.Error as e:
            raise Exception("Error al obtener el índice de impacto: " + str(e))

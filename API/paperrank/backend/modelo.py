""" AÑADIR EN MEMORIA
psycopg2 es un módulo de Python que proporciona una interfaz para conectarse y interactuar con bases de datos PostgreSQL. 
Es una de las librerías más populares y ampliamente utilizadas para trabajar con PostgreSQL en Python.
Es compatible con la mayoría de las versiones de Python y es muy fácil de utilizar, proporciona una interfaz similar a la
de las bases de datos relacionales como MySQL, además proporciona una gran cantidad de funciones útiles para trabajar con 
bases de datos.
"""
import json
import os
import pickle

import psycopg2

from .datasource import Articulo, Citas, Revista, User

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
                os.environ['postgres://ztzjgdjnrrjcqc:039a004b9bb682c3d598bef51d01b9c632b9325bba8f6eb7e87e909d6553c6fe@ec2-52-215-209-64.eu-west-1.compute.amazonaws.com:5432/d8rmkut3jrsi93'], 
                sslmode='require'
            )
        except psycopg2.Error as e:
            raise Exception("Error al conectarse a la base de datos: " + str(e))
        
    def get_journals(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nombre, ISSN, categoria FROM revista")
            journals = []
            for nombre, ISSN, categoria in cur:
                journals.append(Revista(nombre, ISSN, categoria))
            return journals
        except psycopg2.Error as e:
            raise Exception("Error al obtener las revistas: " + str(e))
        
    def get_last_jcr(self, nombre_revista):
        try:
            cur = self.conn.cursor()

            query_last_jcr = """
                SELECT fecha, JCR
                FROM revista_jcr
                WHERE nombre = %s
                AND fecha = (SELECT MAX(fecha) FROM revista_jcr WHERE nombre = %s)
            """
            cur.execute(query_last_jcr, (nombre_revista, nombre_revista))
            last_jcr = cur.fetchone()

            if last_jcr is None:
                last_jcr = (0, 0.0)
            else:
                last_jcr = (last_jcr[0], last_jcr[1])
            cur.close()
            return last_jcr

        except psycopg2.Error as e:
            raise Exception("Error al obtener el último JCR: " + str(e))
    
    def get_jcr(self, nombre_revista, anio):
        try:
            cur = self.conn.cursor()

            query_last_jcr = """
                SELECT JCR
                FROM revista_jcr
                WHERE nombre = %s
                AND fecha = %s
            """
            cur.execute(query_last_jcr, (nombre_revista, anio))
            jcr = cur.fetchone()[0]

            if jcr is None:
                jcr = 0.0

            cur.close()
            return jcr

        except psycopg2.Error as e:
            raise Exception("Error al obtener los JCR: " + str(e))
        
    def get_year_range(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT DISTINCT fecha FROM revista_jcr")
            years = [elem[0] for elem in cur]
            cur.close()
            return years
        except psycopg2.Error as e:
            raise Exception("Error al obtener los años de los artículos: " + str(e))

    def get_revistas_por_categoria(self, categoria):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nombre FROM revistas WHERE categoria = %s", categoria)

            revistas = []
            for elem in cur:
                revistas.append(elem[0])
            return revistas
        
        except psycopg2.Error as e:
            raise Exception("Error al obtener las revistas de la categoría " + categoria + ": " + str(e))

    # Gestionar usuarios
    def create_user(self, username, password, email, admin=False):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO users (username, password, email, admin) VALUES (%s, %s, %s)",
                        (username, password, email, admin))
            self.conn.commit()
            cur.close()
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            cur.close()
            raise Exception("Error al crear el nuevo usuario: " + str(e))
            
    def authenticate_user(self, username, password):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id FROM users WHERE username = %s AND password = %s FETCH FIRST 1 ROW ONLY", (username, password))
            user_id = cur.fetchone()[0]
            cur.close()

            if user_id:
                return user_id[0]
            else:
                return None
        except psycopg2.Error as e:
            raise Exception("Error al crear el nuevo usuario: " + str(e))
        
    def get_user(self, user_id):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            cur.close()

            if user_data:
                user = User(user_data[0], user_data[1], "", user_data[2])
                return user
            else:
                return None
        except psycopg2.Error as e:
            raise Exception("Error al obtener los datos del usuario: " + str(e))
        
    def get_users_by_role(self, admin=False):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id, username, password, email, admin FROM users WHERE admin = %s", (admin,))
            users = []
            for user_data in cur:
                user = User(user_data[0], user_data[1], "", user_data[2], user_data[3])
                users.append(user)
            cur.close()
            return users
        except psycopg2.Error as e:
            raise Exception("Error al obtener los usuarios por rol: " + str(e))
    
    def update_user(self, user_id, new_username, new_password, new_email, new_admin):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE users SET username = %s, password = %s, email = %s, admin = %s WHERE id = %s",
                        (new_username, new_password, new_email, new_admin, user_id))
            self.conn.commit()
            cur.close()
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            cur.close()
            raise Exception("Error al actualizar los datos del usuario: " + str(e))
        
    def delete_user(self, user_id):
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.conn.commit()
            cur.close()
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            cur.close()
            raise Exception("Error al eliminar el usuario: " + str(e))
        
    # Gestión de los modelos de predicción
    def insert_models(self):
        try:
            cur = self.conn.cursor()

            # Cargar el archivo JSON 
            nombre_archivo = r"C:\Users\Gadea\Desktop\Repositorios_Git\TFG\JCR_Impact_Factor\API\API_babel\prediction_models\resultados.json"
            with open(nombre_archivo, "r") as archivo_json:
                diccionario_modelos = json.load(archivo_json)

            for nombre, rmse in diccionario_modelos.items():
                # Cargar el modelo desde el archivo pickle
                path = r'C:\Users\Gadea\Desktop\Repositorios_Git\TFG\JCR_Impact_Factor\API\API_babel\prediction_models\modelo_'+ nombre + '.pickle'
                with open(path, 'rb') as archivo:
                    modelo_bytes = pickle.load(archivo)
                # modelo_bytes = pickle.dumps(modelo)

                # Insertar en la base de datos
                consulta = """
                INSERT INTO modelos (nombre, modelo, rmse) VALUES (%s, %s, %s);
                """
                cur.execute(consulta, (nombre, modelo_bytes, rmse))

            self.conn.commit()
            cur.close()
            return True

        except (psycopg2.Error, IOError) as e:
            self.conn.rollback()
            cur.close()
            raise Exception("Error al insertar los modelos: " + str(e))

    def get_model_names_and_errors(self):
        try:
            cur = self.conn.cursor()

            consulta = """
            SELECT nombre, rmse FROM modelos;
            """
            cur.execute(consulta)
            resultados = cur.fetchall()

            lista_modelos = []
            for nombre, rmse in resultados:
                modelo = {"nombre": nombre, "rmse": rmse}
                lista_modelos.append(modelo)

            cur.close()
            return lista_modelos

        except psycopg2.Error as e:
            cur.close()
            raise Exception("Error al obtener los nombres de los modelos y sus errores: " + str(e))

    def get_model_binaries(self, nombres_modelos):
        try:

            diccionario_modelos = {}

            for nombre in nombres_modelos:

                # Cargar el modelo desde el archivo pickle
                path = r'C:\Users\Gadea\Desktop\Repositorios_Git\TFG\JCR_Impact_Factor\API\API_babel\prediction_models\modelo_'+ nombre + '.pickle'
                with open(path, 'rb') as archivo:
                    resultados = pickle.load(archivo)

                # Obtener la lista de modelos y resultados de la iteración
                modelos_iteracion = resultados['modelos']
                resultados_iteracion = resultados['resultados']

                # Encontrar el índice del modelo con el menor valor de RMSE
                indice_mejor_modelo = resultados_iteracion.index(min(resultados_iteracion))
                # Seleccionar el modelo con mejores resultados
                mejor_modelo = modelos_iteracion[indice_mejor_modelo]

                diccionario_modelos[nombre] = mejor_modelo

            return diccionario_modelos

        except psycopg2.Error as e:
            raise Exception("Error al obtener los binarios de los modelos: " + str(e))

    def get_ejemplo(self, nombre_revista, year):
        try:
            cur = self.conn.cursor()
            year = int(year)

            # Obtener número de citas de hace 3 años de la revista
            query_3_anios = """
            SELECT citas, jcr, diff
            FROM revista_jcr
            WHERE nombre = %s AND fecha = %s
            """
            cur.execute(query_3_anios, (nombre_revista, year - 3))
            citas_3_anios, jcr_3_anios, diff_3_anios = cur.fetchone() or (0, 0.0, 0.0)

            # Obtener número de citas de hace 2 años de la revista
            query_2_anios = """
            SELECT citas, jcr, diff
            FROM revista_jcr
            WHERE nombre = %s AND fecha = %s
            """
            cur.execute(query_2_anios, (nombre_revista, year - 2))
            citas_2_anios, jcr_2_anios, diff_2_anios = cur.fetchone() or (0, 0.0, 0.0)

            # Obtener número de citas de hace 1 año de la revista
            query_1_anio = """
            SELECT citas, jcr, diff
            FROM revista_jcr
            WHERE nombre = %s AND fecha = %s
            """
            cur.execute(query_1_anio, (nombre_revista, year - 1))
            citas_1_anios, jcr_1_anios, diff_1_anios = cur.fetchone() or (0, 0.0, 0.0)

            # Obtener número de citas de este año de la revista
            query_citas_este_anio = """
            SELECT citas, jcr, diff
            FROM revista_jcr
            WHERE nombre = %s AND fecha = %s
            """
            cur.execute(query_citas_este_anio, (nombre_revista, year))
            citas_este_anio, jcr_este_anio, diff_este_anio = cur.fetchone() or (0, 0.0, 0.0)

            cur.close()
            # ejemplo = [
            #     citas_3_anios, jcr_3_anios, diff_3_anios,
            #     citas_2_anios, jcr_2_anios, diff_2_anios,
            #     citas_1_anios, jcr_1_anios, diff_1_anios,
            #     citas_este_anio
            # ]
            ejemplo = [
                int(citas_3_anios), float(jcr_3_anios), float(diff_3_anios),
                int(citas_2_anios), float(jcr_2_anios), float(diff_2_anios),
                int(citas_1_anios), float(jcr_1_anios), float(diff_1_anios),
                int(citas_este_anio)
            ]
            return ejemplo

        except psycopg2.Error as e:
            cur.close()
            raise Exception("Error al obtener datos para la predicción: " + str(e))

    # Restablecer la BBDD
    def initialize_database(self):
        try:
            cur = self.conn.cursor()

            # Eliminar tablas si existen
            cur.execute("DROP TABLE IF EXISTS revista CASCADE;")
            cur.execute("DROP TABLE IF EXISTS articulo CASCADE;")
            cur.execute("DROP TABLE IF EXISTS citas CASCADE;")
            cur.execute("DROP TABLE IF EXISTS users CASCADE;")
            cur.execute("DROP TABLE IF EXISTS modelos CASCADE;")
            self.conn.commit()

            # Crear tablas
            cur.execute("""
                CREATE TABLE users (
                    username VARCHAR(255),
                    password VARCHAR(255),
                    email VARCHAR(255),
                    admin BOOLEAN
                );
            """)
            
            cur.execute("""
                CREATE TABLE modelos (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT,
                    rmse FLOAT,
                    modelo BYTEA
                );
            """)

            cur.execute("""
                CREATE TABLE revista (
                    nombre CHAR(60) PRIMARY KEY,
                    ISSN CHAR(9) UNIQUE NOT NULL,
                    categoria CHAR(255) NOT NULL,
                    fecha INT NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE articulo (
                    nombre CHAR(255) NOT NULL,
                    DOI CHAR(30) PRIMARY KEY,
                    revista CHAR(60) REFERENCES revista(nombre),
                    ncitas INT NOT NULL,
                    fecha INT NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE citas (
                    doi_citante CHAR(30) REFERENCES articulo(DOI),
                    doi_citado CHAR(30) REFERENCES articulo(DOI),
                    PRIMARY KEY (doi_citante, doi_citado)
                );
            """)

            # Crear índice
            cur.execute("""
                CREATE INDEX nombre_index ON revista (nombre);
            """)

            # Ejecutar el optimizador
            cur.execute("ANALYZE revista;")
            cur.execute("ANALYZE articulo;")
            cur.execute("ANALYZE citas;")
            cur.execute("ANALYZE users;")

            self.conn.commit()
            cur.close()
            return True

        except psycopg2.Error as e:
            cur.close()
            raise Exception("Error al inicializar las tablas de la base de datos: " + str(e))


                


            

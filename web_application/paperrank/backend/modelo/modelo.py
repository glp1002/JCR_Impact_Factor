import base64
import binascii
import json
import os
import pickle

import bcrypt
import psycopg2

from ..datasource import  Revista, User

"""
La clase Modelo contiene métodos para interactuar con la base de 
datos y realizar operaciones específicas.

psycopg2 es un módulo de Python que proporciona una interfaz para
 conectarse y interactuar con bases de datos PostgreSQL. 
Es una de las librerías más populares y ampliamente utilizadas 
para trabajar con PostgreSQL en Python. Es compatible con la 
mayoría de las versiones de Python y es muy fácil de utilizar, 
proporciona una interfaz similar a la de las bases de datos 
relacionales como MySQL, además proporciona una gran cantidad 
de funciones útiles para trabajar con bases de datos.

============================
  Trabajo de Fin de Grado
Universidad de Burgos (UBU)
============================

Autor: Gadea Lucas Pérez
Año: 2023

"""
 
class Modelo:

    # Ruta absoluta del directorio actual
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Ruta del directorio padre 
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    backend_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))

    """
    Para configurar la conexión a la base de datos se proporcionarán los
    detalles de la conexión (nombre de usuario, contraseña, nombre de la
    base de datos, etc...) mediante la biblioteca psycopg2 (en app.py).
    """
    def __init__(self, db):
        try:
            self.conn = db
        except psycopg2.Error as e:
            raise Exception("Error al conectarse a la base de datos: " + str(e))
        
    
    def get_journals(self):
        """
        Obtiene la lista de revistas de la base de datos.

        Returns:
            list: Lista de objetos Revista con los datos de las revistas.
            
        Raises:
            Exception: Si se produce un error al obtener las revistas.
        """
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT nombre, issn, categoria FROM revista")
            journals = []
            for nombre, issn, categoria in cur:
                journals.append(Revista(nombre, issn, categoria))
            return journals
        except psycopg2.Error as e:
            raise Exception("Error al obtener las revistas: " + str(e))
        finally:
            cur.close()

    def get_last_year(self):
        """
        Obtiene el último año para el que hay datos del JCR reales disponibles.

        Returns:
            int: Último año de los datos JCR.
            
        Raises:
            Exception: Si se produce un error al obtener el último año.
        """
        cur = self.conn.cursor()
        try:
            query_last_jcr = """
                SELECT MAX(fecha) FROM revista_jcr
            """
            cur.execute(query_last_jcr)
            last_year = cur.fetchone()[0]

            return last_year

        except psycopg2.Error as e:
            raise Exception("Error al obtener el último jcr: " + str(e))
        finally:
            cur.close()
        
    def get_last_jcr(self, nombre_revista):
        """
        Obtiene el último JCR registrado para una revista específica.

        Args:
            nombre_revista (str): Nombre de la revista.

        Returns:
            tuple: Tupla con el último JCR y la fecha correspondiente de una revista.
            Si no se encuentra el JCR, se devuelve (0, 0.0).

        Raises:
            Exception: Si se produce un error al obtener el último JCR.
        """
        cur = self.conn.cursor()
        try:
            query_last_jcr = """
                SELECT fecha, jcr
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
            return last_jcr

        except psycopg2.Error as e:
            raise Exception("Error al obtener el último jcr: " + str(e))
        finally:
            cur.close()
    
    def get_last_cuartil(self, nombre_revista):
        """
        Obtiene el último cuartil registrado para una revista específica.

        Args:
            nombre_revista (str): Nombre de la revista.

        Returns:
            tuple: Tupla con el último cuartil y la fecha correspondiente de una revista.
            Si no se encuentra el cuartil, se devuelve (0, '-').

        Raises:
            Exception: Si se produce un error al obtener el último cuartil.
        """
        cur = self.conn.cursor()
        try:
            query_last_cuartil = """
                SELECT fecha, cuartil
                FROM revista_jcr
                WHERE nombre = %s
                AND fecha = (SELECT MAX(fecha) FROM revista_jcr WHERE nombre = %s)
            """
            cur.execute(query_last_cuartil, (nombre_revista, nombre_revista))
            last_cuartil = cur.fetchone()

            if last_cuartil is None:
                last_cuartil = (0, '-')
            else:
                last_cuartil = (last_cuartil[0], last_cuartil[1])
            return last_cuartil

        except psycopg2.Error as e:
            raise Exception("Error al obtener el último jcr: " + str(e))
        finally:
            cur.close()

    
    def get_jcr(self, nombre_revista, anio):
        """
        Obtiene el factor de impacto de una revista para un año específico.

            Parameters:
                nombre_revista (str): Nombre de la revista.
                anio (int): Año para el cual se quiere obtener el factor de impacto.

            Returns:
                float: El factor de impacto de la revista para el año dado. Si no se encuentra
                    el factor de impacto, se devuelve 0.0.
        """

        cur = self.conn.cursor()
        try:
            query_jcr = """
                SELECT jcr
                FROM revista_jcr
                WHERE nombre = %s
                AND fecha = %s
            """
            cur.execute(query_jcr, (nombre_revista, anio))
            result = cur.fetchone()

            if result is not None:
                jcr = result[0]
            else:
                jcr = 0.0

            return jcr

        except psycopg2.Error as e:
            raise Exception("Error al obtener los jcr: " + str(e))
        finally:
            cur.close()

        
    def get_quartil(self, nombre_revista, anio):
        """
        Obtiene el cuartil de una revista para un año específico.

        Parameters:
        - nombre_revista (str): Nombre de la revista.
        - anio (int): Año para el cual se quiere obtener el cuartil.

        Returns:
        - str: El cuartil de la revista para el año dado. Si no se encuentra
            el cuartil, se devuelve "-".
        """
        cur = self.conn.cursor()
        try:
            query_cuartil = """
                SELECT cuartil
                FROM revista_jcr
                WHERE nombre = %s
                AND fecha = %s
            """
            cur.execute(query_cuartil, (nombre_revista, anio))
            result = cur.fetchone()

            if result is not None:
                cuartil = result[0]
            else:
                cuartil = "-"

            return cuartil

        except psycopg2.Error as e:
            raise Exception("Error al obtener los cuartiles: " + str(e))
        finally:
            cur.close()
        
    def get_year_range(self):
        """
        Obtiene el rango total de años disponibles en la tabla 'revista_jcr'.
        
        Returns:
            years (list): Lista de años distintos presentes en la tabla.
        
        Raises:
            Exception: Si ocurre un error al obtener los años de los artículos.
        """
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT DISTINCT fecha FROM revista_jcr")
            years = [elem[0] for elem in cur]
            return years
        except psycopg2.Error as e:
            raise Exception("Error al obtener los años de los artículos: " + str(e))
        finally:
            cur.close()


    # Gestionar usuarios
    def create_user(self, username, password, email, admin=False):
        """
        Crea un nuevo usuario en la tabla 'users'.

        Args:
            username (str): Nombre de usuario del nuevo usuario.
            password (str): Contraseña del nuevo usuario.
            email (str): Dirección de correo electrónico del nuevo usuario.
            admin (bool, optional): Indica si el nuevo usuario es un administrador.
                 Por defecto es False.

        Returns:
            bool: True si se creó el usuario correctamente.

        Raises:
            Exception: Si ocurre un error al crear el nuevo usuario.
        """
        cur = self.conn.cursor()
        try:
            # Contraseña hasheada
            password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(7))

            # Imagen default
            file_path = os.path.join(self.parent_directory, 'data', 'perfil.jpg')
            with open(file_path, 'rb') as file:
                image_data = file.read()

            query = """INSERT INTO users (username, password, email, admin, image) VALUES (%s, %s, %s, %s, %s);"""
            cur.execute(query, (username, hashed_password, email, admin, image_data))
            self.conn.commit()

            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception("Error al crear el nuevo usuario: " + str(e))
        finally:
            cur.close()

            
    def authenticate_user(self, username, password):
        """
        Autentica un usuario en la tabla 'users' mediante el nombre de 
        usuario y la contraseña proporcionados.

        Args:
            username (str): Nombre de usuario del usuario a autenticar.
            password (str): Contraseña del usuario a autenticar.

        Returns:
            bool: True si el usuario se autentica correctamente, False en caso contrario.

        Raises:
            Exception: Si ocurre un error al autenticar al usuario.
        """
        cur = self.conn.cursor()
        try:
            query = "SELECT password FROM users WHERE username = %s"
            cur.execute(query, (username,))
            real_password = cur.fetchone()

            if real_password is not None:
                new_password = password.encode('utf-8')
                if bcrypt.checkpw(new_password, binascii.unhexlify(real_password[0][2:])):
                    return True
            return False
            
        except psycopg2.Error as e:
            raise Exception("Error al crear el nuevo usuario: " + str(e))
        finally:
            cur.close()

        
    def get_email(self, username):
        """
        Obtiene la dirección de correo electrónico de un usuario de 
        la tabla 'users' mediante su nombre de usuario.

        Args:
            username (str): Nombre de usuario del usuario del que se desea obtener el correo electrónico.

        Returns:
            str: Dirección de correo electrónico del usuario.

        Raises:
            Exception: Si ocurre un error al obtener los datos del usuario.
        """
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT email FROM users WHERE username = %s", (username,))
            email = cur.fetchone()[0]
            return email
        except psycopg2.Error as e:
            raise Exception("Error al obtener los datos del usuario: " + str(e))
        finally:
            cur.close()

    
    def update_user(self, new_username, new_email, old_email):
        """
        Actualiza los datos de un usuario en la tabla 'users' con un nuevo 
        nombre de usuario y correo electrónico.

        Args:
            new_username (str): Nuevo nombre de usuario a actualizar.
            new_email (str): Nuevo correo electrónico a actualizar.
            old_email (str): Correo electrónico actual del usuario que se desea actualizar.

        Returns:
            bool: True si se actualizan los datos del usuario correctamente.

        Raises:
            Exception: Si ocurre un error al actualizar los datos del usuario.
        """
        cur = self.conn.cursor()
        try:
            cur.execute("UPDATE users SET username = %s, email = %s WHERE email = %s",
                        (new_username, new_email, old_email))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception("Error al actualizar los datos del usuario: " + str(e))
        finally:
            cur.close()

        
    # Gestión de los modelos de predicción
    def insert_models(self):
        """
        Inserta los modelos de predicción en la tabla 'modelos' de la base de datos.

        Returns:
            bool: True si se insertan los modelos correctamente.

        Raises:
            Exception: Si ocurre un error al insertar los modelos.
        """
        cur = self.conn.cursor()
        try:
            # Cargar el archivo JSON 
            file_path = os.path.join(self.backend_directory, 'prediction_models', 'resultados.json')
            with open(file_path, "r") as archivo_json:
                diccionario_modelos = json.load(archivo_json)

            for nombre, rmse in diccionario_modelos.items():

                # Insertar en la base de datos
                consulta = """
                INSERT INTO modelos (nombre, rmse) VALUES (%s, %s);
                """
                cur.execute(consulta, (nombre, rmse))

            self.conn.commit()
            return True

        except (psycopg2.Error, IOError) as e:
            self.conn.rollback()
            raise Exception("Error al insertar los modelos: " + str(e))
        finally:
            cur.close()


    def get_model_names_and_errors(self):
        """
        Obtiene los nombres de los modelos y sus errores (RMSE) de la tabla
        'modelos' de la base de datos.

        Returns:
            list: Lista de diccionarios que contienen los nombres de los 
            modelos y sus errores (RMSE).

        Raises:
            Exception: Si ocurre un error al obtener los nombres de los 
            modelos y sus errores.
        """
        cur = self.conn.cursor()
        try:
            consulta = """
            SELECT nombre, rmse FROM modelos;
            """
            cur.execute(consulta)
            resultados = cur.fetchall()

            lista_modelos = []
            for nombre, rmse in resultados:
                modelo = {"nombre": nombre, "rmse": rmse}
                lista_modelos.append(modelo)

            return lista_modelos

        except psycopg2.Error as e:
            raise Exception("Error al obtener los nombres de los modelos y sus errores: " + str(e))
        finally:
            cur.close()


    def get_model_binaries(self, nombres_modelos):
        """
        Obtiene los binarios de los modelos de predicción a partir de una lista de nombres de modelos.

        Args:
            nombres_modelos (list): Lista de nombres de modelos de los cuales se desea obtener los binarios.

        Returns:
            dict: Diccionario donde las claves son los nombres de los modelos y los valores son los binarios de los modelos.

        Raises:
            Exception: Si ocurre un error al obtener los binarios de los modelos.
        """
        try:
            diccionario_modelos = {}

            for nombre in nombres_modelos:

                # Cargar el modelo desde el archivo pickle
                path = os.path.join(self.backend_directory, 'prediction_models', 'modelo_'+ nombre + '.pickle')
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
        """
        Obtiene un ejemplo de datos para la predicción a partir del nombre 
        de una revista y un año específico. Estos datos se pasarán a los modelos 
        de predicción.

        Args:
            nombre_revista (str): Nombre de la revista para la cual se desea
              obtener el ejemplo de datos.
            year (int): Año para el cual se desea obtener el ejemplo de datos.

        Returns:
            list: Lista que contiene el ejemplo de datos en el siguiente orden:
                [citas_3_anios, jcr_3_anios, diff_3_anios,
                citas_2_anios, jcr_2_anios, diff_2_anios,
                citas_1_anios, jcr_1_anios, diff_1_anios,
                citas_este_anio]

        Raises:
            Exception: Si ocurre un error al obtener los datos para la predicción.
        """
        cur = self.conn.cursor()
        try:
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

            ejemplo = [
                int(citas_3_anios), float(jcr_3_anios), float(diff_3_anios),
                int(citas_2_anios), float(jcr_2_anios), float(diff_2_anios),
                int(citas_1_anios), float(jcr_1_anios), float(diff_1_anios),
                int(citas_este_anio)
            ]
            return ejemplo

        except psycopg2.Error as e:
            raise Exception("Error al obtener datos para la predicción: " + str(e))
        finally:
            cur.close()


    # Restablecer la BBDD

    # Módulo de creación de tablas
    def create_tables(self):
        """
        Crea las tablas necesarias en la base de datos.

        Raises:
            Exception: Si ocurre un error al crear las tablas.
        """
        cur = self.conn.cursor()
        try:
            cur.execute("""
                CREATE TABLE users (
                    username VARCHAR(255),
                    password VARCHAR(255),
                    email VARCHAR(255) PRIMARY KEY,
                    admin BOOLEAN,
                    image BYTEA
                );
                
                CREATE TABLE modelos (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT,
                    rmse FLOAT
                );
                
                CREATE TABLE revista (
                    nombre CHAR(255) PRIMARY KEY,
                    issn CHAR(9) UNIQUE NOT NULL,
                    categoria CHAR(255) NOT NULL
                );
                
                CREATE TABLE revista_jcr (
                    nombre CHAR(255) NOT NULL,
                    fecha NUMERIC NOT NULL, 
                    jcr FLOAT,
                    citas NUMERIC,
                    diff FLOAT,
                    cuartil CHAR(10)
                );
                
            """)

            self.conn.commit()
        except psycopg2.Error as e:
            raise Exception("Error al crear las tablas: " + str(e))
        finally:
            cur.close()


    # Módulo de carga de datos
    def load_data(self, csv_path, table_name, columns):
        """
        Carga los datos desde un archivo CSV en una tabla específica de la base de datos.

        Args:
            csv_path (str): Ruta del archivo CSV que contiene los datos a cargar.
            table_name (str): Nombre de la tabla en la que se cargarán los datos.
            columns (list): Lista de nombres de columnas correspondientes a los datos a cargar.

        Raises:
            Exception: Si ocurre un error al copiar los datos.
        """
        cur = self.conn.cursor()
        try:            
            with open(csv_path, 'r') as file:          
                # Generar la sentencia COPY personalizada
                copy_sql = f"COPY {table_name} ({', '.join(columns)}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER '|')"
                cur.copy_expert(copy_sql, file)

            self.conn.commit()
        except psycopg2.Error as e:
            raise Exception("Error copiando los datos: " + str(e))
        finally:
            cur.close()

        
    # Módulo de inserción de usuarios inicial
    def insert_users(self):
        """
        Inserta un usuario inicial en la base de datos.

        El usuario inicial tiene el nombre de usuario "Admin", la contraseña "p@ssw0rd",
        el correo electrónico "admin@example.com" y se le asigna el rol de administrador.

        Raises:
            Exception: Si ocurre un error al insertar el usuario.
        """
        cur = self.conn.cursor()
        try:
            # Password hasheada
            password = 'p@ssw0rd'
            password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(7))

            # Imagen default
            file_path = os.path.join(self.parent_directory, 'data', 'perfil.jpg')
            with open(file_path, 'rb') as file:
                image_data = file.read()

            query = """INSERT INTO users (username, password, email, admin, image) VALUES ('Admin', %s, 'admin@example.com', true, %s);"""
            cur.execute(query, (hashed_password, image_data))

            # Confirmar los cambios en la base de datos
            self.conn.commit()
        except psycopg2.Error as e:
            raise Exception("Error al insertar los usuarios: " + str(e))
        finally:
            cur.close()


    # Módulo para eliminar la información de la BBDD
    def drop_tables(self):
        """
        Elimina todas las tablas de la base de datos.

        Esto borrará permanentemente toda la información almacenada en las tablas revista,
        revista_jcr, citas, users y modelos.

        Raises:
            Exception: Si ocurre un error al eliminar las tablas.
        """
        cur = self.conn.cursor()
        try:
            # Eliminar tablas si ya existen
            cur.execute("""
                DROP TABLE IF EXISTS revista CASCADE;
                DROP TABLE IF EXISTS revista_jcr CASCADE;
                DROP TABLE IF EXISTS citas CASCADE;
                DROP TABLE IF EXISTS users CASCADE;
                DROP TABLE IF EXISTS modelos CASCADE;
            """)

            # Confirmar los cambios en la base de datos
            self.conn.commit()

        except psycopg2.Error as e:
            raise Exception("Error eliminando las tablas: " + str(e))
        finally:
            cur.close()

        
    # Módulo para comprobar si existen las tablas
    def check_tables(self):
        """
        Verifica si las tablas de la base de datos existen.

        Returns:
            bool: True si las tablas existen, False en caso contrario.
            
        Raises:
            Exception: Si ocurre un error al comprobar las tablas.
        """
        cur = self.conn.cursor()
        try:
            # Eliminar tablas si ya existen
            cur.execute("""
                SELECT EXISTS (
                SELECT 1
                FROM pg_tables
                WHERE tablename = 'users'
                );
            """)
            resultado = cur.fetchone()[0]
            return resultado
    
        except psycopg2.Error as e:
            raise Exception("Error eliminando las tablas: " + str(e))
        finally:
            cur.close()



    # Módulo principal de inicialización
    def initialize_database(self):
        """
        Inicializa la base de datos eliminando las tablas existentes, creando
        las tablas desde cero y cargando datos iniciales en la base de datos.

        Raises:
            Exception: Si ocurre un error al inicializar las tablas de la base de datos.
        """
        try:

            # Eliminar las tablas si existen previamente
            self.drop_tables()

            # Creación de las tablas de cero
            self.create_tables()

            # Cargar datos iniciales en la BBDD
            self.load_data(os.path.join(self.parent_directory, 'data', 'lista_revistas.csv'), 'revista', ('nombre', 'issn', 'categoria'))
            self.load_data(os.path.join(self.parent_directory, 'data', 'datos_combinados.csv'), 'revista_jcr', ('fecha', 'nombre', 'citas', 'jcr', 'diff', 'cuartil'))
            
            self.insert_users()
            self.insert_models()

        except psycopg2.Error as e:
            raise Exception("Error al inicializar las tablas de la base de datos: " + str(e))
        

    def validate_email(self, email):
        """
        Valida si un correo electrónico ya existe en la base de datos.
        Si ya existiese, no se puede registrar otro igual.

        Args:
            email (str): Correo electrónico a validar.

        Returns:
            bool: True si el correo electrónico no existe en la base de datos,
              False si ya existe.

        Raises:
            Exception: Si ocurre un error al realizar la validación.
        """
        cur = self.conn.cursor()
        try:
            # Eliminar tablas si ya existen
            query = """SELECT email FROM users"""
            cur.execute(query)
            emails = cur.fetchall()
            if (email,) in emails:
                resultado = False
            else:
                resultado = True
            return resultado
    
        except psycopg2.Error as e:
            raise Exception("Error eliminando las tablas: " + str(e))
        finally:
            cur.close()

        
    def validate_user(self, username):
        """
        Valida si un nombre de usuario ya existe en la base de datos.
        Si ya existiese, no se puede registrar otro igual.

        Args:
            username (str): Nombre de usuario a validar.

        Returns:
            bool: True si el nombre de usuario no existe en la base de datos,
              False si ya existe.

        Raises:
            Exception: Si ocurre un error al realizar la validación.
        """
        cur = self.conn.cursor()
        try:
            # Eliminar tablas si ya existen
            query = """SELECT username FROM users"""
            cur.execute(query)
            usernames = cur.fetchall()
            if (username,) in usernames:
                resultado = False
            else:
                resultado = True
            return resultado
        except Exception as e:
            return {"error": str(e)}
        finally:
            cur.close()

        
    def insert_profile_picture(self, image, username):
        """
        Inserta una imagen de perfil para un usuario en la base de datos.

        Args:
            image (file): Archivo de imagen de perfil.
            username (str): Nombre de usuario al que se le asignará la imagen.

        Returns:
            bool: True si la imagen de perfil se inserta correctamente, 
            False en caso contrario.

        Raises:
            Exception: Si ocurre un error al insertar la imagen de perfil.
        """
        cur = self.conn.cursor()
        try:
            query = "UPDATE users SET image = %s WHERE username = %s"
            cur.execute(query, (image.read(), username))
            self.conn.commit()
            return True
        except (psycopg2.Error, Exception) as error:
            self.conn.rollback()
            return False
        finally:
            cur.close()

    def get_profile_picture(self, username):
        """
        Obtiene la imagen de perfil de un usuario de la base de datos
        para poder mostrarla.

        Args:
            username (str): Nombre de usuario del cual se desea obtener
              la imagen de perfil.

        Returns:
            str or None: Cadena Base64 que representa la imagen de perfil
              si se encuentra, None si no se encuentra o ocurre un error.

        Raises:
            Exception: Si ocurre un error al obtener la imagen de perfil.
        """
        cur = self.conn.cursor()
        try:
            query = "SELECT image FROM users WHERE username = %s"
            cur.execute(query, (username,))
            result = cur.fetchone()
            if result:
                image_data = result[0]
                image_base64 = base64.b64encode(image_data).decode('utf-8')  # Convertir a cadena Base64
                return image_base64
            else:
                return None
        except (psycopg2.Error, Exception) as error:
            return f'Error al obtener la imagen: {str(error)}'
        finally:
            cur.close()


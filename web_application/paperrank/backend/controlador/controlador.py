"""
La clase Controlador tiene un constructor que recibe como 
parámetro una instancia del modelo. Se encarga de ajustar 
la lógica de negocio de la aplicación manejando estructuras 
de datos así como de la comunicación con Modelo.

============================
  Trabajo de Fin de Grado
Universidad de Burgos (UBU)
============================

Autor: Gadea Lucas Pérez
Año: 2023

"""
import datetime

class Controlador:
    
    def __init__(self, modelo):
        self.modelo = modelo
    
    
    def obtener_indice_impacto(self, revista):
        """
        Obtiene el índice de impacto de una revista.

        Args:
            revista (str): Nombre de la revista.

        Returns:
            float or dict: Índice de impacto redondeado si se encuentra, 
            diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener el índice de impacto.
        """
        try:
            indice = round(self.modelo.obtener_indice_impacto(revista),4)
            return indice
        except Exception as e:
            return {"error": str(e)}
        
    def get_journals(self):
        """
        Obtiene la lista de revistas.

        Returns:
            list or dict: Lista de revistas si se obtiene correctamente,
              diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener la lista de revistas.
        """
        try:
            journals = []
            for journal in self.modelo.get_journals():
                nombre = journal.nombre
                issn = journal.issn
                categoria = journal.categoria
                journals.append((nombre.rstrip(), issn.rstrip(), categoria.rstrip()))
            return journals
        except Exception as e:
            return {"error": str(e)}
        
    def get_journals_list(self):
        """
        Obtiene la lista de revistas con información adicional.

        Returns:
            list or dict: Lista de revistas con información adicional si se obtiene
              correctamente, diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener la lista de revistas.
        """
        try:
            journals = self.get_journals()
            journal_data = []

            for journal in journals:
                nombre = journal[0]
                issn = journal[1]
                categoria = journal[2]
                last_jcr = self.modelo.get_last_jcr(nombre)
                last_cuartil = self.modelo.get_last_cuartil(nombre)
                last_jcr = [valor if valor is not None else "-" for valor in last_jcr]
                last_cuartil = [valor if valor is not None else "-" for valor in last_cuartil]
                journal_tuple = (nombre, issn, categoria, last_jcr, last_cuartil)
                journal_data.append(journal_tuple)

            return journal_data

        except Exception as e:
            return {"error": str(e)}
    
        
    def get_journals_name(self):
        """
        Obtiene los nombres de las revistas.

        Returns:
            list or dict: Lista de nombres de revistas si se obtiene correctamente,
              diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener los nombres de revistas.
        """
        try:
            names = []
            for journal in self.modelo.get_journals():
                names.append(journal.nombre.rstrip())
            return names
        except Exception as e:
            return {"error": str(e)}
    
    def get_year_range(self):
        """
        Obtiene el rango de años.

        Returns:
            list or dict: Lista de años si se obtiene correctamente, 
            diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener el rango de años.
        """
        try:
            year = self.modelo.get_year_range()
            min_year = min(year)
            max_year = max(year)
            years = []
            for anio in range(min_year, max_year + 1):
               years.append(anio)
            return years
        except Exception as e:
            return {"error": str(e)}
        
    def get_categories(self):
        """
        Obtiene las categorías de las revistas.

        Returns:
            list or dict: Lista de categorías si se obtiene correctamente, 
            diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener las categorías de revistas.
        """
        try:
            categories = []
            for journal in self.modelo.get_journals():
                categories.append(journal.categoria)
            return list(set(categories))
        except Exception as e:
            return {"error": str(e)}
        
    def get_revistas_por_categoria(self, categoria):
        """
        Obtiene las revistas por categoría.

        Args:
            categoria (str): Categoría de las revistas.

        Returns:
            list or dict: Lista de revistas de la categoría especificada si 
            se obtiene correctamente, diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener las revistas por categoría.
        """
        try:
            journals = []
            for journal in self.modelo.get_journals():
                if journal.categoria.rstrip() == categoria:

                    journals.append(journal.nombre)
            return journals
        except Exception as e:
            return {"error": str(e)}
        
    def authenticate_user(self, username, password):
        """
        Autentica al usuario.

        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña del usuario.

        Returns:
            bool or dict: True si la autenticación es exitosa, False si la 
            autenticación falla, diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al autenticar al usuario.
        """
        try:
            done = self.modelo.authenticate_user(username, password)
            return done
        except Exception as e:
            return {"error": str(e)}

    def create_user(self, username, password, email, admin=False):
        """
        Crea un nuevo usuario.

        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña del usuario.
            email (str): Dirección de correo electrónico del usuario.
            admin (bool, optional): Indica si el usuario es administrador. 
            Por defecto es False.

        Returns:
            bool or dict: True si el usuario se crea correctamente, 
            False si ocurre algún error, 
            diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al crear el usuario.
        """
        try:
            done = self.modelo.create_user(username, password, email, admin)
            return done
        except Exception as e:
            return {"error": str(e)}
        
    def update_user(self, new_username, new_email, old_email):
        """
        Actualiza los datos de un usuario.

        Args:
            new_username (str): Nuevo nombre de usuario.
            new_email (str): Nueva dirección de correo electrónico.
            old_email (str): Dirección de correo electrónico actual.

        Returns:
            bool or dict: True si la actualización es exitosa, False si la actualización
              falla, diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al actualizar el usuario.
        """
        try:
            done = self.modelo.update_user( new_username, new_email, old_email)
            return done
        except Exception as e:
            return {"error": str(e)}
        
    def initialize_database(self):
        """
        Inicializa la base de datos solo si no existen las tablas.

        Returns:
            dict: Diccionario vacío si se inicializa correctamente, 
            diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al inicializar la base de datos.
        """
        try:
            if not self.modelo.check_tables():
                self.modelo.initialize_database()

        except Exception as e:
            return {"error": str(e)}
        
    def reinitialize_database(self):
        """
        Reinicializa la base de datos borrando las tablas existentes.

        Returns:
            dict: Diccionario vacío si se reinicializa correctamente, 
            diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al reinicializar la base de datos.
         """
        try:
            self.modelo.initialize_database()

        except Exception as e:
            return {"error": str(e)}
        
    def insert_models(self):
        """
        Inserta los modelos.

        Returns:
            None or dict: None si se insertan correctamente, 
            diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al insertar los modelos.
        """
        try:
            self.modelo.insert_models()
        except Exception as e:
            return {"error": str(e)}

    def get_model_names_and_errors(self):
        """
        Obtiene los nombres y errores de los modelos.
        Solo valdrán aquellos modelos con RMSE inferior a 6.

        Returns:
            list or dict: Lista de nombres y errores de los modelos 
            si se obtiene correctamente, diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener los nombres y errores de los modelos.
        """
        try:
            results = []
            for elem in self.modelo.get_model_names_and_errors():
                if elem['rmse'] < 6: # Líneas futuras: parametrizar (admin)
                    elem['rmse'] = round(elem['rmse'], 2)
                    results.append(elem)
            return results
        except Exception as e:
            return {"error": str(e)}

    def get_model_binaries(self, nombres_modelos):
        """
        Obtiene los archivos binarios de los modelos de predicción.

        Args:
            nombres_modelos (list): Lista de nombres de los modelos.

        Returns:
            dict or None: Diccionario con los nombres de los modelos y 
            sus archivos binarios si se obtienen correctamente, 
            diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener los archivos binarios de los modelos.
        """
        try:
            results = self.modelo.get_model_binaries(nombres_modelos)
            return results
        except Exception as e:
            return {"error": str(e)}

    def get_last_year(self, nombre_revista):
        """
        Obtiene el último año con datos reales 
        disponible para una revista.

        Args:
            nombre_revista (str): Nombre de la revista.

        Returns:
            int or dict: Último año disponible si se obtiene correctamente,
              diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener el último año disponible.
        """
        try:
            last_year = int(self.modelo.get_last_year())
        
            return last_year
        except Exception as e:
            return {"error": str(e)}
        
    def get_consulta_quartil(self, nombre_revista):
        """
        Obtiene la consulta de cuartiles para una revista en los últimos 5 años.

        Args:
            nombre_revista (str): Nombre de la revista.

        Returns:
            list or dict: Lista de tuplas (año, cuartil) si se obtiene correctamente,
              diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener la consulta de cuartiles.
        """
        try:
            last_year = int(self.modelo.get_last_year())
            results = []

            for anio in range(last_year, last_year-5, -1):
                cuartil = self.modelo.get_quartil(nombre_revista, anio)
                tupla = (anio, cuartil)
                results.append(tupla)
            return results
        except Exception as e:
            return {"error": str(e)}

    def get_consulta_jcr(self, nombre_revista):
        """
        Obtiene la consulta de valores JCR (Journal Citation Reports) 
        para una revista en los últimos 5 años.

        Args:
            nombre_revista (str): Nombre de la revista.

        Returns:
            list or dict: Lista de tuplas (año, JCR) si se obtiene correctamente,
              diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener la consulta de valores JCR.
        """
        try:
            last_year = last_year = int(self.modelo.get_last_year())
            results = []

            for anio in range(last_year, last_year-5, -1):
                jcr = self.modelo.get_jcr(nombre_revista, anio)
                tupla = (anio, jcr)
                results.append(tupla)
            return results
        except Exception as e:
            return {"error": str(e)}
        
    def get_ejemplo(self, nombre_revista):
        """
        Obtiene ejemplos de datos para una revista en el año actual y el año anterior.

        Args:
            nombre_revista (str): Nombre de la revista.

        Returns:
            tuple or dict: Tupla con los ejemplos de datos del año actual y el año
            anterior si se obtienen correctamente, diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener los ejemplos de datos.
        """
        try:
            curr_year = datetime.datetime.now().year
            this_year_ex = self.modelo.get_ejemplo(nombre_revista, curr_year)
            last_year_ex = self.modelo.get_ejemplo(nombre_revista, curr_year - 1)
            return this_year_ex, last_year_ex
        except Exception as e:
            return {"error": str(e)}
        
    def predict(self, ejemplo, modelos):
        """
        Realiza predicciones utilizando los modelos especificados.

        Args:
            ejemplo (list): Ejemplo de datos para realizar la predicción.
            modelos (dict): Diccionario de modelos, donde las claves son 
            los nombres de los modelos y los valores son las instancias de los modelos.

        Returns:
            list or dict: Lista de predicciones realizadas por los 
            modelos si se ejecuta correctamente, diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al realizar las predicciones.
        """
        try:
            predicciones = []
            for nombre, model in modelos.items():
                prediccion = model.predict([ejemplo])
                predicciones.append(prediccion)
            return predicciones
        except Exception as e:
            return {"error": str(e)}
        
    def get_email(self, username):
        """
        Obtiene el correo electrónico asociado al nombre de usuario especificado.

        Args:
            username (str): Nombre de usuario.

        Returns:
            str or dict: Correo electrónico asociado al nombre de usuario si se encuentra,
                        diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al obtener el correo electrónico.
        """
        try:
            email = self.modelo.get_email(username)
            return email
        except Exception as e:
            return {"error": str(e)}
        
    def validate_email(self, email):
        """
        Valida si el correo electrónico ya está registrado en la base de datos.

        Args:
            email (str): Correo electrónico a validar.

        Returns:
            bool or dict: True si el correo electrónico es válido (no está registrado),
                        False si el correo electrónico ya está registrado,
                        diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al validar el correo electrónico.
        """
        try:
            resultado = self.modelo.validate_email(email)
            return resultado
        except Exception as e:
            return {"error": str(e)}
        
    def validate_user(self, username):
        """
        Valida si el nombre de usuario ya está registrado en la base de datos.

        Args:
            username (str): Nombre de usuario a validar.

        Returns:
            bool or dict: True si el nombre de usuario es válido (no está registrado),
                        False si el nombre de usuario ya está registrado,
                        diccionario de error si ocurre algún error.

        Raises:
            Exception: Si ocurre un error al validar el nombre de usuario.
        """
        try:
            resultado = self.modelo.validate_user(username)
            return resultado
        except Exception as e:
            return {"error": str(e)}


    def insert_profile_picture(self, image, username):
        """
        Inserta una imagen de perfil para el usuario especificado.

        Args:
            image (bytes): Imagen de perfil en formato bytes.
            username (str): Nombre de usuario.

        Returns:
            bool or dict: True si se insertó la imagen correctamente, 
            False si ocurrió un error.
        """
        try:
            done = self.modelo.insert_profile_picture(image, username)
            return done
        except Exception as e:
            return {"error": str(e)}
        
    def get_profile_picture(self, username):
        """
        Obtiene la imagen de perfil asociada al nombre de usuario especificado.

        Args:
            username (str): Nombre de usuario.

        Returns:
            str or None or dict: Cadena Base64 que representa la imagen
              de perfil si existe,
            None si no se encuentra una imagen para el usuario, o un 
            diccionario de error si ocurre una excepción.
        """
        try:
            image = self.modelo.get_profile_picture(username)
            return image
        except Exception as e:
            return {"error": str(e)}
    
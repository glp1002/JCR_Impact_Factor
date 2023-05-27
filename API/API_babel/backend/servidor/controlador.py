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
        try:
            articulos = [] 
            for articulo in self.modelo.obtener_articulos(revista):
                nombre = articulo.nombre
                DOI = articulo.DOI
                revista = articulo.revista
                ncitas = articulo.ncitas
                fecha = articulo.fecha
                articulos.append((nombre.rstrip(), DOI.rstrip(), revista.rstrip(), ncitas, fecha))
            return articulos
        except Exception as e:
            return {"error": str(e)}

    def obtener_indice_impacto(self, revista):
        try:
            indice = round(self.modelo.obtener_indice_impacto(revista),4)
            return indice
        except Exception as e:
            return {"error": str(e)}
        
    def get_journals(self):
        try:
            journals = []
            for journal in self.modelo.get_journals():
                nombre = journal.nombre
                ISSN = journal.ISSN
                categoria = journal.categoria
                journals.append((nombre.rstrip(), ISSN.rstrip(), categoria.rstrip()))
            return journals
        except Exception as e:
            return {"error": str(e)}
        
    def get_journals_list(self):
        try:
            journals = self.get_journals()
            journal_data = []

            for journal in journals:
                nombre = journal[0]
                issn = journal[1]
                categoria = journal[2]
                last_jcr = self.modelo.get_last_jcr(nombre)
                journal_tuple = (nombre, issn, categoria, last_jcr)
                journal_data.append(journal_tuple)

            return journal_data

        except Exception as e:
            return {"error": str(e)}
        
    def get_journals_name(self):
        try:
            names = []
            for journal in self.modelo.get_journals():
                names.append(journal.nombre.rstrip())
            return names
        except Exception as e:
            return {"error": str(e)}
    
    def get_year_range(self):
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
        try:
            categories = []
            for journal in self.modelo.get_journals():
                categories.append(journal.categoria)
            return list(set(categories))
        except Exception as e:
            return {"error": str(e)}
        
    def get_revistas_por_categoria(self, categoria):
        try:
            journals = []
            journals = self.modelo.get_revistas_por_categoria(categoria)
            return journals
        except Exception as e:
            return {"error": str(e)}
        
    def authenticate_user(self, username, password):
        try:
            id_user = self.modelo.authenticate_user(username, password)
            return id_user
        except Exception as e:
            return {"error": str(e)}

    def create_user(self, username, password, email, admin=False):
        try:
            done = self.modelo.create_user(username, password, email, admin)
            return done
        except Exception as e:
            return {"error": str(e)}
    
    def get_users_by_role(self, admin=False):
        try:
            users = []
            for user in self.modelo.get_users_by_role(admin):
                id = user.id
                username = user.username
                password = user.password
                email = user.email
                admin = user.admin
                users.append((id, username, password, email, admin))
            return users
        except Exception as e:
            return {"error": str(e)}
        
    def update_user(self, user_id, new_username, new_password, new_email, new_admin):
        try:
            done = self.modelo.update_user(user_id, new_username, new_password, new_email, new_admin)
            return done
        except Exception as e:
            return {"error": str(e)}
        
    def delete_user(self, user_id):
        try:
            done = self.modelo.delete_user(user_id)
            return done
        except Exception as e:
            return {"error": str(e)}
        
    def initialize_database(self):
        try:
            done = self.modelo.initialize_database()
            return done
        except Exception as e:
            return {"error": str(e)}
        
    def insert_models(self):
        try:
            self.modelo.insert_models()
        except Exception as e:
            return {"error": str(e)}

    def get_model_names_and_errors(self):
        try:
            results = []
            for elem in self.modelo.get_model_names_and_errors():
                if elem['rmse'] < 6: # TODO: parametrizar
                    elem['rmse'] = round(elem['rmse'], 2)
                    results.append(elem)
            return results
        except Exception as e:
            return {"error": str(e)}

    def get_model_binaries(self, nombres_modelos):
        try:
            results = self.modelo.get_model_binaries(nombres_modelos)
            return results
        except Exception as e:
            return {"error": str(e)}
        
    def get_ejemplo(self, revista, anio):
        try:
            ejemplo = self.modelo.get_ejemplo(revista, anio)
            return ejemplo
        except Exception as e:
            return {"error": str(e)}
        
    def predict(self, ejemplo, modelos):
        try:
            predicciones = []
            for nombre, modelo in modelos.items():
                prediccion = modelo.predict(ejemplo)
                predicciones.append(prediccion)
            return predicciones
        except Exception as e:
            return {"error": str(e)}
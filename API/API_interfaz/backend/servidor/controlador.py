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
        
    def authenticate_user(self, username, password):
        try:
            id_user = self.modelo.authenticate_user(username, password)
            return id_user
        except Exception as e:
            return {"error": str(e)}

    def create_user(self, username, password):
        try:
            done = self.modelo.create_user(username, password)
            return done
        except Exception as e:
            return {"error": str(e)}

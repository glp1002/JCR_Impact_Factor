import pandas as pd
import os
import re

CATEGORIA = "COMPUTER SCIENCE, ARTIFICIAL INTELLIGENCE"
path = "./resultados2"

# Lista para almacenar los resultados
resultados = []

# Iterar por los archivos en la carpeta
for nombre_archivo in os.listdir(path):
    if nombre_archivo.endswith(".csv"):
        # Extraer el número ISSN del nombre del archivo
        match = re.search(r"resultados_(\d{4}-\d{4})", nombre_archivo)
        if match:
            issn = match.group(1)
            
            try:
                df = pd.read_csv(os.path.join(path, nombre_archivo))
                
                # Verificar si el archivo tiene datos
                if not df.empty:
                    # Extraer ISSN y nombre de la revista
                    issn_revista = issn
                    nombre_revista = df['Revista'].unique()[0]
                    
                    # Agregar a la lista de resultados
                    resultados.append([nombre_revista, issn_revista, CATEGORIA])
            except pd.errors.EmptyDataError:
                # El archivo está vacío, continuar con el siguiente
                continue

# Crear un DataFrame a partir de los resultados
df_resultados = pd.DataFrame(resultados, columns=['Revista', 'ISSN', 'Categoría'])

# Guardar los resultados en un nuevo archivo CSV
df_resultados.to_csv('lista_revistas.csv', index=False)
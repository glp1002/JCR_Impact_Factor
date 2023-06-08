import numpy as np
import pandas as pd

# Leer los datos del archivo CSV
df_csv = pd.read_csv('./datos_combinados.csv', encoding='utf-8')

# Crear una lista para almacenar los datos de los cuartiles
cuartiles = []

# Iterar sobre cada fila del DataFrame
for index, row in df_csv.iterrows():
    # Obtener el año y el nombre de la revista
    year = row['Anio']
    journal = row['Revista']
    
    # Crear el nombre del archivo Excel correspondiente al año
    excel_file = f'./JCR_AI_{year}.xlsx'    
        
        
    try:
        # Leer los datos del archivo Excel
        df_excel = pd.read_excel(excel_file,  header=0)
        
        # Filtrar los datos por el nombre de la revista
        filtered_df = df_excel[df_excel['Journal name'] == journal]
        
        # Obtener el cuartil de la columna 'JIF Quartile'
        cuartil = filtered_df.iloc[0]['JIF Quartile']
        
        # Agregar el cuartil a la lista
        cuartiles.append(cuartil)
        
    except FileNotFoundError:
        # En caso de que no se encuentre el archivo Excel, agregar un valor vacío a la lista
        cuartiles.append('')
    
# Agregar la lista de cuartiles como una nueva columna en el DataFrame
df_csv['Cuartil'] = cuartiles

# Guardar los datos actualizados en un nuevo archivo CSV
df_csv.to_csv('archivo_actualizado.csv', index=False)

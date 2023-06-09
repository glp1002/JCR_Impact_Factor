import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('./datos_combinados.csv', encoding='utf-8')

# Leer los archivos Excel para cada año
jcr_files = {
    2017: './JCR_AI_2017.xlsx',
    2018: './JCR_AI_2018.xlsx',
    2019: './JCR_AI_2019.xlsx',
    2020: './JCR_AI_2020.xlsx',
    2021: './JCR_AI_2021.xlsx'
}

# Crear una función para obtener el cuartil de una revista en un año determinado
def get_quartile(row):
    year = row['Anio']
    journal = row['Revista'].lower() 
    jcr_file = jcr_files.get(year)

    if jcr_file:
        jcr_df = pd.read_excel(jcr_file, header=0)
        jcr_df['Journal name'] = jcr_df['Journal name'].str.lower()  # Convertir a minúsculas
        quartile = jcr_df[jcr_df['Journal name'] == journal]['JIF Quartile'].values
        if quartile.size > 0:
            return quartile[0]
    return None

# Aplicar la función para obtener el cuartil y agregarlo como una nueva columna
df['Quartile'] = df.apply(get_quartile, axis=1)

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv('archivo_con_cuartil.csv', index=False)

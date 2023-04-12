import csv
from numpy import NaN
import pandas as pd

archivo = pd.read_csv("listas_jcr\JCR_AI_2022.csv", quotechar='"')
cambiar = pd.read_csv("listas_jcr\JCR_AI_2020.csv", quotechar='"')



# fusionar ambos dataframes usando 'JCR Abbreviation' como clave de unión
df = pd.merge(cambiar, archivo, on='Journal name', how='left')

df.fillna('N/A', inplace=True)
print(df)

# reordenar las columnas del dataframe
df = df[['Journal name', 'JCR Abbreviation_y', 'ISSN_x', 'eISSN_y', 'Category_y', 'Total Citations_x', '2020 JIF']]

df = df.rename(columns={
                                      'JCR Abbreviation_y':'JCR Abbreviation',
                                      'ISSN_x': 'ISSN', 
                                      'eISSN_y': 'eISSN',
                                      'Total Citations_x': 'Total Citations',
                                      'Category_y':  'Category'
                                      })

# guardar el resultado final en un archivo CSV
df.to_csv('listas_jcr\JCR_AI_2020.csv', index=False)

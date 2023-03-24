"""
Módulo para el cálculo del JCR a partir de los datos extraidos.

============================
  Trabajo de Fin de Grado
Universidad de Burgos (UBU)
============================

Autor: Gadea Lucas Pérez
Año: 2023
"""

import os
import math
import pandas as pd
import csv
import matplotlib.pyplot as plt


def getJCR(anio_i: int):
    """
    Calcula el JCR de cada revista a partir de los archivos de citas descargados de Web of Science.

    Parámetros:
    -----------
    - anio_i (int): Año base para calcular el JCR. Se tendrán en cuenta los artículos publicados
        en los dos años anteriores a este.

    Returns:
    --------
    - dict: Diccionario que asocia a cada ISSN el JCR y el nombre de la revista correspondiente.

    """
    jcr_por_revista = {}

    # Recorrer todos los ficheros en la carpeta "resultados"
    for nombre_fichero in os.listdir("resultados"):
        if nombre_fichero.startswith("resultados_") and nombre_fichero.endswith(".csv"):
            
            # Obtener el ISSN de la revista a partir del nombre del fichero
            issn = nombre_fichero.split("_")[1].split(".")[0]
            
            with open(os.path.join("resultados", nombre_fichero), "r", encoding="utf-8") as f:
                next(f) # Omitir la primera línea si contiene los encabezados de las columnas
                
                citas_jcr = 0
                num_art = 0
                
                for linea in f:
                    # Obtener el año y el número de citas recibidas de cada artículo
                    campos = linea.strip().split(",")
                    
                    if len(campos) == 6:
                        doi, titulo, autores, anio, num_citas, revista = campos   
                        anio = int(anio)                 
                        # Si se trata de los años adecuados, se registran
                        if anio == anio_i-1 or anio == anio_i-2:
                            citas_jcr += int(num_citas)
                            num_art += 1
                            
                # Cálculo del JCR
                jcr = citas_jcr / num_art if num_art != 0 else 0
                
                # Se añade la revista con su JCR   
                jcr_por_revista[issn] = (jcr, revista)    
                        
    return jcr_por_revista


def comparar(obtenido:dict, anio:int)-> tuple:
    '''
    Compara los valores obtenidos para el factor de impacto (JCR) de un conjunto de revistas con los valores esperados
    que se encuentran en un archivo CSV de la base de datos JCR (Journal Citation Reports) de Clarivate.
    
    Parámetros:
    -----------
    - obtenido: dict
        Diccionario con los ISSN de las revistas obtenidas por nosotros y su correspondiente valor de JCR.
    - anio: int
        Entero que indica el año para el cuál se quiere comparar los valores de JCR.
    
    Returns:
    --------
    - resultado: tuple
        Tupla que contiene una lista de tuplas con la información de cada revista que se ha comparado. Cada tupla 
        contiene el nombre de la revista, el valor de JCR obtenido y el valor de JCR esperado.
    '''
    
    num_errores = 0
    num_omitidos = 0
    num_exitos = 0
    media = 0
    resultado =  []
    
    # Se lee el ficehro xml de Clarivate        
    esperado = pd.read_csv('./listas_jcr/JCR_AI_'+ str(anio) + '.csv', delimiter=',', quotechar='"',  header=0, index_col=False)

    # Se extraen los issn de las revistas obtenidas por nosotros
    revistas_obtenidas = obtenido.keys()
    # Se extraen los issn de las revistas del fichero
    issn = esperado.iloc[:, 2]
    eissn = esperado.iloc[:, 3].tolist()
    revistas_esperadas = issn.fillna(pd.Series(eissn)).tolist()
        

    # Si la revista aparece en ambas listas, se compara se JCR
    for revista in revistas_obtenidas:
        if revista in revistas_esperadas:
            
            # Obtenemos nuestro JCR 
            jcr_obtenido = obtenido[revista][0]
            
            # Obtenemos el JCR real
            jcr_esperado = esperado.loc[esperado["ISSN"] == revista].iloc[:,6].tolist()
            if len(jcr_esperado) == 0:
                jcr_esperado = esperado.loc[esperado["eISSN"] == revista].iloc[:,6].tolist()
            jcr_esperado = jcr_esperado[0]
            if math.isnan(jcr_esperado): # Si es N/A, se deja como 0
                jcr_esperado = 0.0

            # Se comparan los JCR
            if jcr_esperado != jcr_obtenido:
                num_errores = num_errores + 1
                media = media + abs(jcr_esperado-jcr_obtenido)
                #print(f"La revista {obtenido[revista][1]} tiene un error de {abs(jcr_esperado-jcr_obtenido)}.")
            else:
                num_exitos = num_exitos + 1
                #print(f"La revista {obtenido[revista][1]} es un éxito.")
                
            # Almacenamos los resultados
            resultado.append( (obtenido[revista][1], jcr_obtenido, jcr_esperado) )

        else:
            num_omitidos = num_omitidos + 1
            print(f"La revista {obtenido[revista][1]} está omitida.")
            
    # print(f"Se han logrado {num_exitos} exitos.")
    # print(f"Se han cometido {num_errores} errores.")
    # print(f"Se han omitido {num_omitidos} cálculos.")
    # print(f"La probabilidad de fallo es {(num_errores/len(obtenido))*100} %.") 
    # print(f"La media del margen de error es de {media/len(obtenido)}.") 

    return resultado
    

def genFiles(anios:list, data:dict) -> None:
    """
    Genera tres archivos CSV a partir de un diccionario que contiene la información de las revistas y sus JCR
    en diferentes años. Los archivos son:
    - jcr_obtenido.csv: Contiene los valores de Crossref de los JCR para cada revista en cada año.
    - jcr_esperado.csv: Contiene los valores de Clarivate de los JCR para cada revista en cada año.
    - diferencias.csv: Contiene la diferencia entre los valores esperados y obtenidos de los JCR para cada 
        revista en cada año.

    Parámetros:
    -----------
    - anios (list): Lista de años en los que se tienen valores de JCR.
    - data (dict): Diccionario que contiene la información de las revistas y sus JCR en diferentes años.

    Returns:
    --------
    - None: La función no retorna ningún valor.
    
    """  
    # Definir los nombres de las columnas del archivo CSV
    header = ['Revista'] + [f'JCR {anio}' for anio in anios]

    # Crear una lista de diccionarios con los datos de las revistas y sus JCR en cada año
    data_esperado = []
    data_obtenido = []
    data_diferencias = []
    for revista in data:
        row_esperado = {'Revista': revista}
        row_obtenido = {'Revista': revista}
        row_diferencias = {'Revista': revista}
        for jcr in data[revista]:
            for anio in anios:
                if f'JCR {anio}' in jcr:
                    esperado, obtenido = jcr[f'JCR {anio}']
                    row_esperado[f'JCR {anio}'] = round(esperado,3)
                    row_obtenido[f'JCR {anio}'] = obtenido
                    row_diferencias[f'JCR {anio}'] = round(abs(obtenido - esperado),3)
        data_esperado.append(row_esperado)
        data_obtenido.append(row_obtenido)
        data_diferencias.append(row_diferencias)

    # Escribir los archivos CSV
    with open('jcr_obtenido.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data_esperado:
            writer.writerow(row)

    with open('jcr_esperado.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data_obtenido:
            writer.writerow(row)
    
    with open('diferencias.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data_diferencias:
            writer.writerow(row)

def genRanking() -> None:
    df = pd.read_csv('jcr_obtenido.csv', delimiter=",", header=0)
    # años como índices
    df_transposed = df.transpose() 
    # ranking
    df_ranking = df_transposed.iloc[1:].rank(ascending=False, axis=1, method='min') 
    # Generar el fichero
    df_ranking = df_ranking.transpose()
    df_ranking.insert(0, "Revista", df["Revista"])
    df_ranking.to_csv('ranking.csv', index=False)
    
def genBoxGraph() -> None:
    df = pd.read_csv('diferencias.csv', delimiter=",", header=0)
    
    # Columnas a graficarz
    data = df.iloc[:, 16:] # Últimos 4 años
    data = data.fillna(0)

    # Crea el diagrama de cajas
    fig, ax = plt.subplots()
    ax.boxplot(data.values)

    # Configura las etiquetas del eje x
    ax.set_xticklabels(data.columns, rotation=90)

    # Configura el título y etiquetas de los ejes
    ax.set_title('Diagrama de cajas de JCR')
    ax.set_xlabel('Año')
    ax.set_ylabel('Valor de diferencias')

    # Muestra la gráfica
    plt.show()
    plt.savefig("diagrama_cajas.png")






def main(anio_i:int, anio_f:int):
    anios = []
    data = {}
    
    # Se extrae la totalidad de los años
    for anio in range(anio_i, anio_f + 1):
        anios.append(anio)
        print(f"\nAÑO {anio}.\n----------\n")
        
        # Cálculo del Factor de Impacto
        obtenido = getJCR(anio)
        # print(f"El número total de revistas es {len(obtenido)}.")

        # Comparación
        lista = comparar(obtenido, anio)

        # Ordenamos los resultados
        for elem in lista:  
            if not elem[0] in data.keys():
                data[ elem[0] ] = [] 
            # Estructura -> { Revista: revista } : [ {año: (esperados, obtenidos)} ]
            data[elem[0]].append({f'JCR {anio}': (elem[1],elem[2])})
            
    # Escribir resultados
    genFiles(anios, data)
    genRanking()
    genBoxGraph()
        
        
        
    
if __name__ == '__main__':
    main(2004, 2022)
   







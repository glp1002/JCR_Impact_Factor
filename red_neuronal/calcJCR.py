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
import pandas as pd




def getJCR(anio_i:int):
    # Crear diccionario vacío para almacenar los JCR de cada revista
    jcr_por_revista = {}

    # Recorrer todos los ficheros en la carpeta "resultados" que tengan el patrón "resultados_issn.csv"
    for nombre_fichero in os.listdir("resultados"):
        if nombre_fichero.startswith("resultados_") and nombre_fichero.endswith(".csv"):
            # Abrir el fichero y leer cada línea
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
                            citas_jcr = citas_jcr + int(num_citas)
                            num_art = num_art + 1
                            
                # Cálculo del JCR
                if num_art != 0:
                    jcr = citas_jcr / num_art
                else:
                    jcr = 0
                
                # Se añade la revista con su JCR   
                jcr_por_revista[revista] = jcr 
                
    return jcr_por_revista


def comparar(obtenido:dict)-> tuple:
    num_errores = 0
    num_omitidos = 0 
    
    # Se lee el ficehro xml de Clarivate
    esperado = pd.read_excel('Journal-Impact-Factor-2019-XLS.xlsx')
    
    # Se extrae el factor de impacto de las revistas necesitadas
    revistas = esperado.iloc[1]
    
    for revista in obtenido.keys():
        
        # Si aparece la revista, se compara
        if revista in revistas:
            jcr_esperado = esperado.loc[:, 1] == revista.upper()
            jcr_obtenido = obtenido[revista]
            
            # Se comparan
            if jcr_esperado.iloc[3] != jcr_obtenido:
                num_errores = num_errores + 1
        else:
            num_omitidos = num_omitidos + 1
            
    return num_errores, num_omitidos



def main(anio_i:int):
    obtenido = getJCR(anio_i)
    print(f"El número total de revistas es {len(obtenido)}.")

    errores, omitidos = comparar(obtenido)
    print(f"Se han cometido {errores} errores.")
    print(f"Se han omitido {omitidos} cálculos.")
    print(f"El porcentaje de fallos es {(errores/len(obtenido))*100}") 
    
    
if __name__ == '__main__':
    main(2020)
   







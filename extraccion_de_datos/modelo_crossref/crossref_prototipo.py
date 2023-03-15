"""
Módulo que contiene las funciones de extracción de datos de la API de Crossref.

============================
  Trabajo de Fin de Grado
Universidad de Burgos (UBU)
============================

Autor: Gadea Lucas Pérez
Año: 2023
"""

import datetime
import logging
import re
import csv

import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configuración del archivo de "log"
logger = logging.getLogger('crossref_log')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('crossref.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


# Definición de métodos
def journalExist(issn: str, journal: str) -> bool:
    """
    Verifica si una revista existe en la base de datos de Crossref.

    Parameters:
        issn (str): El identificador ISSN de la revista que se desea buscar en la base de datos de Crossref. 
        journal (str): El nombre de la revista que deseas buscar en la base de datos de Crossref.

    Returns:
        bool: Devuelve True si la revista existe en la base de datos, de lo contrario devuelve False.

    Ejemplo:
        >>> journalExist('2326-3814','IEEE Transactions on Computers')
        [START] Extracción de la revista IEEE Transactions on Computers
        True
        >>> journalExist('12345-12345','Nonexistent Journal')
        [WARNING] La revista Nonexistent Journal no existe.
        False
    """
    # Especifica los parámetros de búsqueda de la API de Crossref
    url = f"https://api.crossref.org/journals/{issn}"
    
    # Realiza una solicitud GET a la API de Crossref con los parámetros de búsqueda especificados
    response = requests.get(url)
    
    # Si la solicitud es exitosa, se procede a extraer sus artículos 
    if response.ok:
        data = response.json()
        
        if 'title' in data['message']:
            logger.info(f'Extraccion de la revista {journal}')
            return True
        else:
            logger.warning(f'La revista {journal} no existe.')
            return False
    else:
        logger.error(f'Error para "{journal}" al realizar la solicitud: {response.status_code}')
        
# def getReferences(doi: str) -> None|int:
#     response = requests.get(f'http://api.crossref.org/works/{doi}')
#     if response.ok:
#         pass
#     else:
#         return None
        
def getArticles(issn: str, year_i: str, year_f: str) -> list[dict[str, str]]:
    """
    Obtiene todos los artículos publicados en una revista en un año determinado.

    Parameters:
        issn (str): El identificador de la revista que deseas buscar en la base de datos de Crossref.
        year_i (str): El año inicial de publicación de los artículos que se desean buscar.
        year_i (str): El año final de publicación de los artículos que se desean buscar.
        
    Returns:
        List[Dict[str, str]]: Una lista de diccionarios de artículos que contienen los siguientes campos:
        "DOI", "Título", "Autores", "Año", "Citas", "Revista".

    """
    articles = []
    cursor = '*'
    while cursor != '':
        params = {
            'filter': f'from-pub-date:{year_i}-01-01,until-pub-date:{year_f}-12-31',
            'rows': 1000,
            'cursor': cursor
        }
        response = requests.get(f'http://api.crossref.org/journals/{issn}/works', params=params)
        if response.ok:
            data = response.json()
            items = data.get('message', {}).get('items', [])
            for item in items:
                article = {
                    "DOI": item.get('DOI', ''),
                    "Título": formatData(item.get('title', ['n.m.'])[0]),
                    "Autores": formatData(' and '.join(author.get('given', 'n.m.') + ' ' + author.get('family', 'n.m.') for author in item.get('author', []))),
                    "Año": item.get('published-print', {}).get('date-parts', item.get('created', {}).get('date-parts',[['n.m.']]))[0][0],
                    "Citas": item.get('is-referenced-by-count', 0),
                    "Revista": item.get('container-title', ["n.m."])[0]
                }
                articles.append(article)
                # Llamamos a la función que extrae las referencias o citas del artículo
                # citas_jcr = getReferences(article.get('DOI', ''))
                # if citas_jcr != None:
                #     article["Citas"] = citas_jcr
                
            if data['message']['total-results'] - len(articles) == 0:
                cursor = ''
            else:
                cursor = data.get('message', {}).get('next-cursor', '')
        else:
            logger.error(f'Error al realizar la solicitud: {response.status_code}')
            cursor = ''
    return articles

def formatData(data: str) -> str:
    """
    Formatea y limpia una cadena de texto eliminando espacios en blanco innecesarios y etiquetas HTML.

    Args:
        data (str): La cadena de texto que se debe formatear y limpiar.

    Returns:
        str: La cadena de texto formateada y limpia, sin espacios en blanco innecesarios ni etiquetas HTML.
    """
    
    # Reemplazar las etiquetas HTML con una cadena vacía
    format_data = re.sub('<.*?>', '', data)
    # Eliminamos espacios en blanco y las retornos de línea
    format_data = re.sub('\s\s*', ' ', format_data.strip()).replace('\n', '').replace('\r', '')
    # Eliminamos las comas seguidas (campos vacíos)
    format_data = re.sub(',,', ',n.m.,', format_data.strip())
    
    return format_data

def loadData(csv_name: str) -> list:
    """
    Carga los datos de un archivo CSV que contiene información sobre revistas científicas
    y devuelve una lista de tuplas, donde cada tupla contiene el nombre del journal y su ISSN.

    Args:
        csv_name (str): El nombre del CSV que contiene la lista de revistas.

    Returns:
        list: Lista de tuplas que contiene el nombre del journal y su ISSN.
    
    """
    journal_list = []

    # Abrir el archivo CSV y leerlo
    with open(csv_name, encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        # Saltar las filas iniciales que no contienen información de revistas
        for i in range(3):
            next(reader)

        # Iterar sobre las filas restantes y extraer el nombre del journal y el ISSN
        for row in reader:
            if len(row) > 1:
                journal_list.append((row[0], row[3]))
    return journal_list

def plotBar(time_data: dict) -> None:
    """
    Crea una gráfica de barras a partir de un diccionario de tiempos de extracción de revistas.

    Args:
        time_data (dict): Un diccionario con los tiempos de extracción de cada revista.

    Returns:
        None: La función no retorna ningún valor.
    """
    if time_data != None and len(time_data) > 0:
        if any(val < 0 for val in time_data.values()):
            logger.error(f"No puede haber valores negativos en los tiempos de extraccion.")
        else:
            # Crear la gráfica de barras
            plt.bar(time_data.keys(), time_data.values(), width=1)

            # Personalizar la gráfica
            plt.title("Tiempo de estracción en función de la revista")
            plt.xlabel("ISSN de la revista")
            plt.ylabel("Tiempo (segundos)")
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.20)
            
            # Guardar la gráfica en un archivo de imagen
            plt.savefig('grafica_tiempos.png')
    else:
        logger.warning(f'No hay datos para graficar.')




def main(year_i:str, year_f:str, csv_name: str) -> int: 
    logger.info('\nNew CROSSREF execution:')
    
    # Gráficas de tiempo 
    time_data = {}
    
    # Especifica los parámetros de búsqueda de la API de Crossref
    for (journal,issn) in loadData(csv_name):
        
        # Comprobamos que la revista en cuestión existe
        if journalExist(issn, journal):

            # Comprobamos el tiempo que tarda -> INICIO
            initial_time = datetime.datetime.now()
            logger.info(f"[TIME] La hora de comienzo es: {initial_time.time()}")

            # Realizamos la búsqueda de los artículos (a partir de cualquiera de sus dos ISSN)
            data = getArticles(issn, year_i, year_f)
            
            # Transformamos los datos a CSV
            # NOTA: en un futuro irá directamente a la BBDD
            df = pd.DataFrame(data)
            df.to_csv('resultados/resultados_'+ issn +'.csv', index=False, encoding='utf-8')

            # Comprobamos el tiempo que tarda -> FIN
            final_time = datetime.datetime.now()
            logger.info(f"[TIME] La hora de finalización es: {final_time.time()}")
            logger.info(f"[TIME] El tiempo que ha tardado es: {final_time-initial_time}")
            time_data[issn] = int(final_time.timestamp()) - int(initial_time.timestamp())
            
    # Generamos la gráfica de tiempo
    plotBar(time_data)
    
   

if __name__ == '__main__':
    main("2000", "2023", r'JCR_JournalResults_01_2023_ComputerScience_AI.csv')
   
    












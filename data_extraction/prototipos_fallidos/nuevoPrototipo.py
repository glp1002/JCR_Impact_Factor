# Librería request: obtener un objeto respuesta (sin parser)
import requests
# Librería BeautifulSoup: parsear la página web
from bs4 import BeautifulSoup
# Módulo regex para poder trabajar con expresiones regulares
import re
# Librería para ell tratamiento de ficheros y directorios
import os
# Librería para extraer el DOI de Crossref
from habanero import Crossref
from habanero import counts
# Otras librerias
import csv
import random
import datetime
# Librería para programación concurrente
import concurrent.futures



# Creación del objeto BeautifulSoup
def htmlParsing(direccion):
    # Parseamos el HTML -> documentación: https://docs.python.org/3/library/html.parser.html
    soup = BeautifulSoup(direccion.content, 'html.parser')
    # Devolvemos el objeto con los datos sin procesar
    return soup

def listHeather():
    print("Obteniendo lista de headers...")
    url = 'https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/'
    # Extraemos de una lista gratuita varios agentes
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.content, 'html.parser')
    # Lista de posibles agentes
    user_agents = soup.find_all("a","code")
    
    if user_agents!= None:
        print("Lista terminada!")
    
    return user_agents
    
def getHeather(user_agents):
    # Selección de un agente al azar
    random_user_agent = random.choice(user_agents)
    headers = {'User-Agent': random_user_agent.text}
    # Se retorna la elección aleatoria del agente
    return headers




def get_article_info(elemento):

    article_info = []
    # Se busca la revista (aparecerá etiquetada en negrita)
    revista = elemento.find(class_='gs_a').find('b')
    # Compruebo que se trata de la revista que me interesa
    if(revista != None and revista.text.lower().strip() == 'chemical reviews'):
        # Consigo el título del artículo
        articulo = elemento.find('h3',class_='gs_rt').find('a')
            
        # Este "if" es imprescindible, ya que hay resultadoS intercalados que no hacen referencia a ningún artículo
        if(articulo != None): 

            # Consigo el año de publicación
            texto = elemento.find(class_='gs_a') # Extraigo el texto en el que aparece el año
            patron = ('[0-9]{4}') # Patrón de "año": 4 dígitos (del 0 al 9)
            anno = re.search(patron, texto.text) # Busco coincidencias
            fecha = anno.group(0) # Busco coincidencias con el patrón en el texto

            # Relleno la lista de resultados
            article_info.append(articulo.text)
            article_info.append(revista.text)
            article_info.append(fecha) 

            """OPCIONAL: IMPRIMIR POR PANTALLA"""
            # # Si la revista existe se añade junto al artículo
            # resultado = articulo.text + "," + revista.text + "," + ncitas + "," + fecha
            # # Imprimimos el resultado
            # print(resultado)

            # # SE EXTRAE EL ENLACE QUE REDIRECCIONA A LOS ARTICULOS "CITANTES"
            # citados = elemento.find(class_='gs_fl').find_all('a', href=True)[2]
            # print("URL de artículos citantes:", citados['href'])
            # print('\n')
       
    return article_info

def get_last_field(article_name):
    last_field = []
    # Conseguimos el DOI
    cr = Crossref()
    DOI = cr.works(query = article_name)
    DOI = DOI['message']['items'][0]['DOI']
    # Conseguimos el número de citas filtradas:
    # Contando el número de artículos "citantes" de tipo "journal-article"
    citantes = cr.works(filter={"doi": DOI})
    count = 0
    # for article in citantes['message']['items']:
    #     if article.get('type') == 'journal-article':
    #         count += 1
    # Añadimos los campos a la lista
    last_field.append(DOI)
    last_field.append(count)
    return last_field

def write_to_csv(article_info, last_field, csv_file):
    # Escribe la información del artículo y el último campo en el archivo CSV
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(article_info + last_field)



"""
PRIMERA BÚSQUEDA: Revista 'chemical reviews'
"""

    
def main():
    # Página de la que se extraerá información
    URL1 = 'https://scholar.google.com/scholar?start='
    URL2 = '&q=chemical+reviews&hl=es&as_sdt=0,5'
    
    # Lista de headers para las requests
    user_agents = listHeather()
    
    # Preparamos el CSV
    csv_file = 'con2nucleos.csv'
    header = ["Nombre del artículo","Nombre de la revista","Año de publicación","DOI","Número de citas"]
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    # Comprobamos el tiempo que tarda
    initial_time = datetime.datetime.now()
    print("La hora de inicio es: ", initial_time.time())

    # Lanzamos 2 hilos/núcleos
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Número de páginas de resultados sobre las que se quiere buscar 
        # Si se quiere buscar en 20 páginas, se deberá multiplicar por diez: 20*10=200
        for pagina in range(0, 200, 10):
            html = requests.get(URL1 + str(pagina) + URL2, headers=getHeather(user_agents))
            soup = BeautifulSoup(html.content, 'html.parser')    
            # Recogemos la información contenida en la sección de resultados
            elementos = soup.find_all('div', class_='gs_ri')
            # Realizamos la búsqueda de la revista en todos los resultados
            for elemento in elementos: 
                future1 = executor.submit(get_article_info, elemento)
                article_info = future1.result()
                if len(article_info) != 0:
                    future2 = executor.submit(get_last_field, article_info[0])
                    last_field = future2.result()
                    write_to_csv(article_info,last_field, csv_file)
                    
    # Comprobamos el tiempo que tarda
    final_time = datetime.datetime.now()
    print("La hora de finalización es: ", final_time.time())
    print("El tiempo que ha tardado es: ", final_time-initial_time)

if __name__ == '__main__':
    main()


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
# Otras librerias
import csv
import random
import datetime


# Creación del objeto BeautifulSoup
def htmlParsing(direccion):
    # Parseamos el HTML -> documentación: https://docs.python.org/3/library/html.parser.html
    soup = BeautifulSoup(direccion.content, 'html.parser')
    # Devolvemos el objeto con los datos sin procesar
    return soup
# def getHeather():
#     # Extraemos de una lista gratuita varios agentes
#     respuesta = requests.get('https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/')
#     soup = BeautifulSoup(respuesta.content, 'html.parser')
#     # Lista de posibles agentes
#     user_agents = soup.find_all("a","code")
#     # Selección de un agente al azar
#     random_user_agent = random.choice(user_agents)
#     headers = {'User-Agent': random_user_agent.text}
#     # Se retorna la elección aleatoria del agente
#     return headers
def listHeather():
    print("Obteniendo lista de headers...")
    url = 'https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/'
    # Extraemos de una lista gratuita varios agentes
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.content, 'html.parser')
    # Lista de posibles agentes
    user_agents = soup.find_all("a","code")
    
    if user_agents!= None:
        print("Lista obtenida!")
    
    return user_agents
    
def getHeather(user_agents):
    # Selección de un agente al azar
    random_user_agent = random.choice(user_agents)
    headers = {'User-Agent': random_user_agent.text}
    # Se retorna la elección aleatoria del agente
    return headers

# Creación del CSV
def iniFicheros():
    # Nombres del fichero
    filename1 = 'BBDD3.csv'    
    # En caso de ya existir y estar escrito,se borra para generar un nuevo CSV
    if(os.path.exists(filename1)and os.stat(filename1).st_size != 0):
        os.remove(filename1) 
    # Nombres del fichero
    filename2 = 'BBDD4.csv'    
    # En caso de ya existir y estar escrito,se borra para generar un nuevo CSV
    if(os.path.exists(filename2) and os.stat(filename2).st_size != 0):
        os.remove(filename2)
        
    # Escribimos la cabecera de cada campo
    with open('BBDD3.csv', 'a', newline = '', encoding='utf-8') as csvfile:
        my_writer = csv.writer(csvfile, delimiter = ',')
        my_writer.writerow(["Nombre del artículo","DOI","Nombre de la revista","Número de citas","Año de publicación","Id Artículo"])
    with open('BBDD4.csv', 'a', newline = '', encoding='utf-8') as csvfile:
        my_writer = csv.writer(csvfile, delimiter = ',')
        my_writer.writerow(["Nombre del artículo","DOI","Nombre de la revista","Número de citas","Año de publicación","Id Artículo"])
        
# Inicializamos los ficheros
iniFicheros()






"""
PRIMERA BÚSQUEDA: Revista 'chemical reviews'
"""

# Lista de headers para las requests
user_agents = listHeather()

# Página de la que se extraerá información
URL1 = 'https://scholar.google.com/scholar?start='
URL2 = '&q=chemical+reviews&hl=es&as_sdt=0,5'

# Lista de resultados
lista = []
# Inicializamos el índice de resultados
indice = 0

# Comprobamos el tiempo que tarda
initial_time = datetime.datetime.now()
print("La hora de inicio es: ", initial_time.time())


# Número de páginas de resultados sobre las que se quiere buscar 
# Si se quiere buscar en 20 páginas, se deberá multiplicar por diez: 20*10=200
for pagina in range(0, 200, 10):
    
    html = requests.get(URL1 + str(pagina) + URL2, headers=getHeather(user_agents))
    soup = BeautifulSoup(html.content, 'html.parser')
            
    # Recogemos la información contenida en la sección de resultados
    elementos = soup.find_all('div', class_='gs_ri')

    # Realizamos la búsqueda de la revista en todos los resultados
    for elemento in elementos: 
        # Se busca la revista (aparecerá etiquetada en negrita)
        revista = elemento.find(class_='gs_a').find('b')
        # Compruebo que se trata de la revista que me interesa
        if(revista != None and revista.text.lower().strip() == 'chemical reviews'):
            # Consigo el título del artículo
            articulo = elemento.find('h3',class_='gs_rt').find('a')
            
            # Este "if" es imprescindible, ya que hay resultadoS intercalados que no hacen referencia a ningún artículo
            if(articulo != None): 
                
                # Conseguimos el DOI
                cr = Crossref()
                DOI = cr.works(query = articulo.text)
                DOI = DOI['message']['items'][0]['DOI']
                                        
                # Consigo el número de citas
                texto = elemento.find(class_='gs_fl').find_all('a')[2]
                patron = ('[0-9]+')
                cita = re.search(patron, texto.text)
                ncitas = cita.group(0)

                # Consigo el año de publicación
                texto = elemento.find(class_='gs_a') # Extraigo el texto en el que aparece el año
                patron = ('[0-9]{4}') # Patrón de "año": 4 dígitos (del 0 al 9)
                anno = re.search(patron, texto.text) # Busco coincidencias
                fecha = anno.group(0) # Busco coincidencias con el patrón en el texto

                # Actualizo el índice
                indice += 1

                # Relleno la lista de resultados
                tupla = (articulo.text,DOI,revista.text,ncitas,fecha,indice)
                lista.append(tupla)

                # # Si la revista existe se añade junto al artículo
                # resultado = articulo.text + "," + DOI + "," + revista.text + "," + ncitas + "," + fecha + "," + str(indice)
                # # Imprimimos el resultad
                # print(resultado)

                # # SE EXTRAE EL ENLACE QUE REDIRECCIONA A LOS ARTICULOS "CITANTES"
                # citados = elemento.find(class_='gs_fl').find_all('a', href=True)[2]
                # print("URL de artículos citantes:", citados['href'])
                # print('\n')
            
# Escribimos los resultados en un CSV
with open('BBDD3.csv', 'a', newline = '', encoding='utf-8') as csvfile:
    my_writer = csv.writer(csvfile, delimiter = ',')
    for elemento in lista:
        my_writer.writerow(elemento)    

# Comprobamos el tiempo que tarda
final_time = datetime.datetime.now()
print("La hora de finalización es: ", final_time.time())
print("El tiempo que ha tardado es: ", final_time-initial_time)    
# Espacio para la siguiemte búsqueda
print('\n\n')






"""
SEGUNDA BÚSQUEDA: Revista 'the lancet'
"""

# Página de la que se extraerá información
URL1 = 'https://scholar.google.com/scholar?start='
URL2 = '&q=the+lancet&hl=es&as_sdt=0,5'

# Lista de resultados
lista2 = []
# Inicializamos el índice de resultados
indice = 0

# Número de páginas de resultados sobre las que se quiere buscar 
# Si se quiere buscar en 20 páginas, se deberá multiplicar por diez: 20*10=200
for pagina in range(0, 200, 10):
    
    html = requests.get(URL1 + str(pagina) + URL2, headers=getHeather(user_agents))
    soup = BeautifulSoup(html.content, 'html.parser')


    # Recogemos la información contenida en la sección de resultados
    elementos = soup.find_all('div', class_='gs_ri')

    # Realizamos la búsqueda de la revista en todos los resultados
    for elemento in elementos: 
        # Se busca la revista (aparecerá etiquetada en negrita
        revista = elemento.find(class_='gs_a').find('b')
        # Compruebo que se trata de la revista que me interesa
        if(revista != None and revista.text.lower().strip() == 'the lancet'):
            # Consigo el título del artículo
            articulo = elemento.find(class_='gs_rt').find('a')

            if(articulo != None):
                # Conseguimos el DOI
                cr = Crossref()
                DOI = cr.works(query = articulo.text)
                DOI = DOI['message']['items'][0]['DOI']
                
                # Consigo el número de citas
                texto = elemento.find(class_='gs_fl').find_all('a')[2]
                patron = ('[0-9]+')
                cita = re.search(patron, texto.text)
                ncitas = cita.group(0)

                # Consigo el año de publicación
                texto = elemento.find(class_='gs_a') # Extraigo el texto en el que aparece el año
                patron = ('[0-9]{4}') # Patrón de "año": 4 dígitos (del 0 al 9)
                anno = re.search(patron, texto.text) # Busco coincidencias
                fecha = anno.group(0) # Busco coincidencias con el patrón en el texto

                # Actualizo el índice
                indice += 1

                # Relleno la lista de resultados
                tupla = (articulo.text,DOI,revista.text,ncitas,fecha,indice)
                lista2.append(tupla)

                # Si la revista existe se añade junto al artículo
                resultado = articulo.text + "," + DOI + "," + revista.text + "," + ncitas + "," + fecha + "," + str(indice)
                # Imprimimos el resultado
                print(resultado)
                
                # SE EXTRAE EL ENLACE QUE REDIRECCIONA A LOS ARTICULOS "CITANTES"
                citados = elemento.find(class_='gs_fl').find_all('a', href=True)[2]
                print("URL de artículos citantes:", citados['href'])
                print('\n')
        
# Escribimos los resultados en un CSV        
with open('BBDD4.csv', 'a', newline = '', encoding='utf-8') as csvfile:
    my_writer = csv.writer(csvfile, delimiter = ',')
    for elemento in lista2:
        my_writer.writerow(elemento)

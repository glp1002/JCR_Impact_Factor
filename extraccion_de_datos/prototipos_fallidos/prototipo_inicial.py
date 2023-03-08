"""
PROTOTIPO WEB SCRAPPING TO GOOGLE SCHOOLAR
Versión 1.0
"""

######################################################################################

"""
IMPORTS
"""

# Librería request: obtener un objeto respuesta (sin parser)
import requests

# Librería BeautifulSoup: parsear la página web
# Documentación: https://beautiful-soup-4.readthedocs.io/en/latest/
from bs4 import BeautifulSoup

# Librería para ell tratamiento de ficheros y directorios
import os

# Otros
from datetime import datetime
import csv
import random


 
######################################################################################

"""
HTTP Requests
"""

# Método que selecciona un "user agent" al azar
# Código sacado de: https://www.shellhacks.com/python-requests-user-agent-web-scraping/
def getHeather():
    
    # Extraemos de una lista gratuita varios agentes
    respuesta = requests.get('https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/')
    soup = BeautifulSoup(respuesta.content, 'html.parser')
    
    # Lista de posibles agentes
    user_agents = soup.find_all("a","code")

    # Selección de un agente al azar
    random_user_agent = random.choice(user_agents)
    headers = {'User-Agent': random_user_agent.text}
    
    # Se retorna la elección aleatoria del agente
    return headers
    
    
# Método para establecer un proxy (enmascaramos así nuestra ip)
def getProxy():

    # Extraemos de una lista gratuita varios proxies
    respuesta = requests.get('https://www.proxy-list.download/HTTP')
    soup = htmlParsing(respuesta)
    
    # Extraemos un proxy https
    resp = soup.find("td")
    ip = resp.next
    port = resp.next.next.next.next
    proxy = ip.strip() + ':' + port.strip()

    # Lista de posible user agents
    proxies = {'http': proxy} 

    return proxies 


# Ejecución del método HTTP GET
# Se pasa por parámetro la página web deseada y los datos de la búsqueda
def requestGet(direccion, parametros):
    
    #TO DO:
    pagina = requests.get(direccion, params=parametros, headers=getHeather(), proxies=getProxy() )
    return pagina


# Status code (el código de éxito es '200')
# Comprobamos que se busca la URL de forma adecuada
def checkSuccess(indice, direccion):
    
    if(direccion.status_code == 200):
        msg = "Llamada " + str(indice) + " a " + direccion.url + " exitosa."
        # Imprimimos el resultado
        print(msg)
        exiTxt(msg)
        return True
    
    else:
        msg = "Llamada " + str(indice) + " a " + direccion.url + " fallida."
        # Imprimimos el resultado
        print(msg)
        errTxt(msg)
        return False


# Impresión del contenido de la página copleta
def printContent(direccion):
    print(direccion.content)
    

######################################################################################
    
"""
Objeto BeautifulSoup
"""
# Método que realiza web scrapping
# def webScrapping(nuevaUlr):
    # Parseamos el HTML
    # soup = htmlParsing(url)
    # Obtenemos su título
    # getTittle(soup)

# Creación del objeto BeautifulSoup
def htmlParsing(direccion):
    # Parseamos el HTML -> documentación: https://docs.python.org/3/library/html.parser.html
    soup = BeautifulSoup(direccion.content, 'html.parser')
    # Devolvemos el objeto con los datos sin procesar
    return soup

# Procesamiento de los datos e impresión de los mismos
def printSoup():
    # Limpiamos los datos sin procesar y se imprime la estructura anidada de HTML en la "soup".
    print(soup.prettify())
    

# Obtener el título y sus datos
# Nombre del tag ("title") + Título
def getTittle(soup):
    titulo = str(soup.title.name) + ": " + str(soup.title.text)
    return titulo


######################################################################################

"""
Entrada y salida de datos
"""

# Método que inicializa los ficheros de resultados
def iniFicheros():
    
    # Nombres de los ficheros
    filename1 = 'exitos.txt'
    filename2 = 'errores.txt'
    filename3 = 'datos.csv'
    
    # En caso de ya existir y estar escritos, se borran para generar los nuevos sin problemas
    if(os.path.exists(filename1) and os.stat(filename1).st_size != 0):
        os.remove(filename1)
        
    if(os.path.exists(filename2) and os.stat(filename2).st_size != 0):
        os.remove(filename2)
        
    if(os.path.exists(filename3) and os.stat(filename3).st_size != 0):
        os.remove(filename3)


# Parámetros de los resultados exitosos de la búsqueda almacenados en un CSV
# TO DO: incluir el resto de parámetros que interesan, no solo el título
def lineCsv(soup, indice):
    
    # Se almacena el título
    titulo = getTittle(soup)
    
    # Se abre el fichero CSV en el que se escribirá
    filename = 'datos.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        linea = [indice,titulo]
        w.writerow(linea)
    
    # Se cierra el fichero para evitar posibles errores
    f.close()

    
# Txt de solicitudes exitosas
def exiTxt(msg):
    
    # Se abre el fichero txt en el que se escribirá
    filename = 'exitos.txt'

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        f.write(msg)
        f.write('\n')
    
    # Se cierra el fichero para evitar posibles errores
    f.close()
    
# Txt de solicitudes fallidas
def errTxt(msg):
    
    # Se abre el fichero txt en el que se escribirá
    filename = 'errores.txt'

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        f.write(msg)
        f.write('\n')
        
    # Se cierra el fichero para evitar posibles errores
    f.close()

    
    
# Se pide el término de búsqueda y se guarda en forma de diccionario
# TO DO: incrementar el número de parámetros posibles (autor, citas...)
def searchParameters():  
    
    # Entrada de palabras claves (puede haber más de una palabra)
    busquedaS = ''
    busqueda = input("Introduce el término de búsqueda: ").split()
    indice = 1
    for b in busqueda:
        busquedaS += b
        if indice < len(busqueda):
            busquedaS += '+'
        indice += 1

    # Entrada del idioma
    idioma = input("Introduce el idioma de la búsqueda: ")
    
    # Separación de la entrada y la salida
    print('\n') 
    
    # Diccionario de datos
    data = {'q': busquedaS,'hl': idioma, 'as_sdt': '0,5'}
    return data
    
######################################################################################

"""
Tiempo
"""

def getTiempo():
    lista = (datetime.today().strftime('%a,%b,%d,%Y,%H:%M:%S')).split(',')
    tiempo = lista[0] + ',+' + lista[2] + '-' + lista[1] + '-' + '2023' + '+' + lista[4] + '+GMT'
    return tiempo

######################################################################################
    
"""
Método principal
"""

def main():
    
    # Dirección de Google Scholar, sitio que se desea inspeccionar
    direccionS = 'https://scholar.google.com/scholar'
    
    # Se pide el término de búsqueda y se guarda en forma de diccionario
    data = searchParameters()
    
    # Se solicita la web de búsqueda
    direccionB = requestGet(direccionS, data)
        
    # Preparamos los ficheros donde se guardarán los resultados
    iniFicheros()

    # Hacemos 1000 solicitudes a la página
    for indice in range(1000):
        
        # Se comprueba que la web es accesible antes de realizar la búsqueda
        if(checkSuccess(indice + 1, direccionB)):
            # Parseamos la dirección de búsqueda
            soup = htmlParsing(direccionB)
            # Imprimimos los datos en una linea del CSV de resultados
            lineCsv(soup, indice + 1)
   
        # Si la IP ha sido baneada, se trata de evitar el error
        #else:
            # Url que suprime el error
            #direccionErr = 'https://scholar.google.com/scholar?q=' + data['q'] + '&hl=' + data['hl'] + '&as_sdt=0%2C5&google_abuse=GOOGLE_ABUSE_EXEMPTION%3DID%3D0bb1123c8648d592:TM%3D1665669239:C%3Dr:IP%3D193.146.172.152-:S%3DpYb4eD9wyC67xaXFFgTCaFs%3B+path%3D/%3B+domain%3Dgoogle.com%3B+expires%3D' + getTiempo()
            # Solicitamos la nueva web
            #direccionB = requests.get(direccionErr)
            
        # Separación entre solicitudes        
        print('\n') 
          

if __name__=="__main__":
    main()


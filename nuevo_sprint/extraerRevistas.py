# Librería request: obtener un objeto respuesta (sin parser)
import requests
# Librería BeautifulSoup: parsear la página web
from bs4 import BeautifulSoup


"""
PRIMERA BÚSQUEDA: Revista Educación
"""
html = requests.get('https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q=robotica+revista+Educacion&btnG=')
soup = BeautifulSoup(html.content, 'lxml')

elementos = soup.find_all('div', class_='gs_a')

for elemento in elementos:
    revista = elemento.find('b')
    # Compruebo que se trata de la revista que me interesa
    if(revista != None and revista.text.lower().strip() == 'revista educación'):
        # Consigo el título del artículo
        articulo = elemento.previous_sibling
        # Si la revista existe se añade junto al artículo
        lista = {articulo.text : revista.text}
        print(lista)

print('\n')



"""
SEGUNDA BÚSQUEDA: Revista Emergencias
"""
html = requests.get('https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q=Revista+Emergencias&btnG=&oq=revista')
soup = BeautifulSoup(html.content, 'lxml')

elementos = soup.find_all('div', class_='gs_a')

for elemento in elementos:
    revista = elemento.find('b')
    # Compruebo que se trata de la revista que me interesa
    if(revista != None and revista.text.lower().strip() == 'emergencias'):
        # Consigo el título del artículo
        articulo = elemento.previous_sibling
        # Si la revista existe se añade junto al artículo
        lista = {articulo.text : revista.text}
        print(lista)

print('\n')
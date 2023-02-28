from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import pandas as pd
import datetime
import random
import time
import re

MAX_SCHOLAR_REQUESTS = 5

# Detalles de la búsqueda
revista = "Algorithms" # Input...
anno_i = "2019"
anno_f = "2020"
resultados = [] # Output...


# Configurar el proxy
myProxy = "154.113.121.60:80"
proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy
       })

# Opción sin gáficos (comentar estas dos líneas de código para verlo gráficamente) -> ver reCAPTCHA
options = FirefoxOptions()
options.add_argument("--headless")

# Prepareciones de Selenium
driver = webdriver.Firefox(options=options, proxy=proxy)
driver.get('https://scholar.google.com/scholar?as_q=&as_publication=' + revista + '&as_ylo=' + anno_i + '&as_yhi=' + anno_f)

# Preparaciones de bs4
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
                            
# Número de resultados encontrados -> class="gs_ab_mdw"
num_res = soup.find_all(class_='gs_ab_mdw')[1] # Obtenemos la etiqueta
num_res = re.findall('\d{1,3}(?:\.\d{3})*', num_res.text)[0] # Obtenemos el número 
print("Se van a extraer 1000 de los " + num_res + " resultados encontrados de la revista " + revista + ".")

# Comprobamos el tiempo que tarda
initial_time = datetime.datetime.now()
print("La hora de inicio es: ", initial_time.time())


indice = 1
flag = True

# Navegación por la página de resultados
while flag:

        # Extracción de la cita de cada artículo
        cite_buttons = driver.find_elements(By.XPATH,"//div[@class='gs_r gs_or gs_scl']//div[@class='gs_ri']//div[@class='gs_fl']//a[@class='gs_or_cit gs_or_btn gs_nph']")
        if len(cite_buttons) != 0:
            for cite_button in cite_buttons:
                
                # Google Scholar solo acepta 20 llamadas
                if indice % 20 == 0:
                    print("[Espera temporal] saturación de requests")
                    time.sleep(random.randint(30,40))
                
                # Entramos en el apartado "citas" y esperamos a que cargue
                driver.execute_script("arguments[0].click();", cite_button)
                time.sleep(2)
                # Preparaciones de bs4
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                # Extracción de la cita
                if len(soup.find_all('div', class_='gs_citr')) != 0:
                    cita_mla = soup.find_all('div', class_='gs_citr')[2]
                    resultados.append(cita_mla.text)
                    indice = indice + 1
                else:
                    print(f"[Error] No se encontró una cita en el formato esperado para el artículo {indice}")
                    time.sleep(40)
                    break
                
                # Salimos del apartado de citas
                exit_button = driver.find_element(By.ID,'gs_cit-x')
                driver.execute_script("arguments[0].click();", exit_button)
             
            # Espera de 3 a 10 segundos (aleatoriamente) para "humanizar" la búsqueda
            time.sleep(random.randint(3,10))   
                
            # hacer clic en el botón "Next" para pasar a la siguiente página
            if driver.find_elements(By.TAG_NAME,'a')[-13] != None:
                next_button = driver.find_elements(By.TAG_NAME,'a')[-13]
                driver.execute_script("arguments[0].click();", next_button)
            else:
                print(f"[Fin] No hay más botones 'next'")
                flag = False
        else:
            print("[Error] Ha saltado un CAPTCHA")
            time.sleep(30)
            # Click en el "chackbox" automatizado
            WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='reCAPTCHA']")))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
            # Resolver las imágenes a mano...
            print("[reCAPTCHA] Resolver el CAPTCHA de imágenes manualmente (activar modo gráfico).")
            time.sleep(2)

  

        # Espera de 3 a 10 segundos (aleatoriamente) para "humanizar" la búsqueda
        time.sleep(random.randint(3,10))
# Salida del navegador
driver.quit()


# Comprobamos el tiempo que tarda
final_time = datetime.datetime.now()
print("La hora de finalización es: ", final_time.time())
print("El tiempo que ha tardado es: ", final_time-initial_time)


# TODO: numero de citas -> bs4
initial_time = datetime.datetime.now()
print("La hora de comienzo de limpieza de datos es: ", initial_time.time())

# Expresión regular para extraer los campos
patrones = {'authors':'.*(?=. ")',
            'tittle':'(?<=").*?(?=.")',
            'journal':'(?<=." ).*?(?= [0-9]+\.[0-9]+)',
            'year':'(?<=\()[0-9]*?(?=\))'
            }

# Almacenamiento de datos
data = []
num_fallos = 0
num_aciertos = 0

for cita in resultados:
    
    # Revista
    journal = re.search(patrones['journal'], cita)
    if journal == None:
        # Si no se encuentra el valor
        # Inicializar los valores de los campos a "n.d." por defecto
        journal = 'n.d.'
    else:
        # Si el valor se encuentra, se añade
        journal = journal.group(0)
        
           
    # Comprobar si el publisher está en la revista
    if revista in journal.lower():
        num_aciertos = num_aciertos + 1
        
        # Autor
        author = re.search(patrones['authors'], cita)
        if author == None:
            author = 'n.d.'
        else:
            author = author.group(0)
            
        # Título
        tittle = re.search(patrones['tittle'], cita)
        if tittle == None:
            tittle = 'n.d.'
        else:
            tittle = tittle.group(0)
            
        # Año
        year = re.search(patrones['year'], cita)
        if year == None:
            year = 'n.d.'
        else:
            year = year.group(0)

        data.append(
                {
                'index': num_aciertos,
                'author':author,
                'tittle':tittle,
                'journal':journal,
                'year':year,
                'publisher': revista 
                }
            )
    else:
        num_fallos = num_fallos + 1
        

df = pd.DataFrame(data)
df.to_csv('resultados.csv',index=False, encoding='utf-8')


# Comprobamos el tiempo que tarda
final_time = datetime.datetime.now()
print("La hora de finalización es: ", final_time.time())
print("El tiempo que ha tardado es: ", final_time-initial_time)


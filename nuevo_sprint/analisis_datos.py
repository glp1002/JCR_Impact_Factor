import re
import pandas as pd

revista = 'ieee'

citacion3 = 'Molisch, Andreas F., et al. "IEEE 802.15. 4a channel model-final report." IEEE P802 15.04 (2004): 0662.'
citation2 = 'Zheng, Jianliang, and Myung J. Lee. "A comprehensive performance study of IEEE 802.15. 4." Sensor network operations 4 (2006): 218-237.'
citation = 'Khorov, Evgeny, et al. "A tutorial on IEEE 802.11 ax high efficiency WLANs." IEEE Communications Surveys & Tutorials 21.1 (2018): 197-216.'
citas = [citation, citation2,citacion3]

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

for cita in citas:
    
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

        


    

  

"""
Módulo de extracción de las URLs de las revistas de la API de Crossref.
Se añadirán dichas URLs a los CSV de resultados ya extraidos.

============================
  Trabajo de Fin de Grado
Universidad de Burgos (UBU)
============================

Autor: Gadea Lucas Pérez
Año: 2023
"""

import csv
import json
import requests
import pandas as pd

from crossref_prototipo import loadData

def extract_journal_urls(journal_list):
    base_url = 'https://api.crossref.org/journals/'
    urls = []

    for (journal,issn) in journal_list:
        journal_url = base_url + issn
        response = requests.get(journal_url)

        if response.status_code == 200:
            data = json.loads(response.text)

            if 'message' in data and 'URL' in data['message']:
                url = data['message']['URL']
                urls.append(url)
                print(f'Revista {journal}: {url}')
            else:
                urls.append(None)
        else:
            urls.append(None)

    return urls

def main(csv_name: str) -> int:
    journals = loadData(csv_name)


    journal_urls = extract_journal_urls(journals)

    for i, url in enumerate(journal_urls):
        print(f'Revista {journals[i]}: {url}')

              

if __name__ == '__main__':
    main( r'JCR_AI_2021.csv')
   
    
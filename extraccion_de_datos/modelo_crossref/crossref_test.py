"""
Módulo de pruebas para el modelo de extracción de datos de Crossref.

============================
  Trabajo de Fin de Grado
Universidad de Burgos (UBU)
============================

Autor: Gadea Lucas Pérez
Año: 2023
"""

import csv
import os
import tempfile
import unittest

import crossref_prototipo as cr

class TestCrossref(unittest.TestCase):
    
    def test_journal_exist(self):
        # Caso de prueba 1: revista existe
        self.assertTrue(cr.journalExist('2168-2267','IEEE Transactions on Big Data'))
        
        # Caso de prueba 2: revista no existe
        self.assertFalse(cr.journalExist('12345-12345','Nonexistent Journal'))
        
    def test_load_data(self):
        # Caso de prueba 3: Comprobar que se cargan bien los datos
        # Crear un archivo CSV temporal con un registro de prueba
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            writer = csv.writer(f)
            writer.writerows([] for i in range(3))
            writer.writerow(["CONNECTION SCIENCE","CONNECT SCI","0954-0091","1360-0494","COMPUTER SCIENCE, ARTIFICIAL INTELLIGENCE - SCIE","921","N/A","N/A","0.7","29.37%"])
        # Llamar a la función loadData() y comprobar que devuelve los datos correctos
        data = cr.loadData(f.name)
        self.assertEqual(data, [('CONNECTION SCIENCE', '0954-0091')])
        # Eliminar el archivo CSV temporal
        os.remove(f.name)
        
    def test_formatData(self):
        # Caso de prueba 4: Comprobar que se eliminan bien las etiquetas HTML y los espacios
        input_data = "<p>This is a  text with <em>html</em> tags and  extra spaces.  </p>"
        expected_output = "This is a text with html tags and extra spaces."
        self.assertEqual(cr.formatData(input_data), expected_output)
        
        # Caso de prueba 5: Comprobar que se eliminan bien las etiquetas "href"
        input_data = "<p> <em> This is a </em> another text with extra  spaces and <a href='https://www.example.com'>links</a>. </p>"
        expected_output = "This is a another text with extra spaces and links."
        self.assertEqual(cr.formatData(input_data), expected_output)
        
        # Caso de prueba 6: Comprobar que los "strings" que no han de cambiar, no cambian      
        input_data = "This is a text with no HTML tags or extra spaces."
        expected_output = "This is a text with no HTML tags or extra spaces."
        self.assertEqual(cr.formatData(input_data), expected_output)
        
        # Caso de prueba 7: Comprobar que no hay campos vacíos (rellenar con n.m.)  
        input_data = "This is a text with,, some void ,, fields."
        expected_output = "This is a text with,n.m., some void ,n.m., fields."
        self.assertEqual(cr.formatData(input_data), expected_output) 
        
    def test_getArticles_returns_list_of_dicts(self):
        # Caso de prueba 8: Devuelve una lista de artículos
        articles = cr.getArticles('1533-7146', '2020', '2021')
        self.assertIsInstance(articles, list)
        for article in articles: 
            self.assertIsInstance(article, dict)
            
    def test_getArticles_returns_valid_keys(self):
        # Caso de prueba 9: Las "keys" o claves del diccionario son correctas
        articles = cr.getArticles('1533-7146', '2020', '2021')
        expected_keys = ["DOI", "Título", "Autores", "Año", "Citas", "Revista"]
        for article in articles:
            self.assertEqual(list(article.keys()), expected_keys)
            
    def test_getArticles_correct_article_count(self):
        # Caso de prueba 10: Devuelve el número correcto de artículos
        articles = cr.getArticles('1533-7146', '2020', '2021')
        self.assertEqual(len(articles), 86)
        
    def test_getArticles_invalid_issn_raises_error(self):
        # Caso de prueba 11: ISSN inválido
        articles = cr.getArticles('invalid_issn', '2020', '2021')
        self.assertEqual(len(articles), 0)
        self.assertEqual(articles, [])  
              
    def test_getArticles_invalid_year(self):
        # Caso de prueba 12: Año incorrecto -> orden incorrecto
        articles = cr.getArticles('1533-7146', '2023', '2022')
        self.assertEqual(len(articles), 0)
        self.assertEqual(articles, [])  
        
        # Caso de prueba 13: Año incorrecto -> años inválidos
        articles = cr.getArticles('1533-7146', '2016', '99999')
        self.assertEqual(len(articles), 0)
        self.assertEqual(articles, [])  
        
    def test_main(self):
        # Ejecución completa del prototipo -> requisito: CSV de entrada de datos
        cr.main("2000", "2023", r'JCR_AI_2021.csv')
   
        # Caso de prueba 14: Se genera una gráfica al finalizar el proceso
        self.assertTrue(os.path.isfile('./resultados2/grafica_tiempos.png'))

        # Caso de prueba 15: Se generan ficheros CSVs de resultados 
        self.assertTrue(os.path.isfile('./resultados2/resultados_2375-4699.csv'))
        self.assertTrue(os.path.isfile('./resultados2/resultados_2168-2291.csv'))
    
        # Caso de prueba 16: Se genera un fichero de log
        self.assertTrue(os.path.isfile('./resultados2/crossref.log'))
        
        # Caso de prueba 17: La información de log es correcta
        log_file = open("./resultados2/crossref.log", "r")
        log_contents = log_file.read()
        self.assertIn('New CROSSREF execution:', log_contents)
        self.assertIn('- ERROR - Error para "JOURNAL OF MULTIPLE-VALUED LOGIC AND SOFT COMPUTING" al realizar la solicitud: 404', log_contents)
        self.assertIn('- INFO - Extraccion de la revista Information Technology and Control', log_contents)
        
        
if __name__ == '__main__':
    unittest.main()

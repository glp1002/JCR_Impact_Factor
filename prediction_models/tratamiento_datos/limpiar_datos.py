import csv

# Especifica el separador actual y el nuevo separador
separador_actual = ','
nuevo_separador = '|'

# Rutas de los archivos CSV (entrada y salida)
archivo_entrada = './datos_combinados.csv'
archivo_salida = './datos_combinados2.csv'

# Abre el archivo de entrada y crea un archivo de salida con el nuevo separador
with open(archivo_entrada, 'r', encoding='utf8') as f_in, open(archivo_salida, 'w', newline='') as f_out:
    # Crea el objeto lector CSV
    lector_csv = csv.reader(f_in, delimiter=separador_actual)
    
    # Crea el objeto escritor CSV con el nuevo separador
    escritor_csv = csv.writer(f_out, delimiter=nuevo_separador)
    
    # Lee y escribe cada línea del archivo CSV
    for linea in lector_csv:
        escritor_csv.writerow(linea)

import csv

citas_file = 'citas.csv'
jcr_file = 'jcr_esperado.csv'
diferencias_file = 'diferencias.csv'
output_file = 'datos_combinados.csv'

# Leer los datos de los archivos CSV
citas_data = {}
with open(citas_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        revista = row['Revista']
        del row['Revista']
        row = {k.strip().replace('Citas ', ''): v for k, v in row.items()}  # Eliminar "Citas" del nombre de columna
        citas_data[revista] = row

jcr_data = {}
with open(jcr_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        revista = row['Revista']
        del row['Revista']
        row = {k.strip().replace('JCR ', ''): v for k, v in row.items()}  # Eliminar "JCR" del nombre de columna
        jcr_data[revista] = row

diferencias_data = {}
with open(diferencias_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        revista = row['Revista']
        del row['Revista']
        row = {k.strip().replace('JCR ', ''): v for k, v in row.items()}  # Eliminar "Diff" del nombre de columna
        diferencias_data[revista] = row

# Combinar los datos en una lista de diccionarios
combined_data = []
for revista in jcr_data:
    for anio in jcr_data[revista]:
            data = {
                'Anio': anio,
                'Revista': revista,
                'Citas': citas_data[revista][anio],
                'JCR': jcr_data[revista][anio],
                'Diff': diferencias_data[revista][anio]
            }
            combined_data.append(data)

# Escribir los datos combinados en un nuevo archivo CSV
fieldnames = ['Anio', 'Revista', 'Citas', 'JCR', 'Diff']
with open(output_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(combined_data)

print("Los datos combinados se han guardado en", output_file)

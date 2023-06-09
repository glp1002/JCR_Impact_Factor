import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
data = pd.read_csv('./resultados.csv', header=0, encoding='utf-8')

# Crear un diccionario para almacenar las estimaciones de cada modelo
model_estimations = {}

# Iterar sobre los datos y agregar las estimaciones a cada modelo
for _, row in data.iterrows():
    modelo = row['Modelo']
    rmse = row['RMSE']
    
    if modelo in model_estimations:
        model_estimations[modelo].append(rmse)
    else:
        model_estimations[modelo] = [rmse]

# Crear una lista de nombres de modelos y una lista de sus estimaciones
model_names = list(model_estimations.keys())
estimations = list(model_estimations.values())

# Crear una lista de datos para el gráfico de cajas
data_to_plot = []
for estimations_list in estimations:
    data_to_plot.append(estimations_list)

# Crear el gráfico de cajas con los ejes invertidos
plt.figure(figsize=(10, 6))
plt.boxplot(data_to_plot, labels=model_names, vert=True)
plt.xlabel('RMSE')
plt.ylabel('Modelos')
plt.title('Comparación de los modelos')
plt.show()
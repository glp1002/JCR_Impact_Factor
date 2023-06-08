import pickle

# Cargar el modelo desde el archivo pickle
with open('modelo_AdaBoost.pickle', 'rb') as archivo:
    resultados = pickle.load(archivo)

# Obtener la lista de modelos y resultados de la iteración
modelos_iteracion = resultados['modelos']
resultados_iteracion = resultados['resultados']

# Encontrar el índice del modelo con el menor valor de RMSE
indice_mejor_modelo = resultados_iteracion.index(min(resultados_iteracion))
# Seleccionar el modelo con mejores resultados
mejor_modelo = modelos_iteracion[indice_mejor_modelo]

# Hacer una predicción con el modelo seleccionado
ejemplo = [[17.87, 18.012, 17.994, 7.743, 9362.0, 9788.0, 17.87, 18.012, 17.994, 7.743, 9362.0, 9788.0, 8]]
predicciones = mejor_modelo.predict(ejemplo)
print(predicciones)


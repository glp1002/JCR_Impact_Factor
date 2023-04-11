import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, KFold, RepeatedKFold, cross_val_score, train_test_split

# Lectura de datos
try:
    df_jcr = pd.read_csv("jcr_esperado.csv")
    df_citas = pd.read_csv("citas.csv")
    df_diferencias = pd.read_csv("diferencias.csv")
except FileNotFoundError:
    print("Error: no se pudo cargar uno o más archivos de datos.")
    exit()

# seleccionar columnas de 2018 a 2022 junto con la columna de Revista
anio_i = 2018
anio_f = 2022
df_jcr1 = df_jcr.loc[:, ['Revista'] + [f'JCR {anio}' for anio in range(anio_i,anio_f+1,1)]]
df_citas1 = df_citas.loc[:, ['Revista'] + [f'Citas {anio}' for anio in range(anio_i,anio_f+1,1)]]
df_diferencias1 = df_diferencias.loc[:, ['Revista'] + [f'Diff {anio}' for anio in range(anio_i,anio_f+1,1)]]

# Unión de los datos en función de la revista
df = pd.merge(df_jcr1, df_citas1, on="Revista")
df = pd.merge(df, df_diferencias1, on="Revista")

# Definición de variables
x = df.drop(columns=["Revista", f"Diff {anio_f-1}", f"JCR {anio_f-1}"])
x = x.fillna(x.mean()).values
y = df[f"JCR {anio_f-1}"]
y = y.fillna(y.mean()).values

# Separar los datos en conjunto de entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


# Definir los modelos de regresión y sus parámetros
models = [  
        ("Random Forest", RandomForestRegressor(), 
            { # Parámetros a seleccionar
            "n_estimators": [50, 100, 150, 200, 300, 400, 500], # Nº de árboles -> 200 - 500
            "max_depth": [10, 20, 30, 40, 50, 60, 70] # Profundidad
            }
        )
        # Meter el resto de modelos AQUÍ ...     
                #    ("MLP", MLPRegressor(), {"hidden_layer_sizes": [(50,), (100,)], # Capas ocultas
        #                              "activation": ["tanh", "relu"] # Funciones de activación
        #                             })
        #    ("GB", GradientBoostingRegressor(), {"n_estimators": [10, 50], # Nº de estimadores
        #                                         "learning_rate": [0.1, 0.5] # Learning rate
        #                                         })
        #    ("SVR", SVR(), { "kernel": ['rbf', 'poly', 'sigmoid'], 
        #                     "C": [150, 100, 50],
        #                     "gamma": ['scale', 'auto'],
        #                     "epsilon": [0.1, 0.2],
        #                     })
        # NAIVE BAYES
        # Linear regression logistica     
        ]

""" Definir los objetos para la NESTED CROSS VALIDATION"""
inner_cv = KFold(n_splits=2, shuffle=True, random_state=42)
outer_cv = RepeatedKFold(n_splits=2, n_repeats=5, random_state=42)

# Para cada modelo...
results = {}
for nombre, estimator, param_grid in models:
    
    """ INNER LOOP """
    # Búsqueda de los mejores parámetros
    grid_search = GridSearchCV(estimator=estimator, param_grid=param_grid, cv=inner_cv)
    grid_search.fit(x, y)
    
    # Impresión de los resultados del grid search
    parametros = grid_search.best_params_
    resultado = grid_search.best_score_ * 100
    print(f"Mejores parámetros encontrados: {parametros} con una puntuación de: {resultado:.2f} %")
        
    """ OUTER LOOP """
    # Crear un nuevo objeto GridSearchCV utilizando los mejores parámetros encontrados
    conf_estimator = estimator.set_params(**parametros)
    nested_grid_search = GridSearchCV(estimator=conf_estimator, param_grid=param_grid, cv=outer_cv)
    # NOTE: Método de scoring: error cuadrático medio
    nested_score = cross_val_score(nested_grid_search, X=x, y=y, cv=outer_cv, scoring='neg_mean_squared_error').mean() * -1
    print(f'[Prueba del modelo "{nombre}"] Mean squared error: {nested_score:.2f}')
    
    """ GUARDAR RESULTADOS """
    # Se guardarán en forma de diccionario
    results[nombre] = {"param" : parametros, "score" : resultado, "nested_score" : nested_score}

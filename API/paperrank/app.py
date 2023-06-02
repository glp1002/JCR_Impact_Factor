"""
El archivo "app.py" es el archivo principal de tu aplicación donde se configura y ejecuta el servidor de backend. 
Este archivo crea una instancia de Flask y define dos rutas, /articulos/<revista> y 
/indice_impacto/<revista> que corresponden a las rutas que utilizan los métodos obtenerArticulos y 
obtenerIndiceImpacto de la clase Controlador del frontend. Cada ruta se asocia con un método de la aplicación
Flask que crea una instancia de la clase Modelo, llama al método correspondiente y devuelve la respuesta en 
formato JSON.
"""
import json
import os
import secrets
from functools import wraps

import psycopg2
from flask import (Flask, g, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_babel import Babel, gettext

from .backend.controlador import Controlador
from .backend.modelo import Modelo

# from flask_login import LoginManager

#from flask_wtf import CSRFProtect
#from flask_cors import CORS # TODO
# CSRFProtect(app)

# Creación de la aplicación
app = Flask(__name__)

# Genera una clave secreta aleatoria de 32 bytes
secret_key = secrets.token_hex(32)
app.secret_key = secret_key

url_database = os.environ.get("DATABASE_URL")
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect( 
            url_database, 
            sslmode='require'
        )
    return g.db



def refresh():
    modelo = Modelo(get_db())
    controlador = Controlador(modelo)
    return controlador

# controlador.reinitialize_database() -> TODO: admin

# app.config['SESSION_COOKIE_SECURE'] = True -> TODO: https
# app.config['REMEMBER_COOKIE_SECURE'] = True
# CSP: Content Security Policy -> TODO: política de privacidad
# @app.after_request
# def add_security_headers(resp):
#     resp.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data: ;"
#     return resp

# Variables globales de internacionalización con Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = {
    'en': gettext('Inglés'),
    'es': gettext('Español'),
    'fr': gettext('Francés'),
    'it': gettext('Italiano')
}

# Obtiene el idioma preferido del navegador, si no se toma el idioma por defecto de la aplicación
def get_locale():
    lang = session.get('LANGUAGES', None)
    if lang == None:
        browser_locale = request.accept_languages.best_match(app.config['LANGUAGES'].keys())
        if browser_locale is not None:
            return browser_locale
        return app.config['BABEL_DEFAULT_LOCALE']
    else:
        app.config['BABEL_DEFAULT_LOCALE'] = lang
        return app.config['BABEL_DEFAULT_LOCALE']

Babel(app, locale_selector=get_locale)

@app.before_request
def before_request():
    if 'lang' in request.args:
        session['LANGUAGES'] = request.args.get('lang')

# Decorador para verificar la autenticación del usuario
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Endpoints
@app.errorhandler(404)
def handle_other(err):
    return render_template('error404.html')

@app.errorhandler(500)      
def handle_other(err):
    return render_template('error500.html')

@app.route('/')
@login_required
def home():
    return redirect('/selection')

@app.route('/login', methods=['GET', 'POST'])
def login():
    controlador = refresh()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['new-password']
        user_exists = controlador.authenticate_user(username, password)
        if user_exists == True:
            session['loggedin'] = True
            session['username'] = username
            return redirect('/selection')
        else:      
            error = gettext('Nombre de usuario o contraseña incorrectos')
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    controlador = refresh()
    if request.method == 'POST':
        username = request.form['new-username']
        password = request.form['new-password']
        email = request.form['new-email']
        controlador.create_user(username, password, email)
        return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect('/')
    
@app.route('/revistas', methods=['GET'])
@login_required
def get_journals():
    controlador = refresh()
    journal_list = controlador.get_journals_list()
    return render_template('journals.html', journal_list=journal_list, username=session.get('username'))

@app.route('/consult', methods=['GET'])
@login_required
def consult():
    revista = request.args.get('revista')
    return render_template('consult.html', revista=revista, username=session.get('username'))

@app.route('/consultJSON/<revista>', methods=['GET'])
@login_required
def consultJSON(revista):
    controlador = refresh()
    # Cálculo de la consulta
    consulta = controlador.get_consulta_jcr(revista)
    # Desempaquetar las tuplas en dos listas
    years, jcrValues = zip(*consulta)
    years = list(years)
    jcrValues = list(jcrValues)

    return jsonify(jcrValues=jcrValues, years=years)

# @app.route('/quartileJSON/<revista>', methods=['GET'])
# @login_required
# def quartileJSON(revista):
#     controlador = refresh()
#     # Cálculo de la consulta
#     consulta = controlador.get_consulta_quartil(revista)
#     # Desempaquetar las tuplas en dos listas
#     years, quartil_list = zip(*consulta)
#     years = list(years)
#     quartil_list = list(quartil_list)

#     return jsonify(quartil_list=quartil_list, years=years)

@app.route('/predictionJSON/<revista>/<modelos_deseados>', methods=['GET'])
@login_required
def predictionJSON(revista, modelos_deseados):
    controlador = refresh()
    # Cálculo de predicciones
    modelos_deseados = modelos_deseados.split(',')
    modelos = controlador.get_model_binaries(modelos_deseados)
    ejemplo1, ejemplo2 = controlador.get_ejemplo(revista)

    # Consulta como la del ejemplo anterior
    consulta = controlador.get_consulta_jcr(revista)  
    years, jcrValues = zip(*consulta)
    years = list(years)
    jcrValues = list(jcrValues)
   
    # Agregar elementos faltantes a ejemplo1 y ejemplo2
    average = sum(ejemplo1) / len(ejemplo1)
    average2 = sum(ejemplo2) / len(ejemplo2)
    ejemplo1.extend([average] * (13 - len(ejemplo1)))
    ejemplo2.extend([average2] * (13 - len(ejemplo2)))

    # Calcular predicciones utilizando comprensión de listas
    predictions = controlador.predict(ejemplo1, modelos)
    predictions = [round(float(numero[0]), 3) for numero in predictions]  # Convertir a float
    predictions = list(zip(modelos_deseados, predictions))  # [(modelo, valor), (modelo2, valor2)...]

    predictions2 = controlador.predict(ejemplo2, modelos)
    predictions2 = [round(float(numero[0]), 3) for numero in predictions2]  # Convertir a float
    predictions2 = list(zip(modelos_deseados, predictions2))  # [(modelo, valor), (modelo2, valor2)...]

    lista_combinada = [(modelo, jcr1, jcr2) for (modelo, jcr1), (_, jcr2) in zip(predictions2, predictions)]

    return jsonify(jcrValues=jcrValues, predictions=lista_combinada, years=years)

@app.route('/prediction', methods=['GET'])
@login_required
def prediction():
    controlador = refresh()

    modelos_deseados = request.args.getlist('modelos')
    modelos_deseados = modelos_deseados[0].split(',')
    revista = request.args.get('revista')
    
    # Cálculo de predicciones
    modelos = controlador.get_model_binaries(modelos_deseados)
    ejemplo1, ejemplo2 = controlador.get_ejemplo(revista)
   
    # Agregar elementos faltantes a ejemplo1 y ejemplo2
    average = sum(ejemplo1) / len(ejemplo1)
    average2 = sum(ejemplo2) / len(ejemplo2)
    ejemplo1.extend([average] * (13 - len(ejemplo1)))
    ejemplo2.extend([average2] * (13 - len(ejemplo2)))

    # Calcular predicciones utilizando comprensión de listas
    predictions = controlador.predict(ejemplo1, modelos)
    predictions = [round(numero[0],3) for numero in predictions]
    predictions = list(zip(modelos_deseados, predictions)) # [(modelo, valor), (moelo2, valor2)...]

    predictions2 = controlador.predict(ejemplo2, modelos)
    predictions2 = [round(numero[0],3) for numero in predictions2]
    predictions2 = list(zip(modelos_deseados, predictions2)) # [(modelo, valor), (moelo2, valor2)...]
    
    return render_template('prediction.html', predictions=predictions, predictions2=predictions2, username=session.get('username'))

@app.route('/selection', methods=['GET', 'POST'])   
@login_required
def formulario():
    controlador = refresh()

    if request.method == 'POST':
        action = request.form.get('action')
        revista = request.form.get('revista')

        if action == 'consultar':
            return redirect(f'/consult?revista={revista}')
        
        elif action == 'predecir':
            modelos_deseados = request.form.getlist('modelo[]')
            return redirect(f'/prediction?revista={revista}&modelos={",".join(modelos_deseados)}')

    else:
        categorias = controlador.get_categories()
        revistas = controlador.get_journals_name()

        # Verificar si los modelos están cargados en la base de datos
        modelos = controlador.get_model_names_and_errors()
        if modelos is None or len(modelos) == 0:
            controlador.insert_models()       
            modelos = controlador.get_model_names_and_errors()
        
        return render_template('selection.html', categorias=categorias, revistas=revistas, modelos=modelos, username=session.get('username'))

@login_required
def get_revistas_por_categoria(categoria):
    controlador = refresh()
    revistas = controlador.get_revistas_por_categoria(categoria)
    return jsonify(revistas=revistas)

# Perfil de usuario
@app.route('/profile', methods=['GET','POST'])
@login_required
def get_profile():
    controlador = refresh()
    username = session.get('username')
    email = controlador.get_email(username)
    if request.method == 'GET':
        return render_template('profile.html', email=email, username=username)
    else:
        new_username = request.form.get('nombre')
        # new_password = request.json['password'] TODO
        new_email = request.form.get('correo')
        done = controlador.update_user(new_username, new_email, email)
        if done == True:
            return render_template('profile.html', email=new_email, username=new_username)
        else:
            return render_template('profile.html', email=email, username=username)

# Recuperar contraseña
@app.route('/recover', methods=['GET'])
def recover_password():
    return render_template('recover.html')

# Ayuda
@app.route('/help', methods=['GET'])
@login_required
def get_help():
    return render_template('help.html', username=session.get('username'))

# Términos de uso
@app.route('/terms_of_use', methods=['GET'])
@login_required
def get_terms_of_use():
    return render_template('termsofuse.html', username=session.get('username'))

# Política de privacidad
@app.route('/privacy_policy', methods=['GET'])
@login_required
def get_privacy_policy():
    return render_template('privacypolicy.html', username=session.get('username'))

# Ruta para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    controlador = refresh()
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    if request.json['admin'] != None:
        admin = request.json['admin']
    done = controlador.create_user(username, password, email, admin)
    return jsonify(done)

# Ruta para obtener la lista de usuarios por rol
@app.route('/users/<role>', methods=['GET'])
def get_users_by_role(role):
    controlador = refresh()
    admin = True if role.lower() == 'admin' else False
    users = controlador.get_users_by_role(admin)
    return jsonify(users)

# Ruta para eliminar un usuario
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    controlador = refresh()
    done = controlador.delete_user(user_id)
    return jsonify(done)


if __name__ == '__main__':
    controlador = refresh()
    controlador.initialize_database()
    app.run()


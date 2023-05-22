"""
El archivo "app.py" es el archivo principal de tu aplicación donde se configura y ejecuta el servidor de backend. 
Este archivo crea una instancia de Flask y define dos rutas, /articulos/<revista> y 
/indice_impacto/<revista> que corresponden a las rutas que utilizan los métodos obtenerArticulos y 
obtenerIndiceImpacto de la clase Controlador del frontend. Cada ruta se asocia con un método de la aplicación
Flask que crea una instancia de la clase Modelo, llama al método correspondiente y devuelve la respuesta en 
formato JSON.
"""
import json
from flask import Flask, jsonify, request, render_template, session, redirect, make_response
from flask_babel import Babel, numbers, dates, gettext
import secrets

from backend.modelo import Modelo
from backend.controlador import Controlador
# from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS # TODO

# Creación de la aplicación
app = Flask(__name__)

# Genera una clave secreta aleatoria de 32 bytes
secret_key = secrets.token_hex(32)
app.config['SECRET_KEY'] = secret_key

# Crear una única instancia de Modelo al inicio de la aplicación
modelo = Modelo()
controlador = Controlador(modelo)

# app.config['SESSION_COOKIE_SECURE'] = True -> TODO: https
# app.config['REMEMBER_COOKIE_SECURE'] = True
# CSP: Content Security Policy -> TODO: política de privacidad
# @app.after_request
# def add_security_headers(resp):
#     resp.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data: ;"
#     return resp

# Internacionalización con Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = {
    'en': 'English',
    'es': 'Español',
    'fr': 'Francaise'
}
babel = Babel(app)

def get_locale():
    # Obtiene el idioma preferido del navegador, si no se toma el idioma por defecto de la aplicación
    lang = request.args.get('lang')
    if lang == None:
        browser_locale = request.accept_languages.best_match(app.config['LANGUAGES'].keys())
        if browser_locale is not None:
            return browser_locale
        return app.config['BABEL_DEFAULT_LOCALE']
    else:
        app.config['BABEL_DEFAULT_LOCALE'] = lang
        return app.config['BABEL_DEFAULT_LOCALE']


babel.init_app(app, locale_selector=get_locale)

# Endpoints
@app.errorhandler(404)
def handle_other(err):
    return render_template('error404.html')

@app.errorhandler(500)      
def handle_other(err):
    return render_template('error500.html')

@app.route('/')
def home():
    if 'username' in session:
        return render_template('selection.html', username=session['username'])
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = controlador.authenticate_user(username, password)
        if user_id != None:
            session['username'] = username
            #return render_template('selection.html', username=session['username'])
            return redirect('/selection')
        else:      
            error = gettext('Nombre de usuario o contraseña incorrectos')
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        controlador.create_user(username, password)
        return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
    
@app.route('/revistas', methods=['GET'])
def get_journals():
    journal_list = controlador.get_journals_list()
    # DEBUG: return jsonify(journal_list)
    return render_template('journals.html', journal_list=journal_list)


    
@app.route('/consult', methods=['GET'])
def consult():
    revista = request.args.get('revista')
    # Cálculo de la consulta
    consulta = controlador.get_consulta_jcr(revista)
    
    # Desempaquetar las tuplas en dos listas
    years, jcrValues = zip(*consulta)

    years_list=[]
    for y in years:
        years_list.append(y)

    return render_template('consult.html', jcrValues=jcrValues, years=json.dumps(years_list))

@app.route('/prediction', methods=['GET'])
def prediction():
    modelos_deseados = request.args.getlist('modelos')
    modelos_deseados = modelos_deseados[0].split(',')
    revista = request.args.get('revista')
    
    # Cálculo de predicciones
    modelos = controlador.get_model_binaries(modelos_deseados)
    consulta = controlador.get_consulta_jcr(revista)  
    ejemplo1, ejemplo2 = controlador.get_ejemplo(revista)
   
    # Agregar elementos faltantes a ejemplo1 y ejemplo2
    average = sum(ejemplo1) / len(ejemplo1)
    average2 = sum(ejemplo2) / len(ejemplo2)
    ejemplo1.extend([average] * (13 - len(ejemplo1)))
    ejemplo2.extend([average2] * (13 - len(ejemplo2)))

    # Calcular predicciones utilizando comprensión de listas
    predictions = controlador.predict(ejemplo1, modelos)
    predictions = [round(numero[0],3) for numero in predictions]
    predictions = list(zip(modelos_deseados, predictions))

    predictions2 = controlador.predict(ejemplo2, modelos)
    predictions2 = [round(numero[0],3) for numero in predictions2]
    predictions2 = list(zip(modelos_deseados, predictions2)) 

    return render_template('prediction.html', consulta=consulta, predictions=predictions, predictions2=predictions2)

@app.route('/selection', methods=['GET', 'POST'])   
def formulario():
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
        
        return render_template('selection.html', categorias=categorias, revistas=revistas, modelos=modelos)
    
def get_revistas_por_categoria(categoria):
    revistas = controlador.get_revistas_por_categoria(categoria)
    return jsonify(revistas=revistas)

# Perfil de usuario
@app.route('/profile', methods=['GET'])
def get_profile():
    return render_template('profile.html')    

# Ruta para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
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
    admin = True if role.lower() == 'admin' else False
    users = controlador.get_users_by_role(admin)
    return jsonify(users)

# Ruta para actualizar la información de un usuario
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    new_username = request.json['username']
    new_password = request.json['password']
    new_email = request.json['email']
    new_admin = request.json['admin']
    done = controlador.update_user(user_id, new_username, new_password, new_email, new_admin)
    return jsonify(done)

# Ruta para eliminar un usuario
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    done = controlador.delete_user(user_id)
    return jsonify(done)

if __name__ == '__main__':
    app.run()

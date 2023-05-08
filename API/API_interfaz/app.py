"""
El archivo "app.py" es el archivo principal de tu aplicación donde se configura y ejecuta el servidor de backend. 
Este archivo crea una instancia de Flask y define dos rutas, /articulos/<revista> y 
/indice_impacto/<revista> que corresponden a las rutas que utilizan los métodos obtenerArticulos y 
obtenerIndiceImpacto de la clase Controlador del frontend. Cada ruta se asocia con un método de la aplicación
Flask que crea una instancia de la clase Modelo, llama al método correspondiente y devuelve la respuesta en 
formato JSON.
"""

from flask import Flask, jsonify, request, render_template, session, redirect

from backend.servidor.modelo import Modelo
from backend.servidor.controlador import Controlador

app = Flask(__name__)

# Crear una única instancia de Modelo al inicio de la aplicación
modelo = Modelo()
controlador = Controlador(modelo)


# app.config['SESSION_COOKIE_SECURE'] = True -> TODO: https
# app.config['REMEMBER_COOKIE_SECURE'] = True
# CSP: Content Security Policy -> TODO: política de privacidad
# @app.after_request
# def add_security_headers(resp):
#     resp.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data: /frontend/icons;"
#     return resp


# Endpoints
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
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
            return redirect('index.html')
        else:
            return render_template('login.html', error='Invalid username or password')
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

@app.route('/articulos/<revista>', methods=['GET'])
def obtener_articulos(revista):
    articulos = controlador.obtener_articulos(revista)    
    # DEBUG: return jsonify(articulos)
    return render_template('articulos.html', articulos=articulos)


@app.route('/indice_impacto/<revista>', methods=['GET'])
def obtener_indice_impacto(revista):
    indice_impacto = controlador.obtener_indice_impacto(revista)
    # DEBUG: return jsonify(indice_impacto)
    return render_template('calculo.html', indice=indice_impacto)
    

if __name__ == '__main__':
    app.run()

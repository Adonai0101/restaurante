from flask import Flask,render_template,redirect

#variables de entorno
from decouple import config

#BluePrints
from usuarios import usuarios
from dashboard import dashboard
from productos import productos
from menu import menu
from master import master

#Database
from database import mongo

app = Flask(__name__)
app.secret_key = "SUpersecretoalvalvPutoelqueloleaporqessecreto"

#Mongo db
app.config['MONGO_URI'] = config('URL_DB')
#app.config['MONGO_URI'] = 'mongodb://localhost'
mongo.init_app(app)

#Registrando blueprints(Mas rutas para el servidor)
app.register_blueprint(usuarios, url_prefix='/usuarios')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(productos, url_prefix='/productos')
app.register_blueprint(menu,url_prefix = '/menu')
app.register_blueprint(master,url_prefix = '/master')

@app.route('/')
def hello():
    return redirect('/menu')

@app.route('/terminoscondiciones')
def terminos():
    return render_template('terminos.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') , 404

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug=True, port=5000)
from flask import Blueprint,render_template,redirect,request,flash,session
from database import mongo

from bson import json_util
from bson.objectid import ObjectId

from tools import *

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    if 'usuario' in session:
        usuario = mongo.db.usuarios.find_one({'_id':ObjectId(session['usuario'])})
        del usuario['password']
        
        #obteniendo categorias
        query = {'user_id':str(session['usuario'])}
        productos = mongo.db.productos.find(query)
        categorias = []
        categoria_temp = []
        for x in productos:
            if not x['categoria'] in categoria_temp:
                temp = {
                    'categoria' : x['categoria'],
                    'foto' : x['fotos']
                }
                categoria_temp.append(x['categoria'])
                categorias.append(temp)
        return render_template('dashboard.html',usuario = usuario, categorias = categorias)
    else:
        return redirect('/usuarios/login')

@dashboard.route('/<string:categoria>')
def categorias(categoria):
    if 'usuario' in session:

        dato = []
        query = {
            '$and':[
                {'user_id':str(session['usuario'])},
                {'categoria':categoria}
            ]
        }
        productos = mongo.db.productos.find(query)
        for i in productos:

            temp = {
                'id':i['_id'],
                'nombre': i['nombre'],
                'categoria': i['categoria'],
                'precio': i['precio'],
                'ingredientes': i['ingredientes'],
                'fotos':i['fotos'],
                'user_id':i['user_id']
            }
            dato.append(temp)
        return render_template('categorias.html',items = dato, categoria = categoria)
    else:
        return redirect('/usuarios/login')


@dashboard.route('/producto/<string:id>')
def producto(id):
    if 'usuario' in session:

        producto = mongo.db.productos.find_one({'_id':ObjectId(id)})
        return render_template('producto.html',producto = producto)
    else:
        return redirect('/usuarios/login')


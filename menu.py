from itertools import product
from flask import Blueprint,render_template,redirect,request,flash,session,url_for
from database import mongo

from bson import json_util
from bson.objectid import ObjectId

from tools import *

menu = Blueprint('menu', __name__)

@menu.route('/')
def index():
    dato = []
    usuarios = mongo.db.usuarios.find()
    for i in usuarios:
        temp = {
            'id':i['_id'],
            'nombre':i['nombre'],
            'foto':i['foto']
        }
        dato.append(temp)
    #return render_template('usuarios_menu.html', usuarios = dato)
    return render_template('/menu/index.html', usuarios = dato)
@menu.route('/<string:id>')
def menu_user(id):

    #guardamos el id del vendedor para usarlo mas adelante (en el sidebar la verdad)
    session['id_vendesor'] = id

    categorias = []
    dato = []

    #validamos que exista un usuario
    exist_products = mongo.db.productos.find({'user_id':id}).count()

    if exist_products == 0:
        return redirect('/fail')

    #obteniendo todos los productos de un usuario
    productos = mongo.db.productos.find({'user_id':id})

    for i in productos:
        item = {
            'categoria':i['categoria'],
            'foto':i['fotos'],
            'nombre':i['nombre'],
            'id': i['_id']
        }
        dato.append(item)
        
        if not i['categoria'] in categorias:
            categorias.append(i['categoria'])
        
    #obteniendo toda la informacion del usuario
    usuario = mongo.db.usuarios.find_one({'_id':ObjectId(id)})

    del usuario['password']
    del usuario['email']

    #return render_template('menu.html', items = dato, categorias = categorias, usuario = usuario)
    return render_template('/menu/menu.html', items = dato, categorias = categorias, usuario = usuario)



@menu.route('/producto/<string:id>')
def menu_producto(id):

    producto = mongo.db.productos.find_one({'_id':ObjectId(id)})


    #obteniendo toda la informacion del usuario
    usuario = mongo.db.usuarios.find_one({'_id':ObjectId(producto['user_id'])})
    del usuario['password']
    del usuario['email']
    #return render_template('menu_producto.html',datos = producto, usuario = usuario)
    return render_template('/menu/producto.html',producto = producto, usuario = usuario)
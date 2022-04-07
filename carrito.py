from asyncio import constants
from math import prod
from flask import Blueprint,jsonify, request, Response,session,render_template,flash,redirect

from bson import json_util
from bson.objectid import ObjectId
from pymongo.read_preferences import Primary
from werkzeug.utils import environ_property

#Database
from database import mongo

#variables de entorno
from decouple import config

from admin_cloudinary import *

from tools import *
from send_mail import *

import time

carrito = Blueprint('carrito',__name__)

@carrito.route('/')
def index():
    paquetes = []
    if 'lista_carrito' in session:
        print('valor del carrito: ' , session['lista_carrito'])

        item_list = []
        for carrito in session['lista_carrito']: # 'carrito' es el id del producto
            paquete = {
                'id_vendedor':"",
                'nombre_vendedor':"",
                'productos':[],
                'total': int(config('COSTO_ENVIO'))
            }

            vendedor = mongo.db.usuarios.find_one({'_id':ObjectId(carrito)})
            paquete['id_vendedor'] = str(vendedor['_id'])
            paquete['nombre_vendedor'] = vendedor['nombre']

            nombre_carrito = 'carrito_' + carrito
            print(session[nombre_carrito])
            carrito_temp = session[nombre_carrito]
            for i in carrito_temp:
                producto = mongo.db.productos.find_one({'_id':ObjectId(i)})
                item = {
                    'id_producto':str(producto['_id']),
                    'nombre_producto':producto['nombre'],
                    'foto_producto':producto['fotos'][0],
                    'cantidad': carrito_temp[i],
                    'precio' : int(producto['precio']) * carrito_temp[i]
                }
                
                paquete['total'] = paquete['total'] + item['precio']
                
                item_list.append(item)
                paquete['productos'] = item_list

            item_list = []  
            paquetes.append(paquete)

        return jsonify({'paquetes':paquetes})
    else:
        return "vacio"

#para el boton de agregar al carrito
@carrito.route('/add',methods = ['POST'])
def add_carrito():
    id_vendedor = request.json['id_vendedor']
    id_producto = request.json['id_producto']
    cantidad = int(request.json['cantidad'])

    #primero creamos mi lista de carritos
    if not 'lista_carrito' in session:
        session['lista_carrito'] = []
    else:
        if id_vendedor in session['lista_carrito']:
            print('carrito dinamico ya existe')
            nombre_carrito = 'carrito_' + id_vendedor
            if id_producto in session[nombre_carrito]:
                print('producto existe en carrito dinamico')
                carrito_temp = session[nombre_carrito]
                carrito_temp[id_producto] = int(carrito_temp[id_producto]) + int(cantidad)
                session[nombre_carrito] = carrito_temp
            else:
                print('producto NO existe en carrito dinamico')
                carrito_temp = session[nombre_carrito]
                carrito_temp[id_producto] = cantidad
                session[nombre_carrito] = carrito_temp
        else:
            #agregarmos el id_vendedor a la lista
            print('Agregando nuevo carrito dinamico')
            lista_carrito = session['lista_carrito']
            lista_carrito.append(id_vendedor)
            session['lista_carrito'] = lista_carrito
            #print(session['lista_carrito'])
            #generando el carrito dinamico
            nombre_carrito = 'carrito_' + id_vendedor
            item = {
                id_producto:cantidad
            }
            session[nombre_carrito] = item
            print(session[nombre_carrito])

    return jsonify({'msj':'resivido'})
    

#obtener la data de un solo carrito
@carrito.route('/<id>')
def get_one(id):
    item_list = []

    paquete = {
        'id_vendedor':"",
        'nombre_vendedor':"",
        'telefono_vendedor':"",
        'email_vendedor':"",
        'productos':[],
        'total': int(config('COSTO_ENVIO'))
    }

    if 'lista_carrito' in session:

        if id in session['lista_carrito']:

            vendedor = mongo.db.usuarios.find_one({'_id':ObjectId(id)})
            paquete['id_vendedor'] = str(vendedor['_id'])
            paquete['nombre_vendedor'] = vendedor['nombre']
            paquete['telefono_vendedor'] = vendedor['telefono']
            paquete['email_vendedor'] = vendedor['email']

            nombre_carrito = 'carrito_' + id
            carrito_temp = session[nombre_carrito]
            print(carrito_temp)
            for i in carrito_temp:
                producto = mongo.db.productos.find_one({'_id':ObjectId(i)})
                item = {
                    'id_producto':str(producto['_id']),
                    'nombre_producto':producto['nombre'],
                    'foto_producto':producto['fotos'][0],
                    'cantidad': carrito_temp[i],
                    'precio' : int(producto['precio']) * carrito_temp[i]
                }

                paquete['total'] = paquete['total'] + item['precio']
                
                item_list.append(item)
                paquete['productos'] = item_list

            return jsonify({'paquete':paquete})

    return jsonify({'msj':'404'})



#ruta que regresa la lista con los nombres de los carritos dinamicos
@carrito.route('/list')
def list_cart():
    lista = []
    if 'lista_carrito' in session:
        
        lista = session['lista_carrito']
        print(lista)
        return jsonify({'lista_carrito':lista})

    return jsonify({'lista_carrito':lista})


#ruta para generar la compra del carrito
@carrito.route('/comprar', methods = ['POST'])
def comprar():
    id_cliente = session['cliente']
    cliente = mongo.db.clientes.find_one({'_id':ObjectId(id_cliente)})
    
    domicilio = "espendado domicilio alv"
    paquete = request.json
    

    #datos del cliente
    paquete['id_cliente'] = str(cliente['_id'])
    paquete['nombre_cliente'] = cliente['nombre']
    paquete['telefono_cliente'] = cliente['telefono']
    paquete['email_cliente']  = cliente['email']
    paquete['domicilio_cliente'] = cliente['domicilio']
    paquete['foto_cliente'] = cliente['foto'] #agregue esta linea de shit
    paquete['estado_compra'] = 'pendiente'
    paquete['nota'] = ""
    paquete['fecha'] = obtener_fecha()

    session['orden_paquete'] = paquete

    return jsonify(paquete)




#ruta de prueba para limpiar el carrito
@carrito.route('/clear')
def limpiar_carrito():
    session.pop("carrito",None)
    session.pop("lista_carrito",None)
    session.clear()
    return "se limpio"
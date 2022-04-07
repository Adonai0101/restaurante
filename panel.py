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

panel = Blueprint('panel',__name__)


@panel.route('/')
def index():
    if 'cliente' in session:
        
        id = session['cliente']

        #modulo de favoritos
        favoritos = []
        arg = []
        res = mongo.db.compras.find_one({'id_cliente':id})
        if res: # validamos esta perra shit que exista un valor porq si no vale verga esto
            res = res['productos']
            
            for i in res:
                if i['id_producto'] in arg:
                    pass    # un iz filtro
                else:
                    arg.append(i['id_producto'])
                    temp = {
                        'id':i['id_producto'],
                        'nombre':i['nombre_producto'],
                        'foto':i['foto_producto']
                    }
                    favoritos.append(temp)
        
        favoritos = favoritos[0:5]
        return render_template('clientes/inicio.html', favoritos = favoritos)
    else:
        return redirect('/clientes/login')

#Modulo de restaurante
@panel.route('/restaurantes')
def restaurantes():
    if 'cliente' in session:
        restaurantes = []
        usuarios = mongo.db.usuarios.find()
        for x in usuarios:
            temp = {
                'id':x['_id'],
                'nombre': x['nombre'],
                'foto':x['foto'],
            }
            restaurantes.append(temp)
        print(restaurantes)
        return render_template('clientes/restaurantes.html' , restaurantes = restaurantes)
    else:
        return redirect('/clientes/login')

@panel.route('/restaurante/<id>')
def show_restaurante(id):
    if 'cliente' in session:

        categorias = []
        dato = []
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
        
        return render_template('/clientes/restaurante.html', items = dato, categorias = categorias, usuario = usuario)
    else:
        return redirect('/clientes/login')


#mostrar el producto para hacer el pedido
@panel.route('/producto/<id>')
def show_producto(id):
    if 'cliente' in session:
        producto = mongo.db.productos.find_one({'_id':ObjectId(id)})

        user_id = producto['user_id']
        vendedor = mongo.db.usuarios.find_one({'_id':ObjectId(user_id)})

        bandera = True
        dia = dia_semana()
        horario = vendedor['horario'][dia]
        """
        print(horario[0])
        print(convertir_hora(horario[0]))
        print(hora_actual())
        """
        if horario[0] == '' or horario[1] == '':
            print('cerrado')
            bandera = False
        else:
            if horario[0] or horario[1]:
                bandera = True
                print('si hay')
                hora_inicio = convertir_hora(horario[0])
                hora_fin = convertir_hora(horario[1])
                if hora_actual() < hora_inicio or hora_actual() > hora_fin:
                    print('cerrado')
                    bandera = False
                else:
                    bandera = True
                    print('abierto')
            else:
                print('cerrado')
                bandera = False
                

        

        return render_template('clientes/producto.html',producto = producto , vendedor = vendedor , bandera = bandera)
    else:
        return redirect('/clientes/login')



@panel.route('/orden')
def show_orden():
    if 'cliente' in session:

        id_cliente = session['cliente']
        datos_cliente = mongo.db.clientes.find_one({'_id':ObjectId(id_cliente)})

        data_orden = session['orden']

        producto = mongo.db.productos.find_one({'_id':ObjectId(data_orden['id_producto'])})
        
        precio = int(data_orden['cantidad']) * int(producto['precio'])
        precio_envio = 30
        total = precio + precio_envio

        costos = {
            'cantidad':data_orden['cantidad'],
            'precio' : precio,
            'precio_envio':precio_envio,
            'total' : total
        }     
        return render_template('/clientes/orden.html',
        cliente = datos_cliente , producto = producto, costos = costos)

    else:
        return redirect('/clientes/login')

#en esta ruta generaremos la estructura de dato para ser guardada la compra
@panel.route('/orden', methods = ['POST'])
def post_orden():
    #obtengo los valores del fontend
    id_producto = request.json['id']
    cantidad = request.json['cantidad']
    
    #genero mi item del producto
    productos = []
    producto = mongo.db.productos.find_one({'_id':ObjectId(id_producto)})
    item = {
        'id_producto':str(producto['_id']),
        'nombre_producto':producto['nombre'],
        'foto_producto':producto['fotos'][0],
        'cantidad': int(cantidad),
        'precio' : int(producto['precio']) * int(cantidad)
    }
    productos.append(item)

    #obtenemos los datos del cliente
    id_cliente = session['cliente']
    cliente = mongo.db.clientes.find_one({'_id':ObjectId(id_cliente)})
    
    #obtenemos lod datos del vendedor
    id_vendedor = producto['user_id']
    vendedor = mongo.db.usuarios.find_one({'_id':ObjectId(id_vendedor)})
    
    total = int(config('COSTO_ENVIO')) + ( int(cantidad) * int(producto['precio']))

    #armamos el pedido
    paquete = {
        'id_vendedor':str(vendedor['_id']),
        'nombre_vendedor': vendedor['nombre'],
        'telefono_vendedor':vendedor['telefono'],
        'email_vendedor':vendedor['email'],
        'productos':productos,
        'total': total,
        #datos del cliente
        'id_cliente' : str(cliente['_id']),
        'nombre_cliente' : cliente['nombre'],
        'telefono_cliente' : cliente['telefono'],
        'email_cliente' : cliente['email'],
        'domicilio_cliente' : cliente['domicilio'],
        'foto_cliente' : cliente['foto'],
        'estado_compra' : 'pendiente',
        'nota' : "",
        'fecha' : obtener_fecha()
    }

    #guardamos el pedido/paquete en la variable de session 'session['orden_paquete']'
    session['orden_paquete'] = paquete
    
    print('--------------finaliza compra rapida --------------')
    return 'works'


@panel.route('/comprar', methods = ['POST']) #esta ruta es sospechosa a ser eliminada
def post_comprar():
    if 'cliente' in session:
        
        id_cliente = session['cliente']
        orden = session['orden']
        domicilio = request.json['domicilio']
        nota = request.json['nota']
        precio_envio = 30

        #obtenemos los datos de cada coleccion

        producto = mongo.db.productos.find_one({'_id':ObjectId(orden['id_producto'])})
 
        id_vendedor = producto['user_id']

        vendedor = mongo.db.usuarios.find_one({'_id':ObjectId(id_vendedor)})

        cliente = mongo.db.clientes.find_one({'_id':ObjectId(id_cliente)})

        #armamos el 'json' de lo que sera la info de la compra
        datos_compra = {
            #datos del vendedor
            'id_vendedor':str(vendedor['_id']),
            'nombre_vendedor':vendedor['nombre'],
            'domicilio_vendedor':vendedor['domicilio'],
            'telefono_vendedor':vendedor['telefono'],

            #datos del cliente
            'id_cliente': str(cliente['_id']),
            'nombre_cliente':cliente['nombre'],
            'telefono_cliente':cliente['telefono'],
            'email_cliente':cliente['email'],
            'domicilio_cliente':domicilio,

            #datos del producto
            'id_producto':str(producto['_id']),
            'nombre_producto':producto['nombre'],
            'foto_producto':producto['fotos'][0],
            'categoria_producto':producto['categoria'],
            'precio_producto':producto['precio'],

            # mas datos de la compra
            #id de la compra, se genera al hacer la insercion en la DB
            'nota':nota,
            'cantidad_producto':orden['cantidad'],
            'precio_envio':precio_envio,
            'total': ( int(producto['precio']) * int(orden['cantidad']) ) + precio_envio,
            'estado_compra':'pendiente',
            'fecha': obtener_fecha()
            #---
        }

        #registar en la db la compra
        id_compra = mongo.db.compras.insert(datos_compra)

        #notificar al vendedor
        mail_vendedor = vendedor['email']
        asunto = "Nuevo pedido"
        msj = "Tienes un nuevo pedido!! \n Revisalo en https://menuzapotlan.club/dashboard/pedidos"
        mail_notificacion(mail_vendedor,asunto,msj)


        return "agregar una buena respuesta xd"
    else:
        return "tienes que hacer login"


@panel.route('/compra/hecho')
def compra_done():
    if 'cliente' in session:
        return render_template('clientes/compra_done.html')
    else:
        return redirect('/clientes/login')

#!! NOTA todas las modificaciones del perfil se hacen en 'clientes'
@panel.route('/perfil')
def perfil():
    if 'cliente' in session:
        id = session['cliente']
        cliente = mongo.db.clientes.find_one({'_id':ObjectId(id)})
        del cliente['password']
        return render_template('clientes/perfil.html', cliente = cliente)
    else:
        return redirect('/clientes/login')

#ruta para obtener los datos del usuario y mostrarlos via js
@panel.route('/test')
def test():
    id = session['cliente']
    cliente = mongo.db.clientes.find_one({'_id':ObjectId(id)})
    del cliente['password'] 
    response = json_util.dumps(cliente)
    return response


#rutas para que el usuario visualice los pedidos
@panel.route('/compras')
def show_pedidos():
    if 'cliente' in session:

        id_cliente = session['cliente']
        compras = []
        res =  mongo.db.compras.find({'id_cliente':id_cliente}).sort('fecha',-1)
        for i in res:
            temp = {
                'nombre_vendedor':i['nombre_vendedor'],
                'estado':i['estado_compra'],
                'fecha':i['fecha'],
                'productos':i['productos'],
                'total':i['total']
            }
            compras.append(temp)
        return render_template('/clientes/compras.html', compras =  compras)
    else:
        return redirect('/clientes/login')


#ruta para la visualizacion del carrito
@panel.route('/carrito')
def show_carrito():
    if 'cliente' in session:


        return render_template('/clientes/carrito.html')
    else:
        return redirect('/clientes/login')














#modulos para pedir datos por axios/fetch/ajax
@panel.route('/api/restaurantes')
def api_restaurante():
    if 'cliente' in session:
        restaurantes = []
        #ordenamos de mayor a menor
        usuarios = mongo.db.usuarios.find().sort('puntos',-1)
        
        for x in usuarios:
            temp = {
                'id':str(x['_id']),
                'nombre': x['nombre'],
                'foto':x['foto'],
            }
            restaurantes.append(temp)

        return jsonify({'datos':restaurantes})
    else:
        return 'inicia sesion'

@panel.route('/api/productos')
def api_productos():
    if 'cliente' in session:
        datos = []
        productos = mongo.db.productos.find()
        for x in productos:
            temp = {
                'id':str(x['_id']),
                'nombre':x['nombre'],
                'fotos':x['fotos'],
                'categoria':x['categoria']
            }
            datos.append(temp)
        return jsonify({'datos':datos})
        
    else:
        return 'inicia sesion'

#solo en este caso el "usuario" hace referencia al cliente no al restaurante/vendedor
@panel.route('/api/usuario')
def get_login_user():
    if 'cliente' in session:
        id = session['cliente']
        datos_cliente = mongo.db.clientes.find_one({'_id':ObjectId(id)})
        del datos_cliente['password']
        del datos_cliente['email']
        del datos_cliente['foto']
        del datos_cliente['foto_key']
        del datos_cliente['puntos']

        id_data = str(datos_cliente['_id'])
        #del datos_cliente['_id']
        datos_cliente['id'] = id_data
        
        resp = json_util.dumps(datos_cliente)
        return Response(resp, mimetype="application/json")
    else:
        return 'inicia sesion'

@panel.route('/api/producto/<id>')
def get_producto(id):
    if 'cliente' in session:
        producto = mongo.db.productos.find_one({'_id':ObjectId(id)})
        id_producto = str(producto['_id'])
        producto['id'] = id_producto
        response = json_util.dumps(producto)
        return Response(response, mimetype="application/json")
    else:
        return 'inicia sesion'

@panel.route('/api/vendedor/<id>')
def get_vendedor(id):
    if 'cliente' in session:
        vendedor = mongo.db.usuarios.find_one({'_id':ObjectId(id)})
        del vendedor['password']
        del vendedor['foto_key']
        id_vendedor = str(vendedor['_id'])
        vendedor['id'] = id_vendedor
        response = json_util.dumps(vendedor)
        return Response(response, mimetype="application/json")
    else:
        return 'inicia sesion'
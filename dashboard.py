from flask import Blueprint,render_template,redirect,request,flash,session
from database import mongo

from bson import json_util
from bson.objectid import ObjectId

from tools import *
from send_mail import *

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
        #return render_template('dashboard.html',usuario = usuario, categorias = categorias)
        return render_template('/vendedores/dashboard.html',usuario = usuario, categorias = categorias)
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
        #return render_template('categorias.html',items = dato, categoria = categoria)
        return render_template('/vendedores/productos_categoria.html',items = dato, categoria = categoria)
    else:
        return redirect('/usuarios/login')


@dashboard.route('/producto/<string:id>')
def producto(id):
    if 'usuario' in session:

        producto = mongo.db.productos.find_one({'_id':ObjectId(id)})
        #return render_template('producto.html',producto = producto)
        return render_template('/vendedores/producto.html',producto = producto)
    else:
        return redirect('/usuarios/login')



#agregamos las rutas para ver los pedidos

@dashboard.route('/pedidos')
def show_pedidos():
    if 'usuario' in session:
        
        id_vendedor = session['usuario']

        pedidos = []
        res =  mongo.db.compras.find({'id_vendedor':id_vendedor})
        for i in res:
            pedidos.append(i)
        
        return render_template('/vendedores/pedidos.html',pedidos = pedidos)
    else:
        return redirect('/usuarios/login')


@dashboard.route('/pedido/<id>')
def show_pedido(id):
    if 'usuario' in session:

        id_usuario = session['usuario']
        res =  mongo.db.compras.find_one({'_id':ObjectId(id)})
        # pequeña validacion para que solo el vendedor pueda ver su pedido
        if not session['usuario'] == res['id_vendedor']:
            return redirect('/dashboard')
        else:
            session['done'] = "validate_done"
            return render_template('/vendedores/pedido.html', pedido = res , usuario = id_usuario)
    else:
        return redirect('/usuarios/login')

@dashboard.route('/pedido/done/<id>')
def done_pedido(id):
    if 'usuario' in session:
        if 'done' in session:
            session.pop("done",None)

            #updating pedido
            mongo.db.compras.update_one(
                {
                    '_id': ObjectId(id)
                },
                {
                    '$set':{
                        'estado_compra':'hecho'
                }}
            )

            #obteniendo el email del cliente
            res =  mongo.db.compras.find_one({'_id':ObjectId(id)})
            print(res['email_cliente'])
            
            #notificar al repartidor

            #notificar al usuario
            mail_vendedor = res['email_cliente']
            asunto = "Tu pedido esta en camino!!"
            msj = "Tu pedido fue terminado, en breve un repartidor llegara a tu domicilio"
            mail_notificacion(mail_vendedor,asunto,msj)


            return redirect('/dashboard/pedidos')
        else:
            return "a quien quieres engañar  hijo de perra"
    else:
        return redirect('/usuarios/login')



@dashboard.route('/perfil')
def show_perfil():
    if 'usuario' in session:
        id = session['usuario']
        vendedor = mongo.db.usuarios.find_one({'_id':ObjectId(id)})
        return render_template('/vendedores/perfil.html', vendedor = vendedor)
    else:
        return redirect('/usuarios/login')


@dashboard.route('/qr')
def show_qr():
    if 'usuario' in session:
        id = session['usuario']
        
        return render_template('/vendedores/qr.html',id = id)
    else:
        return redirect('/usuarios/login')

@dashboard.route('/get/vendedor')
def get_vendedor():
    if 'usuario' in session:
        id = session['usuario']
        vendedor = mongo.db.usuarios.find_one({'_id':ObjectId(id)})
        del vendedor['password'] 
        response = json_util.dumps(vendedor)
        return response
    else:
        return "no tienes permiso para ver esta shit"

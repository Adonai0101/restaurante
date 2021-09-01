from bson import objectid
from flask import Blueprint, app, json,render_template,redirect,request,flash,session,url_for
from database import mongo

from bson import json_util
from bson.objectid import ObjectId

from tools import *

from admin_cloudinary import *

#variables de entorno
from decouple import config

master = Blueprint('master', __name__)

@master.route('/')
def index_master():
    if 'MASTER' in session:
        fecha_actual =  obtener_fecha()
        res = mongo.db.usuarios.find()
        usuarios = []
        for i in res:

            if i['fecha_pago'] > fecha_actual:
                print("todo bien tienes tiempo ")
                ban = 'corriente'
            else:
                print('llego la hora de pagar')
                ban = 'deuda'

            temp = {
                'id':i['_id'],
                'nombre':i['nombre'],
                'fecha_pago':i['fecha_pago'],
                'pago_estado':ban
            }
            usuarios.append(temp)

        return render_template('master.html',usuarios = usuarios)
    else:
        msj_error = 'a donde perro!'
        flash(msj_error)
        return redirect('/master/auth')


#pagando un mes mas
@master.route('/pago',methods = ['POST'])
def pagar():
    if 'MASTER' in session:
        id = request.json['id']
        res = mongo.db.usuarios.find_one({'_id':ObjectId(id)})
        ultimo_pago = res['fecha_pago']
        print(ultimo_pago)

        mongo.db.usuarios.update_one(
            {
                '_id': ObjectId(id)
            },
            {
                '$set':{
                    'fecha_pago': proximo_pago(ultimo_pago)
            }}
        )
        
        return 'pago works'
    else:
        msj_error = 'a donde perro!'
        flash(msj_error)
        return redirect('/master/auth')

@master.route('/user/<id>')
def id_user(id):

    if 'MASTER' in session:
        
        no_products = mongo.db.productos.find({'user_id':id}).count()
        nombre = mongo.db.usuarios.find_one({'_id':ObjectId(id)})
        nombre = nombre['nombre']

        resp = mongo.db.productos.find({'user_id':id})
        dato = []
        
        for x in resp:
            temp = {
                'id':x['_id'],
                'producto':x['nombre'],
                'fotos' : x['fotos']
            }
            dato.append(temp)
        return render_template('master_usuario.html',cant = no_products,nombre = nombre, datos=dato)
    else:
        msj_error = 'a donde perro!'
        flash(msj_error)
        return redirect('/master/auth')


#Eliminar todo el usuario alv
@master.route('/delete/user',methods = ['POST'])
def ver_usuario():
    if 'MASTER' in session:

        print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        id = request.json['id']

        #obtenemos los id's de las fotos guartdadas
        productos = mongo.db.productos.find({'user_id': id})
        keys = []
        for x in productos:
            keys = keys + x['publicID']

        #elimonamos todos los registros de ese usuario
        mongo.db.productos.delete_many({'user_id': id})
        for foto_id in keys:
            destroy_image(foto_id)
        
        #eliminamos el usuario
        mongo.db.usuarios.delete_one({'_id': ObjectId(id)})

        return 'delet¡ing user'
    else:
        msj_error = 'a donde perro!'
        flash(msj_error)
        return redirect('/master/auth')



#Eliminando un item de cualquier usuario
@master.route('/user/delete/item',methods = ['POST'])
def delete_item():
    id = request.json['id']
    producto = mongo.db.productos.find_one({'_id': ObjectId(id)})
    keys_fotos = producto['publicID']
    #eliminando fotos
    for fotoID in keys_fotos:
        destroy_image(fotoID)
    #eliminando el registro de la db
    mongo.db.productos.delete_one({'_id': ObjectId(id)})

    return 'item eliminado'



@master.route('/auth')
def auth():
    return render_template('master_auth.html')

@master.route('/auth',methods = ['POST'])
def auth_post():
    user = request.form['user']
    password = request.form['password']
    
    myuser = config('MASTER')
    mypassword = config('PASSWORD_MASTER')

    if user == myuser and password == mypassword:
        print ('awevo todo ook')
        session["MASTER"] = 'MASTER' 
        return redirect('/master')

    msj_error = 'NO PUEDES FALLAR'
    flash(msj_error)
    return redirect('/master/auth')

@master.route('/logout')
def logout():
    session.pop("MASTER",None)
    return redirect('/menu')
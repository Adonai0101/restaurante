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

compra = Blueprint('compra',__name__)

#NO olvides agregar una validacion aqui para ver si existe algo o tu sabes que pedo

@compra.route('/')
def index():
    paquete = session['orden_paquete']
    return render_template('/clientes/compra.html', paquete = paquete)

@compra.route('/' , methods = ['POST'])
def comprar():
    print('entre a la compra')
    paquete = session['orden_paquete']

    paquete['domicilio_cliente'] = request.json['domicilio']
    paquete['nota'] = request.json['nota']

    #guardar la compra en la DB
    mongo.db.compras.insert_one(paquete)

    #notificar al vendedor
    mail_vendedor = paquete['email_vendedor']
    asunto = "Nuevo pedido"
    msj = "Tienes un nuevo pedido!! \n Revisalo en https://menuzapotlan.com/dashboard/pedidos"
    mail_notificacion(mail_vendedor,asunto,msj)

    #borrar el carrito dinamico
    id_vendedor = paquete['id_vendedor']
    nombre_carrito = 'carrito_' + id_vendedor
    session[nombre_carrito] = {}

    #borramos de la lista de carritos

    # este if esta porque cuando hago una compra directa me da error
    # ya que la compra directa no la guardo en la lista de carritos
    #por eso valido que si xisten carritos se eliminen
    if id_vendedor in session['lista_carrito']: 
        session['lista_carrito'].remove(id_vendedor)

    #eliminamos la orden de compra
    session.pop('orden_paquete',None)

    #falta notificar al vendedor


    return jsonify({'message':'done'})
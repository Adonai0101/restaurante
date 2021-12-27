from flask import Blueprint,jsonify, request, Response,session,render_template,flash,redirect

from bson import json_util
from bson.objectid import ObjectId

#Database
from database import mongo

#variables de entorno
from decouple import config

from admin_cloudinary import *

from tools import *
from send_mail import *

clientes = Blueprint('clientes',__name__)


@clientes.route('/')
def index():
    return 'clientes'



@clientes.route('/registro')
def registro_template():
    return render_template('/clientes/registro.html')

@clientes.route('/registro',methods = ['POST'])
def registrar_cliente():
    usuario = {
        'nombre' : request.form['nombre'],
        'domicilio' : request.form['domicilio'],
        'telefono' : request.form['telefono'],
        'email' : request.form['email'],
        'password' : encriptar( request.form['password']),
        'foto':'../static/img/clientes/perfil.png',
        'foto_key':'123',
        'puntos': '3'
    }

    #Validacion de campos vacios
    if len(usuario['nombre']) < 5:
        msj_error = 'Ingresa un nombre valido'
        flash(msj_error)
        return redirect('/clientes/registro')

    if len(usuario['domicilio']) < 5:
        msj_error = 'Ingresa un domicilio valido'
        flash(msj_error)
        return redirect('/clientes/registro')

    if len(usuario['password']) < 5:
        msj_error = 'usa una contraseña que contenga al menos 5 letras o números'
        flash(msj_error)
        return redirect('/clientes/registro')

    #Pequeña validacion para no duplicar telefonos, emails y nombres de negocios
    if not email_valido(usuario['email']):
        msj_error = 'email invalido, intenta nuevamente'
        flash(msj_error)
        return redirect('/clientes/registro')
        
    if not numero_valido(usuario['telefono'],10):
        msj_error = 'Númerode telefono invalido, intenta nuevamente'
        flash(msj_error)
        return redirect('/clientes/registro')

    #Validando que no este nada registrado
    emailDB = mongo.db.clientes.find({'email':usuario['email']}).count()
    numeroDB = mongo.db.clientes.find({'telefono':usuario['telefono']}).count()
    numeroNombre = mongo.db.clientes.find({'nombre':usuario['nombre']}).count()
    
    if emailDB > 0 or numeroDB > 0 or numeroNombre > 0:
        msj_error = 'El nombre, mail o numero telefonico ya ah sido registrado, intenta con alguno diferente o inicia sesión '
        flash(msj_error)
        return redirect('/clientes/registro')
    #insertando el nuevo usuario
    id_user = mongo.db.clientes.insert(usuario)
    
    #capturamos el tipo de usuario para manejarlo segun que cosas
    session['cliente'] = str(id_user)

    return redirect('/panel')


@clientes.route('/login')
def login_template():
    return render_template('/clientes/login.html')

@clientes.route('/login',methods = ['POST'])
def login_post():
    usuario = {
        'email': request.form['email'],
        'password': encriptar(request.form['password'])
    }

    emailDB = mongo.db.clientes.find({'email':usuario['email']}).count()
    if emailDB == 1:
        query = {
            '$and':[
                {'email':usuario['email']},
                {'password':usuario['password']}
            ]
        }
        password_validated = mongo.db.clientes.find(query).count()

        if password_validated == 0:
            msj_error = 'Contraseña incorrecta'
            flash(msj_error)
            return redirect('/clientes/login')
        
        user_id = mongo.db.clientes.find_one({'email':usuario['email']})
        #creamos la sesion
        session['cliente'] = str(user_id['_id'])  

        return redirect('/panel')
    else:
        msj_error = 'Aún no estas registrado'
        flash(msj_error)
        return redirect('/clientes/login')




@clientes.route('/logout')
def logout_cliente():
    session.pop("cliente",None)
    return redirect('/clientes/login')



# ::::::::::::::::: Recuperacion de correo contraseña :::::::::::::::::::::::

@clientes.route('/forget/password')
def forget_password():
    return render_template('clientes/recuperar_password.html')

@clientes.route('/send/mail',methods = ['POST'])
def send_mail():
    
    mail = request.form['email']
    res = mongo.db.clientes.find({'email':mail}).count()

    if res:
        cliente = mongo.db.clientes.find_one({'email':mail})
        destino = cliente['email']
        codigo = cliente['password']
        enviar_email(destino,codigo)

        #guardamos el id en una session para utilizarlo y cambiar el password 
        id = str(cliente['_id'])
        session["restore"] = id
        return redirect('/clientes/restore/password')

    else:
        msj_error = 'email no registrado'
        flash(msj_error)
        return redirect('/clientes/forget/password')



@clientes.route('/restore/password')
def restore_password():
    return render_template('clientes/restore_password.html')

@clientes.route('/restore/password',methods = ['POST'])
def restore_password_post():
    
    codigo = request.form['codigo']
    password = request.form['password']
    repassword = request.form['repassword']
    
    msj = " "

    if len(password) < 5:
        msj = "contraseña muy corta, intente con una diferente"
        flash(msj)
        return redirect('/clientes/restore/password')

    if not password == repassword:
        msj = "contraseñas no coinciden, intente de nuevo"
        flash(msj)
        
        return redirect('/clientes/restore/password')
    
    print('primer filtro fromted')

    cliente = mongo.db.clientes.find_one({'_id':ObjectId(session['restore'])})
    
    if codigo == cliente['password']:

        id = session['restore']

        mongo.db.clientes.update_one(
            {
                '_id': ObjectId(id)
            },
            {
                '$set':{
                    'password':encriptar(password)
            }}
        )

        session.pop("restore",None)

        session["cliente"] = id 

        return redirect('/panel')

    else:
        msj = "Codigo de seguridad incorrecto"
        flash(msj)
        
        return redirect('/clientes/restore/password')

#Modificaciones en el perfil de usuario

#modificacion de los datos del perfil
@clientes.route('/update',methods = ['POST'])
def update():

    dato = {
      'nombre':request.json['nombre'],
      'domicilio':request.json['domicilio'],
      'telefono':request.json['telefono'],
    }

    id = session['cliente']

    #actualizamos la datos
    mongo.db.clientes.update_one(

        {
            '_id': ObjectId(id)
        },
      {
         '$set':{
            'nombre': dato['nombre'],
            'domicilio': dato['domicilio'],
            'telefono' : dato['telefono']
      }}
    )

    return "updated data"

#modificacion de foto de perfil
@clientes.route('/update/foto',methods = ['POST'])
def update_foto():

    foto = request.json['foto']
    foto_key = request.json['foto_key']

    id = session['cliente']

    #eliminamos la foto que se tenia anterior mente
    user = mongo.db.clientes.find_one({'_id': ObjectId(id)})
    if not user['foto_key'] == '':
        destroy_image(user['foto_key'])

    #actualizamos la foto
    mongo.db.clientes.update_one(

        {
            '_id': ObjectId(id)
        },
      {
         '$set':{
            'foto': foto,
            'foto_key': foto_key,
      }}
    )

    return "updated file"

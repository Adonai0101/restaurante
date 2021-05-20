from flask import Blueprint,render_template,redirect,request,flash,session
from database import mongo

from bson import json_util
from bson.objectid import ObjectId

from admin_cloudinary import *

from tools import *
from send_mail import *

usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/')
def index():
    return 'usuarios'


@usuarios.route("/login")
def login_template():
    return render_template('login.html')

@usuarios.route("/login",methods = ['POST'])
def login_check():
    usuario = {
        'email': request.form['email'],
        'password': encriptar(request.form['password'])
    }

    emailDB = mongo.db.usuarios.find({'email':usuario['email']}).count()
    if emailDB == 1:
        query = {
            '$and':[
                {'email':usuario['email']},
                {'password':usuario['password']}
            ]
        }
        password_validated = mongo.db.usuarios.find(query).count()

        if password_validated == 0:
            msj_error = 'Contraseña incorrecta'
            flash(msj_error)
            return redirect('/usuarios/login')
        
        user_id = mongo.db.usuarios.find_one({'email':usuario['email']})
        #creamos la sesion
        session["usuario"] = str(user_id['_id'])  

        return redirect('/dashboard')
    else:
        msj_error = 'Aún no estas registrado'
        flash(msj_error)
        return redirect('/usuarios/login')

#logout
@usuarios.route('/logout')
def logout():
    session.pop("usuario",None)
    session.pop("vendedor",None)
    session.pop("cliente",None)
    return redirect('/usuarios/login')

# Registro de usuarios
@usuarios.route('/registro')
def registro():
    return render_template('registro.html')

@usuarios.route('/registro',methods = ['POST'])
def registrar_usuario():
    usuario = {
        'nombre' : request.form['nombre'],
        'domicilio' : request.form['domicilio'],
        'telefono' : request.form['telefono'],
        'email' : request.form['email'],
        'password' : encriptar( request.form['password']),
        'foto':'../static/img/header-test.jpg',
        'foto_key':'',
        'facebook' : '',
        'instagram' : '',
        'tiktok' : ''
    }

    #Validacion de campos vacios
    if len(usuario['nombre']) < 5:
        msj_error = 'Ingresa un nombre valido'
        flash(msj_error)
        return redirect('/usuarios/registro')

    if len(usuario['domicilio']) < 5:
        msj_error = 'Ingresa un domicilio valido'
        flash(msj_error)
        return redirect('/usuarios/registro')

    if len(usuario['password']) < 5:
        msj_error = 'usa una contraseña que contenga al menos 5 letras o números'
        flash(msj_error)
        return redirect('/usuarios/registro')

    #Pequeña validacion para no duplicar telefonos, emails y nombres de negocios
    if not email_valido(usuario['email']):
        msj_error = 'email invalido, intenta nuevamente'
        flash(msj_error)
        return redirect('/usuarios/registro')
        
    if not numero_valido(usuario['telefono'],10):
        msj_error = 'Númerode telefono invalido, intenta nuevamente'
        flash(msj_error)
        return redirect('/usuarios/registro')

    #Validando que no este nada registrado
    emailDB = mongo.db.usuarios.find({'email':usuario['email']}).count()
    numeroDB = mongo.db.usuarios.find({'telefono':usuario['telefono']}).count()
    numeroNombre = mongo.db.usuarios.find({'nombre':usuario['nombre']}).count()
    
    if emailDB > 0 or numeroDB > 0 or numeroNombre > 0:
        msj_error = 'El nombre, mail o numero telefonico ya ah sido registrado, intenta con alguno diferente o inicia sesión '
        flash(msj_error)
        return redirect('/usuarios/registro')
    #insertando el nuevo usuario
    id_user = mongo.db.usuarios.insert(usuario)
    
    #capturamos el tipo de usuario para manejarlo segun que cosas
    session['usuario'] = str(id_user)

    return redirect('/dashboard')


#actualizando al usuario

#actuzlizando la foto de perfil del usuario

@usuarios.route('/update_foto',methods = ['POST'])
def user_update_foto():
    usuario ={
        'foto':request.json['foto'],
        'foto_key':request.json['foto_key']
    }

    #aliminamos la foto que se tenia anterior mente
    user = mongo.db.usuarios.find_one({'_id': ObjectId(session['usuario'])})
    if not user['foto_key'] == '':
        destroy_image(user['foto_key'])

    #actualizamos la foto
    mongo.db.usuarios.update_one(

        {
            '_id': ObjectId(session['usuario'])
        },
      {
         '$set':{
            'foto': usuario['foto'],
            'foto_key': usuario['foto_key'],
      }}
    )
    return 'foto actuzalizada'

#actuzlizando informacion del usuario
@usuarios.route('/update'  , methods = ['POST'])
def user_update():

    usuario = {
        'nombre' : request.form['usuario'],
        'domicilio' : request.form['domicilio'],
        'telefono' : request.form['telefono'],
        'facebook' : request.form['facebook'],
        'instagram' : request.form['instagram'],
        'tiktok' : request.form['tiktok']
    }

    temp = mongo.db.usuarios.find_one({'_id':ObjectId(session['usuario'])})

    if not temp['nombre'] == usuario['nombre']:

        numeroNombre = mongo.db.usuarios.find({'nombre':usuario['nombre']}).count()
        if numeroNombre > 0:
            msj_error = 'El nombre ya ah sido registrado, intenta con alguno diferente '
            flash(msj_error)
            return redirect('/dashboard')
    
    print("donde estan perros")
    print(usuario['facebook'])
    mongo.db.usuarios.update_one(
      {
         '_id': ObjectId(session['usuario'])
      },
      {
         '$set':{
            'nombre': usuario['nombre'],
            'domicilio': usuario['domicilio'],
            'telefono': usuario['telefono'],
            'facebook': usuario['facebook'],
            'instagram': usuario['instagram'],
            'tiktok': usuario['tiktok']
      }}
    )
    return redirect('/dashboard')


#formularios para mostrar y validar el correo
@usuarios.route('/password')
def olvide_password():
    return render_template('cambiar_password.html')

@usuarios.route('/password',methods = ['POST'])
def restaurar_password():
    mail = request.form['email']

    mail_exist = mongo.db.usuarios.find({'email':mail}).count()
    
    if mail_exist == 0:
        msj_error = 'Correo electrónico no esta registrado, intente con uno diferente'
        flash(msj_error)
        return redirect('/usuarios/password')
    else:
        #enviamos el codigo de confirmacion
        usuario = mongo.db.usuarios.find_one({'email':mail})
        
        destino = usuario['email']
        codigo = usuario['password']
        
        enviar_email(destino,codigo)

        #guardamos el id en una session para utilizarlo y cambiar el password 
  
        id = str(usuario['_id'])
        session["restore"] = id
        
        return redirect('/usuarios/updatepassword')

@usuarios.route('/updatepassword')
def cambiar_password():
    return render_template('update_password.html')

@usuarios.route('/updatepassword',methods = ['POST'])
def cambiar_password_post():

    codigo = request.form['codigo']
    password = request.form['password']
    repassword = request.form['repassword']

    msj = " "

    if len(password) < 5:
        msj = "contraseña muy corta, intente con una diferente"
        flash(msj)
        return redirect('/usuarios/updatepassword')

    if not password == repassword:
        msj = "contraseñas no coinciden, intente de nuevo"
        flash(msj)
        
        return redirect('/usuarios/updatepassword')

    usuario = mongo.db.usuarios.find_one({'_id':ObjectId(session['restore'])})
    
    if codigo == usuario['password']:

        id = session['restore']

        mongo.db.usuarios.update_one(
            {
                '_id': ObjectId(id)
            },
            {
                '$set':{
                    'password':encriptar(password)
            }}
        )

        session.pop("restore",None)

        session["usuario"] = id 

        return redirect('/dashboard')


    else:
        msj = "Codigo de seguridad incorrecto"
        flash(msj)
        
        return redirect('/usuarios/updatepassword')

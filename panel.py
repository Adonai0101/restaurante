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

panel = Blueprint('panel',__name__)


@panel.route('/')
def index():
    if 'cliente' in session:
        
        return render_template('clientes/inicio.html')
    else:
        print(session)
        return redirect('/clientes/login')


@panel.route('/perfil')
def perfil():
    if 'cliente' in session:
        print("a su mecha" , session['cliente'])
        return render_template('clientes/perfil.html')
    else:
        print(session)
        return redirect('/clientes/login')
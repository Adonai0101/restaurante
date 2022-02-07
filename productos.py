from flask import Blueprint,jsonify, request, Response,session

from bson import json_util
from bson.objectid import ObjectId

#Database
from database import mongo

from admin_cloudinary import *

productos = Blueprint('productos',__name__)

#Get
@productos.route('/')
def get_products():
   query = {'usuario':session['usuario']}
   productos = mongo.db.productos.find(query)
   response = json_util.dumps(productos)
   print("este es el id del vendedor en turno XD")
   print(session["usuario"])
   return Response(response, mimetype="application/json")



@productos.route('/<id>')
def get_product(id):
   producto = mongo.db.productos.find_one()
   response = json_util.dumps(producto)
   return Response(response, mimetype="application/json")


#POST
@productos.route('/',methods = ['POST'])
def add_product():
   
   print('se resivio desde test')
   dato = {
      'nombre':request.json['nombre'],
      'categoria':request.json['categoria'],
      'fotos':request.json['fotos'],
      'publicID':request.json['publicID'],
      'ingredientes':request.json['ingredientes'],
      'precio':request.json['precio'],
      'user_id':session["usuario"],
   }
   mongo.db.productos.insert_one(dato)
   return {"msj":"resivido"}

#Delete
#elimina todo un producto
@productos.route('/delete', methods=['POST'])
def delete_product():

   #obtenemos el id
   dato = {
      'id':request.json['id']
   }
   id = dato['id']
   print(id)
  
   #Eliminamos todos los registros de las imagenes
   producto = mongo.db.productos.find_one({'_id': ObjectId(id)})

   keys = producto['publicID']

   for key in keys:
      destroy_image(key)
   
   #Eliminamos el registro
   mongo.db.productos.delete_one({'_id': ObjectId(id)})
   
   return "works"
   

#Update
@productos.route('/<id>',methods = ['PUT'])
def update_product(id):
   print("actualizando producto")

   nombre = request.json['nombre']
   categoria = request.json['categoria']
   fotos = request.json['fotos']
   descripcion = request.json['descripcion']
   precio = request.json['precio']

   mongo.db.productos.update_one(
      {
         '_id': ObjectId(id)
      },
      {
         '$set':{
            'nombre':nombre,
            'categoria':categoria,
            'fotos':fotos,
            'descripcion':descripcion,
            'precio':precio,
            'descuento':descuento,
            'cantidad':cantidad,
            'user_id':session["usuario"],
      }}
   )

   response = jsonify({'message': 'Producto ' + id + ' Updated Successfully'})
   return response


#categorias de productos
@productos.route('/categorias')
def categorias():

   query = {'user_id':str(session['usuario'])}
   productos = mongo.db.productos.find(query)
   categorias = []

   for x in productos:
      temp = {
         'categoria' : x['categoria'],
         'foto' : x['fotos']
      }
      categorias.append(temp)
   print(categorias)
   return jsonify(categorias)


"""
   este codigop es para editar un solo producto
"""

#para eliminar una sola imagen de producto
@productos.route('/deleteimg',methods = ['POST'] )
def delete_img():

   filename = request.json['filename']
   id = request.json['id']
   key = request.json['publicID']

   producto = mongo.db.productos.find_one({'_id':ObjectId(id)})
   
   fotos = producto['fotos']
   fotos.remove(filename)

   publicID = producto['publicID']
   publicID.remove(key)

   mongo.db.productos.update_one({
        '_id':ObjectId(id)
    },
    {
        '$set':{
            'fotos':fotos,
            'publicID':publicID
        } 
    })

   #aqui faltaria eliminarlas de cloudinary
   destroy_image(key)
   
   return "imagen eliminada"

#agregar mas imagenes
@productos.route('/addimages',methods = ['POST'])
def add_img():
   print('se hizo el post')
   id = request.json['id']
   nuevas_fotos = request.json['fotos']
   nueva_key = request.json['publicID']

   producto = mongo.db.productos.find_one({'_id':ObjectId(id)})
   
   fotos = producto['fotos']
   fotos = nuevas_fotos + fotos

   key = producto['publicID']
   key = nueva_key + key

   mongo.db.productos.update_one({
        '_id':ObjectId(id)
    },
    {
        '$set':{
            'fotos':fotos,
            'publicID': key
        } 
    })

   return "se añidieron nuevas imagenes"

@productos.route('/updateinfo',methods = ['POST'])
def update_info():

   dato = {
      'id':request.json['id'],
      'nombre':request.json['nombre'],
      'categoria':request.json['categoria'],
      'ingredientes':request.json['ingredientes'],
      'precio':request.json['precio'],
   }
   mongo.db.productos.update_one(
      {
         '_id': ObjectId(dato['id'])
      },
      {
         '$set':{
            'nombre':dato['nombre'],
            'categoria':dato['categoria'],
            'ingredientes':dato['ingredientes'],
            'precio':dato['precio']
      }}
   )

   print('se hizo el post')
   print(dato)

   return "updated"

@productos.route('/test/<id>')
def test_info(id):

   producto = mongo.db.productos.find({'_id':ObjectId(id)})
   response = json_util.dumps(producto)
   return Response(response, mimetype="application/json")

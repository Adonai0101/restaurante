import cloudinary
import cloudinary.uploader
import cloudinary.api

#variables de entorno
from decouple import config

cloudinary.config( 
  cloud_name = config('CLOUD_NAME'), 
  api_key = config('API_KEY'), 
  api_secret = config('API_SECRET') 
)


def destroy_image(key):

  rest = cloudinary.uploader.destroy(key)
  print("imagen eliminada")


from validate_email import validate_email

import datetime

def obtener_fecha():
    now = datetime.datetime.utcnow()
    return now

def proximo_pago(fecha):
    nueva_fecha = fecha + datetime.timedelta(days = 30)
    return nueva_fecha

def email_valido(email):
    if validate_email(email):
        return True
    else:
        return False


def numero_valido(numero,longitud):
    try:
        entero = int(numero)
        if len(numero) == longitud:
            return True
        return False
    except ValueError:
        return False

def encriptar(cad):
    msj = ""
    for i in cad:
        temp = ord(i) + 10
        msj  = msj + chr(temp)
    return msj

def desencriptar(cad):
    msj = ""
    for i in cad:
        temp = ord(i) - 1
        msj  = msj + chr(temp)
    return msj 

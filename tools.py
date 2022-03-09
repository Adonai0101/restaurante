from tokenize import Double
from validate_email import validate_email

import datetime


def obtener_fecha():
    now = datetime.datetime.utcnow()
    format = now.strftime('%d/%m/%Y')
    return format

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


def dia_semana():
    x = datetime.datetime.now()
    dias = {
        'MONDAY':'Lunes',
        'TUESDAY':'Martes',
        'WEDNESDAY':'Miercoles',
        'THURSDAY':'Jueves',
        'FRIDAY':'Viernes',
        'SATURDAY':'Sabado',
        'SUNDAY':'Domingo'
    }
    fecha = datetime.date(x.year, x.month, x.day)
    dia = dias[fecha.strftime('%A').upper()]
    return dia

def hora_actual():
    #del punto decimal a la izquierda son las horas
    #y del punto decimal a la derecha son los minutos
    now = datetime.datetime.now()
    time = str(now.hour) + '.' + str(now.minute)
    time = float(time)
    return time


def convertir_hora(cad):
    hora = cad.replace(':', '.')
    hora = float(hora)
    return  hora


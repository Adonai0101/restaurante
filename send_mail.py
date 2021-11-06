import smtplib

#variables de entorno
from decouple import config

def enviar_email(destino,codigo):
    asunto = 'Solicitud de cambio de password, de "Menu Zapotlan" '
    mensaje = "Tu codigo es:\n " + codigo

    mensaje = 'Subject:{}\n\n{}'.format(asunto,mensaje)

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()

    user = 'localdev2000@gmail.com'
    password = config('PASSWORD_MAIL')
    server.login(user,password)

    server.sendmail(user,destino,mensaje)

    server.quit()
    print("sended")


#testeando metodo
#destino = 'pampire1995@gmail.com'
#enviar_email(destino,'123')

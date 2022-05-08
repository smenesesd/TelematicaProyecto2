import os, sys
p = os.path.abspath('D:\TelematicaProyecto2')
sys.path.insert(1, p)
import constants

def get_tipo(archivo):  
    if archivo.endswith('.jpg'):
        tipo = "image/jpg"
    elif archivo.endswith('.css'):
        tipo = "text/css"
    elif archivo.endswith('.pdf'):
        tipo = "application/pdf"
    else:
        tipo = "text/html"
    return tipo

def get_object(address):
    direction = address.split('?')[0]
    if direction == '/' or direction == '/home':
        archivo = 'D:/TelematicaProyecto2/ServerMet/index.html'
    else:
        archivo = 'D:/TelematicaProyecto2/ServerMet'+ direction
    try:
        file = open(archivo, 'rb')
        response = file.read()
        file.close()
        tipo_archivo = get_tipo(archivo)
        header = constants.OK200+'Content-Type: '+str(tipo_archivo)+'\n\n'
    except Exception as e:
        print("Ocurrio un error")
        header = constants.Error400
        response = "".encode(constants.ENCONDING_FORMAT)
    final_response = header.encode(constants.ENCONDING_FORMAT)
    final_response += response
    return final_response


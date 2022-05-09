from dataclasses import replace
import os, sys
p = os.path.abspath('D:\TelematicaProyecto2')
sys.path.insert(1, p)
import constants
import re
from pathlib import Path
BASE_DIR = Path(__file__).parent.absolute()


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
        archivo = str(BASE_DIR /'index.html')
        #archivo = replace('\.','/')
        archivo = re.sub("[\\\]", "/", archivo)
        print(archivo)
    else:
        direction = direction[1:]
        archivo = str(BASE_DIR / direction)
        print(archivo)
        narchivo = re.sub("[\\\]", "/", archivo)
        print(narchivo)
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

get_object("/Recursos/imagenes/equipo.jpg")

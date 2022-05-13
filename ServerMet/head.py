import os
import constants
import re
from pathlib import Path
BASE_DIR = Path(__file__).parent.absolute()         #Tomamos el directorio base para obtener los recursos


def get_tipo(archivo):                              #Seleccion de tipo de archivo para encabezado
    if archivo.endswith('.jpg') or archivo.endswith('.jpeg'):
        tipo = "image/jpeg"
    if archivo.endswith('.png'):
        tipo = "image/png"
    elif archivo.endswith('.css'):
        tipo = "text/css"
    elif archivo.endswith('.pdf'):
        tipo = "application/pdf"
    else:
        tipo = "text/html"
    return tipo

def get_head(address):                                #Metodo para retornar un recurso
    direction = address.split('?')[0]                   #Tomamos todo menos lo que hay despues del ?
    if direction == '/' or direction == '/home':        #En caso de que sea directorio base o /home
        archivo = str(BASE_DIR /'index.html')           #Archivo va a ser directorio base + index.html
        archivo = re.sub("[\\\]", "/", archivo)         #Se cambia los \ por /
    else:
        direction = direction[1:]                       #En caso de que no sea el index.html
        archivo = str(BASE_DIR / direction)             #Directorio base + la direccion que nos mandan
        archivo = re.sub("[\\\]", "/", archivo)        #Se cambia el \ por el /
    if os.path.exists(archivo):
        tipo_archivo = get_tipo(archivo)
        header = constants.OK200+'Content-Type: '+str(tipo_archivo)+'\r\n\r\n'
    else:
        header = constants.Error404
    final_response = header.encode(constants.ENCONDING_FORMAT)              #Se codifica el encabezado y la respuesta
    return final_response                                                   #Se retorna la respuesta

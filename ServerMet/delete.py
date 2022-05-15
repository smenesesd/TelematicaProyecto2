import os
import constants
import re
from pathlib import Path
BASE_DIR = Path(__file__).parent.absolute()         #Tomamos el directorio base para obtener los recursos

def get_direction(direccion):
    direccion = direccion.split('?')[0]
    if direccion == '/' or direccion == '/home':
        archivo = str(BASE_DIR /'index.html')           #Archivo va a ser directorio base + index.html
        archivo = re.sub("[\\\]", "/", archivo)         #Se cambia los \ por /
    else:
        direccion = direccion[1:]                       #En caso de que no sea el index.html
        archivo = str(BASE_DIR / direccion)             #Directorio base + la direccion que nos mandan
        archivo = re.sub("[\\\]", "/", archivo) 
    return archivo 

def delete_object(header):                                  #Metodo para eliminar un archivo
    nombre = str(header[1])
    direccion = get_direction(nombre)                       #Buscamos en que direccion se encuentra dicho archivo
    print(direccion)
    try:
        os.remove(direccion)                                #Tratamos de eliminar el archvio
        header = str(constants.OK200+constants.Okdelete)    #Preparamos header de respuesta en caso de eliminarse correctamente
    except Exception as e:
        header = str(constants.Error400)                    #Header en caso de haber ocurrido un error
    final_response = header
    return final_response                                   #Se retorna mensaje de respuesta



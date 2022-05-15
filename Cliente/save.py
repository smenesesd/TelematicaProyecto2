from audioop import add
import constants
import re
from pathlib import Path
BASE_DIR = Path(__file__).parent.absolute()         #Tomamos el directorio base para obtener los recursos



def get_direction(archivo):                              #Seleccion de tipo de archivo para encabezado
    if archivo.endswith('.jpg') or archivo.endswith('.jpeg') or archivo.endswith('.png'):
        fichero = 'Recursos/imagenes/'+archivo
        tipo = str(BASE_DIR /fichero)  
    elif archivo.endswith('.css'):
        fichero = 'Recursos/css/'+archivo
        tipo = str(BASE_DIR /fichero)  
    elif archivo.endswith('.pdf'):
        fichero = 'Recursos/pdf/'+archivo
        tipo = str(BASE_DIR /fichero)  
    else:
        fichero = 'Recursos/documentos/'+archivo
        tipo = str(BASE_DIR /fichero) 
        tipo = re.sub("[\\\]", "/", tipo) 
    return tipo

def html_parser(contenido, address, port):
    return

def save_object(encabezado , contenido, address, port):
    type = ""
    direction = encabezado.split('?')[0]
    direction = direction.split('/')
    direccion = get_direction(direction[-1])
    print(direccion)
    cont = b''
    if len(contenido)>2:
        for i in range(len(contenido)):
            if i == 0: 
                continue
            else:
                if i < len(contenido)-1:
                    cont += contenido[i]
                else:
                    cont += contenido[i]
    else:
        cont = contenido[1]
    try:
        print(cont)
        file = open(direccion, 'wb')
        file.write(cont)
        file.close()
        #if direccion.endswith(".html"):
            #html_parser(cont, address, port)
    except Exception as e:
        print("Ocurrio un error")

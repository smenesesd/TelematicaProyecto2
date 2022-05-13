import constants
import re
from pathlib import Path
BASE_DIR = Path(__file__).parent.absolute()         #Tomamos el directorio base para obtener los recursos



def get_direction(archivo):                              #Seleccion de tipo de archivo para encabezado
    if archivo.endswith('.jpg'):
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

def save_object(encabezado , contenido):
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
                    cont += contenido[i]+b'\r\n\r\n'
                else:
                    cont += contenido[i]
    else:
        cont = contenido[1]
    try:
        print(cont)
        file = open(direccion, 'wb')
        file.write(cont)
        file.close()
    except Exception as e:
        print("Ocurrio un error")

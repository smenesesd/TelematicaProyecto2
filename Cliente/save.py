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
        print(tipo)
        tipo = re.sub("[\\\]", "/", tipo) 
    return tipo

def save_object(encabezado , contenido):
    type = ""
    encabezado = encabezado [1:]
    direccion = str(BASE_DIR/encabezado)
    direccion = re.sub("[\\\]", "/", direccion) 
    cont = b''
    print(direccion)

    if len(contenido)>2:
        for i in range(len(contenido)):
            if i == 0: 
                continue
            else:
                cont += contenido[i]+b'/n/n'
    else:
        cont = contenido[1]
    print(cont)  
    try:
        file = open(direccion, 'wb')
        file.write(cont)
        file.close()
    except Exception as e:
        print("Ocurrio un error")

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


def put_object(remote_command):
    tipo = ""
    documento=""
    nombre = str(remote_command[1])
    nombre = nombre[1:]
    print(nombre)
    j=0
    for i in range(len(remote_command)):
        if remote_command[i] == "Content-type:":
            tipo = remote_command[i+1]
            print(tipo)
        elif remote_command[i]=="\n" and i!=len(remote_command):
            j = i+1
            for j in range(j,len(remote_command),1):
                documento += str(remote_command[j].descode+" ")
            print(documento)
            break
    try:
        direccion = get_direction(nombre)
        archivo = open(direccion, 'w')
        archivo.write(documento)
        archivo.close()
        header = constants.OK201+direccion
    except:
        header = constants.Error409
    final_response = header.encode(constants.ENCONDING_FORMAT)  
    return final_response

imagen = open('D:/TelematicaProyecto2/ServerMet/Recursos/imagenes/max.jpeg','rb')
img = imagen.read()
imagen.close()

lista = ['PUT','/nuevo.jpg', 'HTTP/1.1\n', 'Host:', 'ejemplo.com', 'Content-type:', 'text/html\n',
'\n',img]

put_object(lista)
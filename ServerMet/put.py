import constants
import re
from pathlib import Path
BASE_DIR = Path(__file__).parent.absolute()         #Tomamos el directorio base para obtener los recursos

def get_direction(archivo):                                                                 #Seleccion la direccion correspondiente al tipo de archivo
    if archivo.endswith('.jpg') or archivo.endswith('.jpeg') or archivo.endswith('.png'):   #En caso de ser una imagen
        fichero = 'Recursos/imagenes/'+archivo
        tipo = str(BASE_DIR /fichero)  
    elif archivo.endswith('.css'):                                                          #En caso de que sea css
        fichero = 'Recursos/css/'+archivo
        tipo = str(BASE_DIR /fichero)  
    elif archivo.endswith('.pdf'):                                                          #En caso de ser pdf
        fichero = 'Recursos/pdf/'+archivo
        tipo = str(BASE_DIR /fichero)  
    else:
        fichero = 'Recursos/documentos/'+archivo                                            #En caso de ser otro tipo de archivo
        tipo = str(BASE_DIR /fichero) 
        print(tipo)
    tipo = re.sub("[\\\]", "/", tipo) 
    return tipo                                                                             #Retornamos la direccion donde va a ser almacneado el archivo


def put_object(header, remote_string):                              #Metodo para realizar un put
    nombre = str(header[1])                                         #Nombre del archivo con direccion
    nombre = nombre[1:]
    direccion = get_direction(nombre)
    cont = b''
    if len(remote_string)>2:                                        #En caso de que el contenido tenga mas de dos argumentos
        for i in range(len(remote_string)):
            if i == 0:
                continue
            else:
                cont += remote_string[i]+b'\r\n\r\n'                    #Volvemos a formar el contenido en caso de haberlo dividido
    else:
        cont = remote_string[1]
    
    try:
        archivo = open(direccion, 'wb')                             #Abrimos el archvio, sea para actualizar o para crear
        archivo.write(cont)
        archivo.close()
        header = constants.OK201+direccion                          #En caso de realizar el proceso con exito, devolvemos el mensaje de confirmacion
    except:                 
        header = constants.Error409                                 #En caso de un error, enviamos un 409
    final_response = header.encode(constants.ENCONDING_FORMAT)  
    return final_response                                           #Retornamos la respuesta final


directorio = str(BASE_DIR / 'Recursos/documentos/nuevo.html')
directorio = re.sub("[\\\]", "/", directorio) 
imagen = open(directorio,'rb')
img = imagen.read()
imagen.close()
img = ['PUT /nuevo.pg',img]

lista = ['PUT','/verstapen.html', 'HTTP/1.1\n', 'Host:', 'ejemplo.com', 'Content-type:', 'image/png\n',
'\n']

put_object(lista,img)
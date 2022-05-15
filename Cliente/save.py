import constants
from bs4 import BeautifulSoup
import re
import socket
from pathlib import Path
BASE_DIR = Path(__file__).parent.absolute()         #Tomamos el directorio base para obtener los recursos



def get_direction(archivo):                                                                 #Busqueda de directorio correspontiente al tipo de archivo
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

def parser(direccion, address, port, host):                                                     #Metodo parser
    direcciones = []
    with open(direccion,'r') as archivo:                                                        #Abrimos el archivo en modo de lectura
        soup = BeautifulSoup(archivo, "html.parser")                                            #Utilizamos la libreria BeautifulSoup para leer el archvio y parsear
        imagenes_encontradas = soup.findAll('img')                                              #Buscamos la etiquetas de imagenes
        for imagen in imagenes_encontradas:                                                     #Por cada etiqueta encontrada, almacenamos la etiqueta 
            direcciones.append(imagen['src'])
    if len(direcciones) > 0:                                                                    #Recorremos las etiquetas encontradas
        for i in direcciones:                                                                   #Para cada direccion vamos a realizar un peticion al servidor para que este nos devuelva el recuros
            client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)                    #Abrimos un nuevo socket
            client_socket.connect((address,port))                                               #Colocamos la direccion y puerto correspondiente
            request = 'GET' + ' ' + '/' + i + ' ' + 'HTTP/1.1\r\nHost: ' + host + '\r\n\r\n'    #Creamos la peticion a ser enviada
            client_socket.send(request.encode(constants.ENCONDING_FORMAT))                      #Codificamos y enviamos
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)                      #Leemos la response entrante
            while True:                                                                         #En caso de que el archivo este partido, creamos el bucle para recibir los datos
                    data_received_add = client_socket.recv(constants.RECV_BUFFER_SIZE)      
                    if not data_received_add or data_received_add == b'':
                        break
                    data_received+= data_received_add
            response = data_received.split(b'\r\n\r\n',1)                                       #dividmos la response en header y contenido
            header = str(response[0].decode(constants.ENCONDING_FORMAT))                        #Decodificamos el header
            print('\n',header)                                                                  #Imprimimos el header de respuesta
            status_code = header.split()    
            status_code = status_code[1]
            if(status_code == '200'):                                                           #En caso de que el mensaje de respuesta sea un 200 debemos almacenar le archivo entrante
                save_object(i,response,address,port, host)
                print("-----------------------------------------------------")
            else:
                print(response[1].decode(constants.ENCONDING_FORMAT))                           #En caso de no haber encontrado el archivo, imprimimos el mensaje de repuesta
            client_socket.close()


def save_object(encabezado , contenido, address, port, host):   #Metodo para guardar un archvio entrante al cliente
    type = ""
    if encabezado == "/":                               #En caso de ser / se cambia el archivo por /index.html
        encabezado = "/index.html"
    direction = encabezado.split('?')[0]
    direction = direction.split('/')                    #Tomamos el encabezado y lo dividimos por / para obtener el nombre del archivo
    direccion = get_direction(direction[-1])            #Buscamos la direccion con el metodo get_direccion y el nombre del archivo
    cont = b''
    if len(contenido)>2:                                #En caso de que el contenido sea mayor a 2, quiere decir que nuestro archivo esta partido en varias partes
        for i in range(len(contenido)):
            if i == 0:                                  #La primera posicion de contenido contiene el encabezado y este no se almacena
                continue
            else:
                if i < len(contenido)-1:                #El resto de partes las juntamos con el contenido
                    cont += contenido[i]
                else:
                    cont += contenido[i]
    else:                                               #En caso de que el archivo este completo, lo almacenamos directmente en la variable cont
        cont = contenido[1]
    try:
        file = open(direccion, 'wb')                    #Intentemos escribir el archivo dentro de nuestro directorio
        file.write(cont)        
        file.close()
        if direccion.endswith(".html"):                 #En caso de que sea un archivo html, llamamos el metodo parser para para parsearlo
            parser(direccion,address, port, host)       #Este netodo recibe la direccion donde se escribio, la direccion del servidor, el puerto y el host
    except Exception as e:
        print("Ocurrio un error")

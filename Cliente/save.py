import constants
from bs4 import BeautifulSoup
import re
import socket
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

def parser(direccion, address, port, host):
    direcciones = []
    with open(direccion,'r') as archivo:
        soup = BeautifulSoup(archivo, "html.parser")
        imagenes_encontradas = soup.findAll('img')
        for imagen in imagenes_encontradas:
            direcciones.append(imagen['src'])
    if len(direcciones) > 0:
        for i in direcciones:
            client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #AF_INET define el tipo de direccion (ipv4), y modo TCP
            client_socket.connect((address,port)) 
            request = 'GET' + ' ' + '/' + i + ' ' + 'HTTP/1.1\r\nHost: ' + host + '\r\n\r\n'
            client_socket.send(request.encode(constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            while True:
                    data_received_add = client_socket.recv(constants.RECV_BUFFER_SIZE)
                    if not data_received_add or data_received_add == b'':
                        break
                    data_received+= data_received_add
            response = data_received.split(b'\r\n\r\n',1)
            header = str(response[0].decode(constants.ENCONDING_FORMAT))
            print('\n',header)
            status_code = header.split()
            status_code = status_code[1]
            if(status_code == '200'):
                save_object(i,response,address,port, host)
                print("-----------------------------------------------------")
            else:
                print(response[1].decode(constants.ENCONDING_FORMAT))
            client_socket.close()


def save_object(encabezado , contenido, address, port, host):
    type = ""
    if encabezado == "/":
        encabezado = "/index.html"
    direction = encabezado.split('?')[0]
    direction = direction.split('/')
    direccion = get_direction(direction[-1])
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
        file = open(direccion, 'wb')
        file.write(cont)
        file.close()
        if direccion.endswith(".html"):
            parser(direccion,address, port, host)
    except Exception as e:
        print("Ocurrio un error")

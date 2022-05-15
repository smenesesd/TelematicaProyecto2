# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # TCP-Socket Client
    # David Gomez Correa - Samuel Meneses Diaz
# ********************************************************************************************

#Import libraries for networking communication...

from os import link
import re
import socket
from urllib import response

from bs4 import BeautifulSoup
import constants
import time
from Cliente import save, put_client


lista_metodos_aceptados = [constants.GET, constants.HEAD, constants.DELETE, constants.PUT, constants.QUIT]
exp_reg_direccion = re.compile('([/\w]+).(\w+)') 
exp_reg_URL = re.compile('([\w]+)://([\w+\.]+)([/\w|-]+).(\w+)') 


def validador(encabezado):
    encabezado = encabezado.split()
    if encabezado[0] in lista_metodos_aceptados:
        if exp_reg_direccion.match(encabezado[1]) or exp_reg_URL.match(encabezado[1]):
            if encabezado[2] == "HTTP/1.1":
                return True
    elif encabezado[0]=='/':
        return True
    return False
        

def main(direccion, port):
    try:
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #AF_INET define el tipo de direccion (ipv4), y modo TCP
        client_socket.connect((direccion,port))                 #Es donde el client se conectara al servidor
        local_tuple = client_socket.getsockname()
        print('Connected to the server from:', local_tuple)
        command_to_send = ""
        while command_to_send != constants.QUIT :
            print('\nEnter \"QUIT\" to exit')
            print('Input commands:')
            print('QUIT, GET, POST, HEAD, DELETE\n')
            command_to_send = input()
            if validador(command_to_send) and command_to_send != constants.QUIT:       
                nombre = command_to_send.split()
                host_send = input("Host: ")
                host_send  = "\nHost: "+host_send
                command_to_send +=host_send
                tipo = nombre[0]
                nombre = nombre[1]
                if tipo == constants.PUT:
                    contenido = put_client.get_object(nombre)
                    header = command_to_send.encode(constants.ENCONDING_FORMAT)
                    header += contenido
                    print(header)
                    client_socket.send(header)
                else:
                    command_to_send += "\r\n\r\n"
                    client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
                data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
                #time.sleep(0.2)
                while True:
                    data_received_add = client_socket.recv(constants.RECV_BUFFER_SIZE)
                    if not data_received_add or data_received_add == b'':
                        break
                    data_received += data_received_add                    
                datos = data_received.split(b'\r\n\r\n',1)
                encabezado = str(datos[0].decode(constants.ENCONDING_FORMAT))
                print("\nResponse: \n")
                encabezado = encabezado.split()
                if encabezado[1] =='200' and tipo == constants.GET:
                    print(encabezado)
                    save.save_object(nombre,datos,direccion, port)
                else:
                    try:
                        print(encabezado)
                        print('\r\n',datos[1].decode(constants.ENCONDING_FORMAT))
                    except:
                        print(encabezado)
                client_socket.close() 
                main(direccion, port)
            elif command_to_send == constants.QUIT:
                continue
            else:
                print('Please enter a valid command')
            #client_socket.connect((direccion,port, host_send))  

    except Exception as e:
        print(e)
        client_socket.close()
        print('Error, please try again...')

    print('Closing connection...BYE BYE...')
    client_socket.close()
    
def parser(name_html, client, server):
    links = []
    with open('Client/' + name_html) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        images = soup.findAll('img')
        for img in images:
            print(img['src'])
            links.append(img['src'])
    if len(links) > 0:
        for i in links:
            request = 'GET' + ' ' + '/' + i + ' ' + 'HTTP/1.1\r\nHost: ' + server + '\r\n\r\n'
            client.send(request.encode())
            response = client.recv(4000000).split(b"\r\n\r\n")
            print(response[0].decode())
            status_code = response[0].decode().split(' ')[1]
            if(status_code == '200'):
                file_receive = response[1]
                file = open("./Client/" + i, 'wb')  
                file.write(file_receive)
                file.close()
                print('File receive')
            else:
                print(response[1].decode())
            print("************************")      

if __name__ == '__main__':
    print('***********************************')
    print('Client is running...')
    direccion = input('Enter the IP Address: ')
    port = int(input('Enter the Port: '))
    main(direccion, port)
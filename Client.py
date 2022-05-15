# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # TCP-Socket Client
    # David Gomez Correa - Samuel Meneses Diaz
# ********************************************************************************************

#Import libraries for networking communication...

import re
import socket
import constants
import time
from Cliente import save

lista_metodos_aceptados = [constants.GET, constants.HEAD, constants.DELETE, constants.PUT, constants.QUIT]
exp_reg_direccion = re.compile('([/\w]+).(\w+)') 
exp_reg_URL = re.compile('([\w]+)://([\w+\.]+)([/\w|-]+).(\w+)') 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #AF_INET define el tipo de direccion (ipv4), y modo TCP

def validador(encabezado):
    encabezado = encabezado.split()
    if encabezado[0] in lista_metodos_aceptados:
        if exp_reg_direccion.match(encabezado[1]) or exp_reg_URL.match(encabezado[1]):
            if encabezado[2] == "HTTP/1.1":
                return True
    return False
        

def main():
    print('***********************************')
    print('Client is running...')
    direccion = input('Enter the IP Address: ')
    port = int(input('Enter the Port: '))
    try:
        client_socket.connect((direccion,port))                 #Es donde el client se conectara al servidor
        local_tuple = client_socket.getsockname()
        print('Connected to the server from:', local_tuple)
        command_to_send = ""
        while command_to_send != constants.QUIT :
            print('\nEnter \"quit\" to exit')
            print('Input commands:')
            print('QUIT, GET, POST, HEAD, DELETE\n')
            command_to_send = input()
            if validador(command_to_send):       
                nombre = command_to_send.split()
                host_send = input("Host: ")
                host_send  = "\nHost: "+host_send+"\r\n\r\n"
                command_to_send +=host_send
                tipo = nombre[0]
                nombre = nombre[1]
                if nombre == "/":
                    nombre = "/index.html"
                client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
                data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
                time.sleep(0.2)
                data_received_add = client_socket.recv(constants.RECV_BUFFER_SIZE)
                if data_received_add != b'':
                    data_received += data_received_add                    
                datos = data_received.split(b'\r\n\r\n',1)
                encabezado = str(datos[0].decode(constants.ENCONDING_FORMAT))
                print("\nResponse: \n")
                print(encabezado)
                encabezado = encabezado.split()
                if encabezado[1] =='200' and tipo == constants.GET:
                    save.save_object(nombre,datos,direccion, port)
                else:
                    print('\r\n',datos[1].decode(constants.ENCONDING_FORMAT))
            else:
                print('Please enter a valid command')
            #client_socket.close() 
            #client_socket.connect((direccion,port))  

    except Exception as e:
        client_socket.close()
        print(e)
        print('Error, please try again...')
        main()
    print('Closing connection...BYE BYE...')
    client_socket.close()
    
        

if __name__ == '__main__':
    main()
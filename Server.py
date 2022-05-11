# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # MultiThread TCP-SocketServer
# ********************************************************************************************

# Import libraries for networking communication and concurrency...

import socket
import threading

from numpy import empty
from setuptools import Command
import constants
from ServerMet import get, put, delete

# Defining a socket object...
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)           #AF_INET define el tipo de direccion (ipv4), y modo TCP
server_address = constants.IP_SERVER                                       #Define la direccion del servidor
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        #Configuracion del socket

def main():
    print("***********************************")
    print("Server is running...")
    print("Dir IP:",server_address )
    print("Port:", constants.PORT)
    server_execution()
    
# Handler for manage incomming clients conections...

def handler_client_connection(client_connection,client_address):
    print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')
    is_connected = True
    while is_connected:
        data_recevived = client_connection.recv(constants.RECV_BUFFER_SIZE)             #Le los datos obetnidos de la peticion
        if data_recevived == b"":                                               
            break
        print (f'Data received from: {client_address[0]}:{client_address[1]}')          #Imprimimos de donde nos llega la conexion
        remote_string = data_recevived.split(b'\n\n')                                   #Division de la peticion entrante por contenido y header
        header = str(remote_string[0].decode(constants.ENCONDING_FORMAT))               #Tomamos la posicion 1 que es el header y decodificamos                                                     
        print(header)                                                                   #Imprimimos el comando entrante
        header = header.split()                                                         #Dividimos el header por  ' '
        command = header[0]                                                             #El comando va posicion 0 del header
               
        if (command == constants.GET):                                                  #En caso de que el comando sea GET
            response = get.get_object(header[1])                                        #Enviamos el header[1] es la direccion del objecto que desea tener
            client_connection.sendall(response)
        elif (command == constants.PUT):                                                #En caso de que el metodo sea PUT                  
            response = put.put_object(header, remote_string)                         #Llamamos el metodo put con el header[1] y el contenido
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
            is_connected = False
        elif (command == constants.HEAD):
            response = "300 DRCV\n"
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
        elif (command == constants.DELETE):
            response = delete.delete_object(header)
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
        else:
            response = 'HTTP/1.1 404 Not Found\n\n'.encode(constants.ENCONDING_FORMAT)
            header = '<html><body>Error 404: File not found</body></html>'.encode(constants.ENCONDING_FORMAT)
            response += header
    
    print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
    client_connection.close()

#Function to start server process...
def server_execution():
    tuple_connection = (server_address,constants.PORT)                      #Tupla con la direccion y el puerto
    server_socket.bind(tuple_connection)                                    #Colocamos el socket visible en privado (dupla direccion, puerto)
    print ('Socket is bind to address and port...')
    server_socket.listen(5)                                                 #Indicamos a sockets no colocar mas de 5 solicitudes en cola
    print('Socket is listening...')
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handler_client_connection, args=(client_connection,client_address))
        client_thread.start()
    print('Socket is closed...')
    server_socket.close()

if __name__ == "__main__":
    main()
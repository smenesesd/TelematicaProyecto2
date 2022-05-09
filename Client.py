# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # TCP-Socket Client
    # David Gomez Correa - Samuel Meneses Diaz
# ********************************************************************************************

#Import libraries for networking communication...


import socket
import constants
import threading

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #AF_INET define el tipo de direccion (ipv4), y modo TCP

def main():
    print('***********************************')
    print('Client is running...')
    client_socket.connect(("127.0.0.1",constants.PORT))                 #Es donde el client se conectara al servidor
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    print('Enter \"quit\" to exit')
    print('Input commands:')
    print('HELO, DATA, QUIT, GET, POST, HEAD, DELETE')
    command_to_send = input()

    #cmd = 'GET http://data.pr4e.otg/romeo.txt HTTP/1.0\r\n\r\n'.encode()
    #client_socket.send(cmd)
    
    while command_to_send != constants.QUIT:
        if command_to_send == '':
            print('Please input a valid command...')
            command_to_send = input()                    
        elif (command_to_send == constants.DATA):
            data_to_send = input('Input data to send: ') 
            command_and_data_to_send = command_to_send + ' ' + data_to_send
            client_socket.send(bytes(command_and_data_to_send,constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
            print(data_received.decode(constants.ENCONDING_FORMAT))
            command_to_send = input()            
        else:        
            print(command_to_send)
            client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)  
            data_received.split("\n\n")
            print(data_received[0].decode(constants.ENCONDING_FORMAT),data_received[1])
            command_to_send = input()
    
    client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
    print(data_received.decode(constants.ENCONDING_FORMAT))
    print('Closing connection...BYE BYE...')
    client_socket.close()    

if __name__ == '__main__':
    main()
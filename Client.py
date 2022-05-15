# ********************************************************************************************
    # Proyecto 2
    # Course: ST0255 - Telemática
    # MultiThread TCP-SocketServer
    #Samuel Meneses Diaz
    #David Gomez Correa
# ********************************************************************************************

# Import libraries for networking communication and concurrency...


import re
import socket
import constants
from Cliente import save, put_client


lista_metodos_aceptados = [constants.GET, constants.HEAD, constants.DELETE, constants.PUT, constants.QUIT]  #Lista de comandos aceptados por el cliente
exp_reg_direccion = re.compile('([/\w]+).(\w+)')                                                            #Expresiones regulares para validar los recursos que se quieren obtner
exp_reg_URL = re.compile('([\w]+)://([\w+\.]+)([/\w|-]+).(\w+)') 


def validador(encabezado):                                                              #Validador: Metodo para validar la direccion a la cual se desea acceder
    encabezado = encabezado.split()
    if encabezado[0] in lista_metodos_aceptados:                                        #Evalua los metodos admitidos
        if exp_reg_direccion.match(encabezado[1]) or exp_reg_URL.match(encabezado[1]):  #Evalua las expresiones regualares
            if encabezado[2] == "HTTP/1.1":                                             #Evalua la parte final del encabezado
                return True
        elif encabezado[1]=='/':                                                        #Excepcion: Cuando se pregunta por el archivo raiz 
            return True
    return False
        

def main(direccion, port):
    try:
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)            #AF_INET define el tipo de direccion (ipv4), y modo TCP
        client_socket.connect((direccion,port))                                     #Es donde el client se conectara al servidor
        local_tuple = client_socket.getsockname()
        print('Connected to the server from:', local_tuple)
        command_to_send = ""
        while command_to_send != constants.QUIT :                                   #Ciclo de conexion mientras que el comando no se QUIT
            print('\nEnter \"QUIT\" to exit')                                       #Impresion con mensajes para ususrio
            print('Input commands:')
            print('QUIT, GET, POST, HEAD, DELETE\n')
            command_to_send = input()                                               #Ingreso del comando por parte del usuario
            if validador(command_to_send) and command_to_send != constants.QUIT:    #Validamos que el comando este permitido     
                nombre = command_to_send.split()                                    #Partimos el comando por ' ' para obtener cada parte de este
                host_send1 = input("Host: ")                                        #Pedimos al usuario por pantalla el host destino
                host_send  = "\nHost: "+host_send1
                command_to_send +=host_send                                         #Añadimos el host al encabezado para el correcto envio de este
                tipo = nombre[0]                                                    #Sacamos el tipo (metodo utilizado)
                nombre = nombre[1]                                                  #Sacamos el nombre (direccion del recurso)
                if tipo == constants.PUT:                                           #En caso de que la peticion sea un PUT se realizan pasos adicionales para cargar el archivo
                    contenido = put_client.get_object(nombre)                       #Metodo para obtener el contenido que se desea enviar
                    header = command_to_send.encode(constants.ENCONDING_FORMAT)     #Codificacion del encabezado
                    header += contenido                                             #Anexamos al encabezado el contenido
                    client_socket.send(header)                                      #Enviamos el mensaje completo
                else:                                                                       #En caso de ser cualquiera de los demas metodos
                    command_to_send += "\r\n\r\n"                                           #Añadimos un doble salto de linea 
                    client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))   #Se codifica el mensaje y se envia
                data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)          #Recibimos la informacion que llega del servidor
                #time.sleep(0.2)
                while True:                                                             #En caso de que el mensaje este partido, se realiza este bucle para anexar los datos restantes
                    data_received_add = client_socket.recv(constants.RECV_BUFFER_SIZE)
                    if not data_received_add or data_received_add == b'':               #Mientras que los datos no sean vacios, se anexan a la parte que ya llego
                        break
                    data_received += data_received_add                    
                datos = data_received.split(b'\r\n\r\n',1)                              #Dividimos los datos entrantess por doble salto de linea, ya que este divide encabezado y archivos
                encabezado = str(datos[0].decode(constants.ENCONDING_FORMAT))           #Decodificamos el encabezado
                encabezado_print = encabezado
                print("\nResponse: \n")
                encabezado = encabezado.split()                                         #Dividimos el encabezado por ' ' para saber que codigo de respuesta llego
                if encabezado[1] =='200' and tipo == constants.GET:                     #En caso de ser 200 y ser un GET, debemos almacenar el archivo entrante
                    print(encabezado_print)                                             #Imprimimos encabezado
                    save.save_object(nombre,datos,direccion, port, host_send1)          #Llamamos al meotodo save_object para almacenar el archivo
                else:                                                                   #De lo contrario solo imprimimos los datos entrantes
                    try:    
                        print(encabezado_print)
                        print('\r\n',datos[1].decode(constants.ENCONDING_FORMAT))
                    except:
                        print(encabezado_print)
                client_socket.close()                                                   #Cerramos conexion, dado que los servidores http tambien lo hacen
                main(direccion, port)                                                   #Volvemos a llamar a main para repetir el proceso
                return
            elif command_to_send == constants.QUIT:
                break
            else:       
                print('Please enter a valid command')                                   #En caso de ingresar un comando invalido
            #client_socket.connect((direccion,port, host_send))  

    except Exception as e:                                                              #Excepcion en caso de ocurrir un error
        print(e)
        client_socket.close()
        print('Error, please try again...')

    print('Closing connection...BYE BYE...')                                            #Final del programa
    client_socket.close()     

if __name__ == '__main__':
    print('***********************************')            #Inicio del programa
    print('Client is running...')
    direccion = input('Enter the IP Address: ')             #Se le pide por pantalla al usuario direccion y puerto
    port = int(input('Enter the Port: '))
    main(direccion, port)
import socket

def iniciar_cliente():
    HOST = 'localhost'    # The remote host
    PORT = 30390              # The same port as used by the server
    cliente_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente_socket.connect((HOST, PORT))
        recibido = cliente_socket.recv(1024)
        recibido= recibido.decode("utf-8")
        print(recibido)
    except ConnectionError:
        print("ERROR DE CONEXION CON EL SERVIDOR")  
        return False    

    return cliente_socket

def enviar_mensaje(cliente_socket, mensaje):
        tamanio=str(len(mensaje))
        tamanio=tamanio.encode("UTF-8")
       
        cliente_socket.send(tamanio)
        mensaje= mensaje.encode("UTF-8")
        cliente_socket.send(mensaje) #envio tipo string

def getdatabase(cliente_socket):
      peticion=b"database"
      cliente_socket.send(peticion)
      database= cliente_socket.recv(1024)
      database= database.decode("utf-8")
      return database
      

# mi_socket=iniciar_cliente()
# mensaje= input("escriba mensaje: ")

# enviar_mensaje(mi_socket, mensaje)
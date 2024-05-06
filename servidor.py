import socket
import threading
from pathlib import Path
import os
import sqlite3


#ruta de archivos propios
database="serv_database.db"

#     def cerrar():
#         if s is not None:
#             s.shutdown()
#             print('Servidor Cerrado')

def atender_peticion(peticion, el_cliente):
    if peticion== "database":
        el_cliente.send(database.encode("utf-8"))

def create_db_default():
    ruta_db=os.getcwd()+"\defaultdatabase.db"
    conex=sqlite3.connect(ruta_db)
    cursor = conex.cursor() #Los cursores nos permiten almacenar información de manera temporal
    i_sql="CREATE TABLE productos"+"""
                    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    producto TEXT NOT NULL, 
                    compra INTEGER NOT NULL,
                    venta INTEGER NOT NULL,
                    stock INTEGER NOT NULL)"""
    cursor.execute(i_sql) #EJECUTAR
    conex.commit() #CONFIRMAR
    return

def escuchar_cliente(el_cliente, dir):
    while True:
        peticiones=["database", ]
        es_peticion=False
        recibido= el_cliente.recv(1024)#determina el largo del paquete de envio/recibo
        recibido=recibido.decode("UTF-8")

        for p in peticiones:
             if recibido==p:
                es_peticion=True
                atender_peticion(recibido, el_cliente)
                        
                
        if es_peticion==False:
            tamanio= int(recibido)
            if tamanio >0:
                            
                recibido=""
                while int(len(recibido))< tamanio:
                    x=el_cliente.recv(1024)
                    x=x.decode("UTF-8")
                    recibido+=str(x)

                print(f"Cliente: {recibido}")  


if __name__ == "__main__":
    
    HOST = 'localhost'                 
    PORT = 30390
                 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5) #hasta 15 solicitudes de conexión
        clientes_conectados=[]
        while True:
                               
                (cliente_conectado, direccion) = server_socket.accept()
                
                clientes_conectados.append((cliente_conectado, direccion))
                cliente_conectado.send(b"Conectado con el servidor")

                hilo_cliente=threading.Thread(target=escuchar_cliente, args=(cliente_conectado, direccion))
                hilo_cliente.start() #escucha continua hasta que se cierre el cliente


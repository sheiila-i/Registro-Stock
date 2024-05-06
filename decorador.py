import pickle
from datetime import *
from tkinter.messagebox import *


def guardar_totales(funcion):
    def envoltura(*args):
        registro=funcion(*args)
        ruta_totales= args[0].archivo_totales.ruta
        archivo_totales = open(ruta_totales, "wb") #abro el archivo.pkl para guardar info totales
        pickle.dump(registro, archivo_totales) #escribo en tal archivo
        archivo_totales.close() #cierro el archivo

        args[0].notificar()
        return
    return envoltura


def registrar_operacion(funcion):
    def envoltura(*args):

        ruta_archivo, nombre_producto, cantidad, dinero, stock_actualizado= funcion(*args)
        fecha= str(datetime.now().strftime('%d/%m/%Y %H:%M'))
        archivo= open(ruta_archivo, "a+")
        registro= "("+ fecha +") producto: "+ nombre_producto + " ; cantidad: "+ cantidad+ dinero+" ; stock actualizado: "+ stock_actualizado 

        archivo.write(registro + " \n")
        archivo.close()

        return
    return envoltura
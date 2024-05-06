from tkinter.messagebox import *
from peewee import *
from datetime import *

class Observable():
    observadores= [] #clase Observer
    def agregar_observador(self, nuevo):
        self.observadores.append(nuevo)

        return
    
    def quitar_observador(self, observador):
        for o in self.observadores:
            if o==observador:
                del self.observadores[o]

    def notificar(self, *args):
        for o in self.observadores:
           o.update(*args)
        return


class Observador():
    def _update(self, *args):
        raise NotImplementedError ("Delegacion de actualizacion")
        

class ObservadorMovimientos(Observador):
    def __init__(self, obj_observado):
        self.observado=obj_observado

        self.observado.agregar_observador(self)
        self.observado.registro= self.observado.archivo_totales.leer_archivo()

        self.observado.set_status(self.observado.registro['capital'], self.observado.registro['saldo'], self.observado.registro['ganancias'], self.observado.registro['total'])

    
    def update(self,):
        registro_dinero= self.observado.get_status()
        self.observado.var_capital.set(registro_dinero['capital'])
        self.observado.var_saldo.set(registro_dinero['saldo'])
        self.observado.var_ganancias.set(registro_dinero['ganancias'])
        self.observado.var_total.set(registro_dinero['total'])
        
        return registro_dinero
        

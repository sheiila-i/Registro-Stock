
from vista import Ventanas
from tkinter import Tk
from tkinter.messagebox import *
from observador import ObservadorMovimientos 

class Controlador():
    def __init__(self, root):
        self.root_controlador= root
        
        self.ventana_tkinter= Ventanas(self.root_controlador)#Objeto ventana        
        self.observador_movimientos = ObservadorMovimientos(self.ventana_tkinter.registro)

        return

if __name__== "__main__":  
    root=Tk()
    root.title("MiApp - PYTHON AVANZADO")
    
    aplicacion= Controlador(root)
    
    root.mainloop()

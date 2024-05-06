from tkinter import Menu
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import Scrollbar
from tkinter import ttk
from tkinter import StringVar
from tkinter import IntVar
from modelo import Databases, Registros
import cliente


bg_color="#a8a4ce"

class Entrys():
    def __init__(self, contenedor, texto, fila, columna, tipo_dato):
        self._nombre= Label(contenedor, text=texto, font=('Lato', 10, "bold"),bg=bg_color)
        self._nombre.grid(row=fila, column=columna, sticky='W', pady=2)
        
        
        self.variable= tipo_dato
        self._entrada= Entry(contenedor, textvariable= self.variable, relief="sunken", font=('Lato', 9, "italic"))
        self._entrada.grid(row=fila, column=columna+1, sticky='W', pady=2)
    

class Labels():
    __slots__=['variable']
    def __init__(self, contenedor, texto, fila, columna):
        _nombre= Label(contenedor, text=texto, font=('Lato', 10, "bold"),bg=bg_color)
        _nombre.grid(row=fila, column=columna, sticky='W', pady=2)

        self.variable=IntVar()
        _valor= Label(contenedor, textvariable=self.variable, bg=bg_color, font=('Lato', 9, "italic"))
        _valor.grid(row=fila, column=columna+1, sticky='W', pady=2)


class Buttons():
    __slots__=[]
    def __init__(self, contenedor, texto, fila, columna, comando ):
        bg_color= "#7a86b6"

        el_boton= Button(contenedor, text=texto, font=('Lato', 10, "bold"), background=bg_color, relief="raised", command= comando)
        el_boton.grid(row=fila, column=columna, pady=2)


class Treeviews():
    def __init__(self, contenedor, fila, columna, scrollbar):
        self.db= 'None'

        self.tabla_tree= ttk.Treeview(contenedor, show="tree headings", height=10)
        self.tabla_tree.grid(row=fila, column=columna, columnspan=scrollbar, sticky='EW', pady=2)

        self.tabla_tree['columns']=("producto","compra","venta","stock")

        self.tabla_scroll=Scrollbar(contenedor, command=self.tabla_tree.yview)
        self.tabla_scroll.grid(row=fila, column=scrollbar, sticky='NS', pady=2)
        self.tabla_tree.config(yscrollcommand=self.tabla_scroll.set)

        self.tabla_tree.heading("#0", text="ID")#siempre tiene que ir el inicial
        self.tabla_tree.column("#0", stretch=False, width=50) 
        self.tabla_tree.heading("producto", text="PRODUCTO")
        self.tabla_tree.column("producto", stretch=False) 
        self.tabla_tree.heading("compra", text="COMPRA")
        self.tabla_tree.column("compra", stretch=False) 
        self.tabla_tree.heading("venta", text="VENTA")
        self.tabla_tree.column("venta", stretch=False) 
        self.tabla_tree.heading("stock", text="STOCK")
        self.tabla_tree.column("stock", stretch=False)


class Ventanas():
    bg_color="#a8a4ce"
    fuente = 'lato'

    def __init__(self, ventana):
        self.root= ventana
        self.cliente= cliente.iniciar_cliente()
        if self.cliente==None:
            self.root.quit()
        
        #
        
        self.l_saldo= Labels(self.root, "Saldo: ", 0, 0)
        self.l_ganancias= Labels(self.root, "Ganancias: ", 0, 2)

        #
        self.l_capital= Labels(self.root, "Capital Contable: ", 1, 0)
        self.l_total= Labels(self.root, "Total: ", 1, 2)


        self.e_ganancia= Entrys(self.root, " Monto: ", 0, 6, IntVar())
        self.b_retirar= Buttons(self.root, "Retirar", 1, 6, lambda:self.registro.retirar(self.e_ganancia.variable))
        self.b_invertir= Buttons(self.root, "Invertir", 1, 7, lambda:self.registro.invertir(self.e_ganancia.variable))
        #####

        self.tabla=Treeviews(self.root, 2, 0, 8)

        #####
        self.e_producto= Entrys(self.root, "Producto: ", 3, 0, StringVar())
        self.e_coste= Entrys(self.root, "Coste: ", 3, 2, IntVar())
        self.e_precio= Entrys(self.root, "Precio: ", 3, 4, IntVar())

        self.b_agregar= Buttons(self.root, "Agregar", 3, 7, lambda:self.db.agrega(self.tabla.tabla_tree, self.e_producto.variable, self.e_coste.variable, self.e_precio.variable) )
        #####

        self.e_es_modificado=Entrys(self.root, "Nuevo: ", 4, 0, StringVar())
        campos=["PRODUCTO", "COMPRA", "VENTA", "STOCK"]
        self.v_es_modificado_campo=StringVar()
        v_entrada_campo = ttk.Combobox(self.root, textvariable= self.v_es_modificado_campo, values=campos, state="readonly")
        v_entrada_campo.grid(row=4, column=3 ,sticky='E', padx=2)
        
        
        self.b_eliminar= Buttons(self.root, "Eliminar", 4, 6, lambda:self.db.elimina(self.tabla.tabla_tree))
        self.b_editar= Buttons(self.root, "Editar", 4, 7, lambda:self.db.edita(self.tabla.tabla_tree, self.e_es_modificado.variable, self.v_es_modificado_campo))
        #####

        self.e_stock= Entrys(self.root, "Unidades: ", 5, 0, IntVar())

        self.b_venta= Buttons(self.root, "Vender", 5, 6, lambda:self.registro.venta(self.tabla.tabla_tree, self.e_stock.variable))
        self.b_compra= Buttons(self.root, "Comprar", 5, 7, lambda:self.registro.compra(self.tabla.tabla_tree, self.e_stock.variable))
    
             #Declaro Observador:
        
        self.db= Databases(self.tabla.tabla_tree, self.root, self.cliente)
        self.registro= Registros(self.db.conex, self.l_capital.variable, self.l_saldo.variable, self.l_ganancias.variable, self.l_total.variable)
        ##############
       
        

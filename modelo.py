from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename
import re
from peewee import *
from tkinter import Tk
from decorador import guardar_totales, registrar_operacion
import pickle
from observador import Observable
import cliente 

class Productos():
    def __init__(self, producto, compra, venta, stock):
        self._nombre=producto
        self._compra= compra
        self._venta= venta
        self._stock= stock
        return
    
class Archivos():
    def __init__(self, name, allows=""):
        self.nombre_archivo=name
        self.ruta=self.abrir_archivo()

        self.permisos=allows
        return

    def abrir_archivo(self, ): 
        ruta=""
        showinfo(message= f"Debe abrir el archivo {self.nombre_archivo}, de lo contrario no podra seguir operando.", title="Abrir "+ self.nombre_archivo)
        
        if(askokcancel(message= f"¿Abrir archivo {self.nombre_archivo}?", title="Abrir archivo"+ self.nombre_archivo)):
            ruta= askopenfilename(title="Abrir Archivo "+ self.nombre_archivo)   
        return ruta 
    

    def leer_archivo(self):
    #dict_estructura= ("capital", "saldo", "ganancias", "total")   
    #se lee y luego cierra el archivo

        for p in self.permisos:
            encontrado= p.find('r')

        if encontrado != "-1":
            archivo= open(self.ruta,"rb")
            valores= pickle.load(archivo)
            archivo.close()
            return valores
             
        else:
            showerror(title="Error", message="No pudo abrirse el archivo")
            return
        

class Databases(Observable):     
    def __init__(self, tabla, root, socket):
        self.socket=socket
        self.ruta_db=cliente.getdatabase(self.socket)
        self.conex=None

        try:
            self.conex=SqliteDatabase(self.ruta_db)
            assert  self.conex!=None, 'ERROR de conexion a la base de datos'
        except AssertionError:
            print("No pudo conectarse >>>> SALIR")
            self.salir(root, socket)
            return
        finally:
            #showinfo('Conection to database','Base de datos conectada con éxito')
            self.mostrardb(tabla)

        if self.conex==None:
            self.salir(root, socket)

    def agrega(self, tabla, var_producto, var_coste_produccion, var_precio_venta):

        if (self.conex == None):
            showerror("BASE DE DATOS" , "Ninguna base de datos abierta")
            return
            
        nuevo_producto=Productos(var_producto.get(), var_coste_produccion.get(), var_precio_venta.get(), "0")

        resultado=re.search(r'[$%&/()=.,:¿?¡!<>#"|]', str(nuevo_producto._nombre)) #validar campo producto

        if resultado!=None:
            print ("error de validación")
            showerror("ERROR DATOS", "No se aceptan caracteres especiales")
            return                   

        ### SQLite3 ###
        instruccion_sql="INSERT INTO productos(producto, compra, venta, stock) VALUES(?, ?, ?, ?)"
        cursor= self.conex.cursor()
        cursor.execute(instruccion_sql, (nuevo_producto._nombre,nuevo_producto._compra,nuevo_producto._venta, nuevo_producto._stock))
        self.conex.commit()
        ### SQLite3 ###

        self.mostrardb(tabla)
                    
        var_producto.set("Producto")
        var_coste_produccion.set("Coste")
        var_precio_venta.set("Precio")
        
        return
    
    def edita(self, tabla, var_nuevo_valor, var_campo):
         
        idd_item_editar= tabla.focus() #I002, IDENTIFICADOR PROPIO my_iid
        if(idd_item_editar==""): return

        if var_nuevo_valor.get()== "" or var_campo.get()=="seleccionar campo":
            showerror("Error datos", "Debe ingresar el campo a editar y el nuevo valor")
            return
        
        id_editar=str(tabla.item(idd_item_editar)['text'])
        el_nuevo_valor=str(var_nuevo_valor.get()).strip()
        el_campo=str(var_campo.get()).lower()

        if askokcancel("Editar", "¿Está seguro que desea continuar?") == False: return       

        ### SQLite3 ###
        instruccion_sql="UPDATE productos SET "+el_campo+"= ? WHERE id="+ str(id_editar)
        cursor=self.conex.cursor()
        cursor.execute(instruccion_sql, (el_nuevo_valor,))
        self.conex.commit()
        ### SQLite3 ###

       
        #showinfo("OPERACION EXITOSA","Producto editado")
        tabla.set(idd_item_editar, el_campo, el_nuevo_valor)
                
        var_nuevo_valor.set("")
        var_campo.set("seleccionar campo")
        return

    def elimina(self, tabla):
          
        idd_item_borrar= tabla.focus() #I002, IDENTIFICADOR PROPIO my_iid
        if(idd_item_borrar==""):return

        id_borrar=tabla.item(idd_item_borrar)['text']
        if askokcancel('ELIMINAR','Esta operación no tiene vuelta atrás,\n ¿Borrar registro definitivamente?')==False: return
        
        ### SQLite3 ###
        instruccion_sql="DELETE FROM productos WHERE id="+ str(id_borrar)
        cursor=self.conex.cursor()
        cursor.execute(instruccion_sql)
        self.conex.commit()
        ### SQLite3 ###

        tabla.delete(idd_item_borrar)

        return
   
    def mostrardb(self, tabla):      
        allidfilas = tabla.get_children() #selecciona todas las filas para luego borrarlas
        for fila in allidfilas:
            tabla.delete(fila)
        
        ### SQL ###
        instruccion_sql= "SELECT * FROM productos" 
        cursor=self.conex.cursor()
        cursor.execute(instruccion_sql)
        
        datadb=cursor.fetchall() #selecciona todas las filas
        self.conex.commit()

        ### SQL ###
        for reg in datadb:
            tabla.insert("","end",text=reg[0],values=(reg[1], reg[2], reg[3], reg[4]))
        
        return
    
    def salir(self, root, socket):  
        if(askyesno("SALIR","Salir de miApp")==True):
            if(self.conex!=None):
                self.conex.close()
                socket.shutdown()
                socket.close()
                print('Cliente Cerrado')

            root.quit()
        return
        
        #-----------------------------------------------------------------------------------------
        
class Registros(Observable):
    def __init__(self, db, capital, saldo, ganancias, total ):
        #self.vendedor="Shei"
        self.conex= db
        self.registro={}
        self.var_capital=capital
        self.var_saldo=saldo
        self.var_ganancias=ganancias
        self.var_total=total

        self.archivo_totales= Archivos("totales","a+")
        self.archivo_compras=""
        self.archivo_ventas="" 
        return 
    
    def get_status(self):
        #dict_estructura= ("capital", "saldo", "ganancias", "total")   
        return self.registro
    
    @guardar_totales
    def set_status(self, capital, saldo, ganancias, total):

        self.registro['capital']=capital
        self.registro['saldo']=saldo
        self.registro['ganancias']=ganancias
        self.registro['total']=total


        return self.registro

    @registrar_operacion
    def compra(self, tabla, var_cant):
        total=self.var_total.get()
        saldo=self.var_saldo.get()
        cant_compra=var_cant.get()
        

        if self.archivo_compras=="":
            self.archivo_compras=Archivos("compras", "w+")

        data=self.com_y_ven(tabla) # (registro, stock antes, fila seleccionada)

        egreso= int(cant_compra)*int(data[0][2]) # unidades * p_compra
        if(egreso>saldo):
            showerror("SALDO", "Saldo no disponible para realizar la compra")
            return
        
        stock_ahora=int(data[1])+ int(cant_compra) #stock ahora 'hipotetico'

        ### SQL ###
        instruccion_sql="UPDATE productos SET stock="+ (str(stock_ahora)) +" WHERE id="+ str(data[0][0])
        cursor=self.conex.cursor()
        cursor.execute(instruccion_sql)
        self.conex.commit()
        ### SQL ###

        tabla.set(data[2],"stock", stock_ahora)
        
        #modificar valores dinero
        saldo=saldo-egreso
        total=total-egreso

        self.set_status(self.var_capital.get(),saldo,self.var_ganancias.get(),total)
       
        var_cant.set("0")

        return (self.archivo_compras.ruta, data[0][1], str(cant_compra), " - egreso: " + str(egreso), str(stock_ahora))

    @registrar_operacion
    def venta(self, tabla, var_cant):
        capital=self.var_capital.get()
        saldo=self.var_saldo.get()
        ganancias=self.var_ganancias.get()
        total=self.var_total.get()

        cant_venta=int(var_cant.get())

        if self.archivo_ventas=="":
            self.archivo_ventas=Archivos("ventas", "w+")
        
        data=self.com_y_ven(tabla)
        stock_ahora=data[1]- int(cant_venta)
        ingreso=int(cant_venta)*int(data[0][3])

        if(stock_ahora<0): #lo que quedaría de stock en el hipotetico caso de comprarse
            showerror("ERROR", "Stock no disponible para realizar la venta")
            return

        #actualizo la db y el treeview con el nuevo valor
        
        ### SQL ##
        instruccion_sql="UPDATE productos SET stock="+str(stock_ahora)+" WHERE id="+str(data[0][0])
        cursor=self.conex.cursor()
        cursor.execute(instruccion_sql)
        self.conex.commit()
        ### SQL ###

        tabla.set(data[2],"stock", stock_ahora)

        #modificar valores dinero
        total+=ingreso
        if (ingreso>(capital-saldo)):
            ganancias+=ingreso+saldo-capital
            saldo = capital
        else:
            saldo+=ingreso    

        self.set_status(capital, saldo, ganancias, total) 
        var_cant.set("0")

        return (self.archivo_ventas.ruta, data[0][1], str(cant_venta), " - ingreso: " + str(ingreso), str(stock_ahora))

    def com_y_ven(self, tabla): # db= la con de la base de datos

        idd_seleccion= tabla.focus()
        id= tabla.item(idd_seleccion)['text'] #del treeview segun idd capturado

        # capturo registro de la db para modificar el stock
        
        ### SQL ###
        instruccion_sql=" SELECT * FROM productos WHERE id="+str(id)
        cursor=self.conex.cursor()
        cursor.execute(instruccion_sql)
        registro=cursor.fetchone() #TODO?
        stock_antes=int(registro[4]) #stock antes
        self.conex.commit()
        ### SQL ###

        data=[registro, stock_antes, idd_seleccion]
        return data
    

    def retirar(self, var_monto, reg_dinero):
          
        total=reg_dinero[0].get()
        ganancias=reg_dinero[2].get()
        monto=var_monto.get()

        if(monto>ganancias):
            showerror("ERROR DATOS", "El monto ingresado no debe ser mayor que las ganancias obtenidas.")
            return
        
        ganancias-= monto
        total-=monto    
        valores=(total, reg_dinero[1].get(), ganancias, reg_dinero[3].get())
        # self.guardar_arch_totales(valores, reg_dinero)

        self.set_status(self.var_capital.get(), self.var_saldo.get(), ganancias, total)
        var_monto.set(0)

        
        return

    #@registrar_operacion
    #@setear_registro
    def invertir(self, var_monto):
              
        ganancias=self.var_ganancias.get()
        capital=self.var_capital.get()
        saldo=self.var_saldo.get()

        monto= var_monto.get()

        if(monto>ganancias):
            showerror("ERROR DATOS", "El monto ingresado no puede ser mayor que las ganancias obtenidas.")
            return
        
        ganancias-= monto
        capital+=monto
        saldo+=monto

        self.set_status(capital, saldo, ganancias,self.var_total.get())
        var_monto.set(0)

        
        return #(capital, saldo, ganancias, self.var_total.get())













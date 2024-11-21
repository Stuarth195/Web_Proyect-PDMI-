from admin import Seccion
from TXTReader import LectorTXT
from WriterEnDocumento import Writer
from Producto import Product
from logic import Instacia_B
import tkinter as tk
from tkinter import messagebox
import os
from botones import Botones, BotonesPE, ReciboCosecha
from verify import FechaEntradaApp, CodigoApp, CantidadApp, ProvedorApp
from loteinfo import LoteInfo
from InterfazGenerica import InterfazGenerica
class Pantalla_add:
    def __init__(self, ventana=None, notebook=None, archivo_usuarios= os.path.join("RegistroCompras.txt"), archivo_recetas=None, archivo_lotes = os.path.join("LISTA PRODUCTO Y RECETAS", "Lotes.txt"), usuario_log= None):
        self. usuario_log = usuario_log
        self.ventana = ventana
        self.notebook = notebook
        self.archivo_usuarios = archivo_usuarios
        self.archivo_recetas = archivo_recetas
        self.archivo_lotes = archivo_lotes
        self.admin = None
        self.ancho = self.ventana.winfo_screenwidth()
        self.alto = self.ventana.winfo_screenheight()
        self.historial_open = False
        self.lista_productos_open =False
        self.lector =  LectorTXT()
        self.escritor = Writer()
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        self.someopen = False
        self.frame_interno= None
        self.almacen_open = False
        self.sv_open = False
        self.SV = None
        self.veriFCH = None
        self.verCOD=None
        self.verCNT = None
        self.verePRV = None
        self.rutalotes = os.path.join("LISTA PRODUCTO Y RECETAS","Lotes.txt")
        self.Descuentos_open = False
        self.facturacion_open = False
        self.VRC_open = False
        self.VTL_open = False

        
        
        
    def crear_menu(self):
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        # Crear el menú principal en la ventana
        self.menu_bar = tk.Menu(self.ventana)

        # Submenú para los productos (solo dentro de "Ventas")
        productos_menu = tk.Menu(self.menu_bar, tearoff=0)
        productos_menu.add_command(label="Crear Producto",)
        productos_menu.add_command(label="Quitar Producto")
        productos_menu.add_command(label="Modificar Producto")
        productos_menu.add_command(label="crear descueto", command=lambda:self.Botones_Desc(500,self.admin.frame_scroll, 0,0))

        # Submenú Ventas
        ventas_menu = tk.Menu(self.menu_bar, tearoff=0)
        ventas_menu.add_cascade(label="Productos", menu=productos_menu)  # Agregar "Productos"

        # Submenú Administrativo dentro de Opciones de Admin
        administrativo_menu = tk.Menu(self.menu_bar, tearoff=0)
        administrativo_menu.add_command(label="Historiales" , command=self.crear_botones_historial)  # Solo "Historiales" en Administrativo
        administrativo_menu.add_command(label="Facturas", command=self.HDF)
        administrativo_menu.add_command(label="Generar recibo Cosecha ", command=self.GRC)
        administrativo_menu.add_command(label="Ver recibo Cosecha ", command=self.VRC)


    #menue almacen
        menu_almacen =tk.Menu(self.menu_bar, tearoff=0)
        menu_almacen.add_command(label="Agregar Lotes", command=lambda: self.agrega_lotes())
        menu_almacen.add_command(label="Maestro de Artículos",command= self.MA_vista)
        menu_almacen.add_command(label="Productos Comprados", command= self.IPC)
        menu_almacen.add_command(label="Registro de Producción", command= self.RDP)
        menu_almacen.add_command(label="ver Lotes", command= self.verlotes)
        menu_almacen.add_command(label="Productos  de Cosechas", command= self.PPO)

        # Crear el menú "Opciones de Admin" y añadir los submenús
        opciones_admin_menu = tk.Menu(self.menu_bar, tearoff=0)
        opciones_admin_menu.add_cascade(label="Ventas", menu=ventas_menu)  # Agregar "Ventas"
        opciones_admin_menu.add_cascade(label="Administrativo", menu=administrativo_menu)
        opciones_admin_menu.add_cascade(label="Almacen",menu=menu_almacen)  # Agregar "Administrativo"

        # Añadir "Opciones de Admin" al menú principal
        self.menu_bar.add_cascade(label="Opciones de Admin", menu=opciones_admin_menu)

        # Configurar el menú en la ventana principal
        self.ventana.config(menu=self.menu_bar)


    def pantalla_oculta(self, nombre):
        self.crear_menu()
        # Crear una sección y su contenido en la pantalla oculta
        self.admin = Seccion(self.notebook, self.alto, self.ancho, "black")
        self.admin.crear(nombre)



    def crear_vista_Historial(self, lado, lugar, padx=0, pady=0):
        self.lado_hiostorial = lado
        if self.historial_open == False and self.someopen == False:
            # Crear el canvas y configurarlo para llenarse dentro del lugar especificado
            self.canvas = tk.Canvas(lugar, bg="lightblue", width=lado, height=lado)
            self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=padx, pady=pady)

            # Configurar el canvas para que use el desplazamiento con el ratón
            self.canvas.config(scrollregion=(0, 0, lado, lado * 2))  # Ajustar la altura del scroll para simular más espacio hacia abajo

            # Crear un frame interno para colocar los botones dentro del canvas
            self.frame_interno = tk.Frame(self.canvas, bg="lightblue")
            self.canvas.create_window((0, 0), window=self.frame_interno, anchor="nw")

            # Actualizar la región desplazable según el tamaño del frame_interno
            self.frame_interno.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            # Función para mover el canvas con el ratón
            def scroll_canvas(event):
                try:
                    if self.canvas.winfo_exists():  # Verifica si el canvas sigue válido
                        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
                except tk.TclError:
                    print("Canvas no válido o eliminado.")

            # Vincular el evento de desplazamiento del ratón al canvas
            self.canvas.bind("<MouseWheel>", scroll_canvas)  # Usar bind en lugar de bind_all

            self.historial_open = True
            self.someopen = True
            self.crear_botones_historial()
        elif self.historial_open == True:
            # Si historial_open es True, eliminar la vista de historial actual
            if hasattr(self, 'canvas'):
                self.canvas.unbind("<MouseWheel>")  # Desvincula el evento
                self.canvas.destroy()  # Elimina el Canvas
            if hasattr(self, 'frame_interno'):
                self.frame_interno.destroy()  # Elimina el Frame interno

            self.historial_open = False 
            self.someopen = False  # Cambiar el estado para indicar que la vista ha sido cerrada
        else:
            messagebox.showwarning("Advertencia", "No puedes avanzar si tienes un proceso abierto")

    def crear_botones_historial(self):
        if not self.someopen and not self.historial_open:  # Verifica que no esté abierto
            self.someopen = True
            self.historial_open = True  # Establece el historial como abierto

            self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
            # Verifica que la lista generada no esté vacía
            if self.Us_math:
                nombres_agregados = set()  # Conjunto para evitar nombres duplicados

                # Escalar el ancho de los botones en función del ancho de la pantalla
                ancho_boton = self.ancho // 10  # Ajusta el divisor según cómo quieras que se escale

                # Primero, elimina todos los widgets existentes en frame_scroll
                for widget in self.admin.frame_scroll.winfo_children():
                    widget.destroy()  # Elimina todos los widgets (botones) del frame_scroll

                # Iterar sobre cada línea en la lista generada
                for linea in self.Us_math:
                    nombre = linea[0]  # El nombre está en la posición 0
                    if nombre not in nombres_agregados:
                        nombres_agregados.add(nombre)  # Registrar el nombre como agregado

                        # Crear el botón y asociarlo a un comando con `lambda`
                        boton = tk.Button(
                            self.admin.frame_scroll,
                            text=nombre,
                            width=ancho_boton,
                            command=lambda nombre=nombre: self.comando_botones_historial(nombre)
                        )

                        # Empaquetar el botón dentro del contenedor
                        boton.pack(fill=tk.X, pady=5, padx=5)

        elif self.historial_open:  # Si el historial está abierto, se procede a limpiarlo
            # Eliminar todos los widgets existentes en frame_scroll
            for widget in self.admin.frame_scroll.winfo_children():
                widget.destroy()  # Elimina todos los widgets (botones) del frame_scroll

            # No es necesario destruir el frame_scroll ni otros componentes
            self.historial_open = False
            self.someopen = False

        else:
            messagebox.showwarning("Advertencia", "No puedes avanzar si tienes un proceso abierto")

    def extraer_historial(self, linea):
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        # Busca las sublistas delimitadas por [ y ]
        historial = []
        contenido = ''.join(linea)  # Convierte la línea en una cadena única para simplificar la búsqueda
        
        # Encuentra los fragmentos entre los delimitadores
        inicio = contenido.find('[')
        while inicio != -1:
            fin = contenido.find(']', inicio)
            if fin != -1:
                # Extraer el contenido entre los delimitadores y dividirlo por comas
                sublista = contenido[inicio+1:fin].split(',')
                # Limpiar espacios en blanco de cada elemento
                historial.extend([item.strip() for item in sublista])
                inicio = contenido.find('[', fin)  # Buscar la siguiente sublista
            else:
                break  # Salir si no se encuentra el delimitador de cierre
        
        return historial

    def comando_botones_historial(self, nombre):
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        alto = 800
        ancho = 1000
        # Crear la subventana
        subventana = tk.Toplevel(self.ventana, width=ancho, height=alto)
        subventana.title(nombre)
        subventana.resizable(0, 0)

        # Crear un Canvas para manejar el scroll
        canvas = tk.Canvas(subventana, width=ancho, height=alto)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Agregar Scrollbar al Canvas
        scrollbar = tk.Scrollbar(subventana, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=scrollbar.set)

        # Crear un frame dentro del Canvas
        frame_contenedor = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_contenedor, anchor="nw")

        # Función para actualizar la región desplazable del Canvas
        def actualizar_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Vincular el ajuste del tamaño del frame para actualizar el scroll
        frame_contenedor.bind("<Configure>", actualizar_scroll)

        # Permitir desplazamiento con la rueda del ratón
        def scroll_con_rueda(event):
            try:
                if canvas.winfo_exists():  # Comprueba si el widget aún existe
                    canvas.yview_scroll(-1 * (event.delta // 120), "units")
            except tk.TclError:
                print("Canvas no válido o eliminado.")


        canvas.bind_all("<MouseWheel>", scroll_con_rueda)

        # Verifica si hay datos en Us_math
        if self.Us_math:
            self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
            for linea in self.Us_math:
                if linea[0] == nombre:
                    # Extrae las sublistas del historial
                    historial = self.extraer_historial(linea)
                    
                    # Crear un encabezado
                    encabezado = tk.Label(frame_contenedor, text="Fecha     Producto     Cantidad     Precio Unidad     Total", font=("Arial", 10, "bold"))
                    encabezado.pack(fill=tk.X, pady=5, padx=5)
                    
                    # Crear un Label para cada entrada en el historial formateada
                    for entrada in historial:
                        # Separar los datos en variables: asumiendo que la entrada tiene fecha, producto, cantidad, precio por unidad y total
                        try:
                            # Separa los elementos de entrada (ajusta según el formato real de tus datos)
                            fecha, producto, cantidad, precio_unidad, total = entrada.split(';')  # Ajusta si el delimitador es diferente
                            
                            # Formatear el texto
                            texto = f"Fecha: {fecha.strip()}     Producto: {producto.strip()}     Cantidad: {cantidad.strip()}     Precio Unidad: {precio_unidad.strip()}     Total: {total.strip()}"
                        except ValueError:
                            texto = "Datos incompletos o incorrectos en el historial"
                        
                        # Crear un Label para cada entrada formateada
                        label = tk.Label(frame_contenedor, text=texto, anchor="w")
                        label.pack(fill=tk.X, pady=2, padx=5)


    def mostrar_historial_usuario(self,):
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        alto = 800
        ancho = 1000
        # Crear una subventana solo para el usuario logueado
        subventana = tk.Toplevel(self.ventana, width=ancho, height=alto)
        subventana.title(f"Historial de {self.usuario_log}")
        subventana.resizable(0, 0)

        # Crear un Canvas para manejar el scroll
        canvas = tk.Canvas(subventana, width=ancho, height=alto)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Agregar Scrollbar al Canvas
        scrollbar = tk.Scrollbar(subventana, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=scrollbar.set)

        # Crear un frame dentro del Canvas
        frame_contenedor = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_contenedor, anchor="nw")

        # Función para actualizar la región desplazable del Canvas
        def actualizar_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Vincular el ajuste del tamaño del frame para actualizar el scroll
        frame_contenedor.bind("<Configure>", actualizar_scroll)

        # Permitir desplazamiento con la rueda del ratón
        def scroll_con_rueda(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind_all("<MouseWheel>", scroll_con_rueda)

        # Verifica si hay datos en Us_math
        if self.Us_math:
            self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
            for linea in self.Us_math:
                # Filtrar el historial del usuario logueado
                if linea[0] == self.usuario_log:
                    # Extrae las sublistas del historial
                    historial = self.extraer_historial(linea)

                    # Crear un encabezado
                    encabezado = tk.Label(frame_contenedor, text="Fecha     Producto     Cantidad     Precio Unidad     Total", font=("Arial", 10, "bold"))
                    encabezado.pack(fill=tk.X, pady=5, padx=5)

                    # Crear un Label para cada entrada en el historial formateada
                    for entrada in historial:
                        # Separar los datos en variables: asumiendo que la entrada tiene fecha, producto, cantidad, precio por unidad y total
                        try:
                            # Separa los elementos de entrada (ajusta según el formato real de tus datos)
                            fecha, producto, cantidad, precio_unidad, total = entrada.split(';')
                            
                            # Formatear el texto
                            texto = f"Fecha: {fecha.strip()}     Producto: {producto.strip()}     Cantidad: {cantidad.strip()}     Precio Unidad: {precio_unidad.strip()}     Total: {total.strip()}"
                        except ValueError:
                            texto = "Datos incompletos o incorrectos en el historial"
                        
                        # Crear un Label para cada entrada formateada
                        label = tk.Label(frame_contenedor, text=texto, anchor="w")
                        label.pack(fill=tk.X, pady=2, padx=5)
        else:
            label = tk.Label(frame_contenedor, text="No hay historial disponible para el usuario.")
            label.pack(fill=tk.X, pady=5, padx=5)


# Dentro de la clase Pantalla_add, en algún método de configuración o en el __init__

    def crear_boton_historial_usuario(self, donde, valx , valy):
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        # Crear el botón en la ventana principal o en un frame específico
        self.boton_historial_usuario = tk.Button(donde, text="Ver mi Historial", command=self.mostrar_historial_usuario)
        
        # Empaquetar el botón en la ventana (puedes usar .pack(), .grid() o .place() según tu diseño)
        self.boton_historial_usuario.place(x=valx, y=valy)

        donde.tag_raise("boton_historial")

    def destruir_boton_usuario(self):
        if self.boton_historial_usuario != None:
            self.boton_historial_usuario.destroy()
            self.boton_historial_usuario=None
        else:
            pass



    def reiniciar_pantalla(self):
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        self.eliminar_menu()
        # Eliminar el menú principal de la ventana
        if hasattr(self, 'menu_bar'):  # Verificar si existe el menú
            self.ventana.config(menu=None)  # Eliminar el menú asociado a la ventana
            
            # Eliminar la referencia al menu_bar (ya no hay más menú)
            del self.menu_bar  

        # Eliminar la sección de la pestaña creada (frame)
        if hasattr(self, 'admin'):
            self.admin.frame.destroy()  # Destruir el frame de la sección
            del self.admin  # Eliminar la referencia a la pestaña oculta

        # Restablecer el historial si es necesario
        self.historial_open = False
        

    def eliminar_menu(self):
        # Destruir el objeto del menú si ya existe
        if self.menu_bar:
            self.menu_bar.destroy()  # Elimina el menú de la ventana

        # Reconfigurar la ventana sin menú
        self.ventana.config(menu=None)
    

    
    def subV_crear(self, nombre="ventana", alto=500, ancho=500):
        self.SV = tk.Toplevel(self.ventana)
        self.SV.geometry(f'{alto}x{ancho}')
        self.SV.title(nombre)
        self.SV.resizable(0, 0)
        self.sv_open = True
        # Vincular el cierre de la ventana al cambio de estado de sv_open
        self.SV.protocol("WM_DELETE_WINDOW", self.subV_destruir)

    def subV_destruir(self):
        if self.SV:
            self.SV.destroy()
            self.SV = None
            self.sv_open = False
            self.veriFCH = None
            self.verCOD=None
            self.verCNT = None
            self.verePRV = None
                
    
    def agrega_lotes(self, nombre="Lotes", alto=700, ancho=700):
        if not self.sv_open:
            self.subV_crear(nombre, alto, ancho)

            # Obtener dimensiones de la ventana
            self.SV.update_idletasks()
            width = self.SV.winfo_width()
            height = self.SV.winfo_height()

            # Crear un marco (frame) para contener los widgets
            frame = tk.Frame(self.SV)
            frame.pack(padx=20, pady=20)  # Se establece un margen general
            
            self.veriFCH = FechaEntradaApp(self.SV)
            self.verCOD=CodigoApp(self.SV)
            self.verCNT = CantidadApp(self.SV)
            self.verePRV = ProvedorApp(self.SV)

            
            # Botón de "Listo", en la parte inferior
            tk.Button(self.SV, text="Crear", command=self.verificacion_de_verificaciones).pack(pady=10)  # Un pequeño margen solo en el botón


        else:
            self.subV_destruir()

    def verificacion_de_verificaciones(self):
        if self.veriFCH.fecha_guardada != None and self.verCOD.codigo_guardado != None and self.verCNT.cantidad_guardada != None and self.verCNT.unidad != None and self.verePRV.nombre_guardado != None:
            print(self.verCNT.unidad)
            instancia_comando = Botones()
            instancia_comando.escribe_lote(
                self.SV,
                self.veriFCH.fecha_guardada,
                self.verCOD.codigo_guardado,
                self.verCNT.cantidad_guardada,
                self.verCNT.unidad,
                self.verePRV.nombre_guardado,
                self.rutalotes
            )
        else:
            messagebox.showerror("Error", "Completa y Guarda todos los espacios para continuar")
        self.subV_destruir()


    def MA_vista(self,nombre=None, alto=None, ancho = None):
        if self.sv_open ==  False:
            self.subV_crear()
            instancia_comando = Botones()
            instancia_comando.visualizar_productos(self.SV)
        else:
            self.subV_destruir()

    def verlotes(self):
        if self.someopen==False and self.VTL_open == False:  # Si los botones no están abiertos
            self.someopen = True
            self.VTL_open =True  # Marcar como abiertos
            # Crear los botones que deseas mostrar
            self.lote_info_instance = LoteInfo(self.admin.frame_scroll)
            self.lote_info_instance.toggle_buttons()
        elif self.VTL_open == True:
            self.VTL_open = False
            self.someopen = False
            self.limpiar_frame_scroll()  # Crear los botones dentro de LoteInfo
        else:  # Si los botones ya están abiertos
            messagebox.showwarning("Advertencia", "No puedes avanzar si tienes un proceso abierto")


    def limpiar_frame_scroll(self):
        # Eliminar todos los widgets dentro de frame_scroll
        for widget in self.admin.frame_scroll.winfo_children():
            widget.destroy()



    def IPC(self, nombre=None, alto=None, ancho=None):
        if self.sv_open == False:
            self.subV_crear()  # Abre la ventana (subventana)
            
            # Crea una instancia de BotonesPE
            instancia_comando_pe = BotonesPE()
            
            # Llama a visualizar_productos para mostrar los productos de PE.txt
            instancia_comando_pe.visualizar_productos(self.SV)
        else:
            self.subV_destruir()

    def RDP(self,nombre= None, alto=None, ancho = None):
        if self.sv_open ==  False:
            self.subV_crear()
        else:
            self.subV_destruir()

    def PPO(self,nombre= None, alto=None, ancho = None):
        if self.sv_open ==  False:
            self.subV_crear()
            archivo_principal = os.path.join("LISTA PRODUCTO Y RECETAS", "COSECHA.txt")
            columnas=["Código", "Descripción", "Unidad", "Cantidad"]
            interfaz = InterfazGenerica(self.SV,archivo_principal,columnas)
        else:
            self.subV_destruir()

    def Botones_Desc(self, lado, lugar, padx=0, pady=0):
        if self.someopen == False and self.Descuentos_open == False:
            self.someopen = True
            self.Descuentos_open = True

            self.canvas = tk.Canvas(lugar, bg="yellow", width=lado, height=lado)
            self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=padx, pady=pady)

            self.label = tk.Label(self.canvas, text="Ingrese el descuento deseado", bg="yellow", fg="Black", font=("Helvetica", 20, "bold"))
            self.label.place(x=10, y=5)

            self.descuento = tk.Entry(self.canvas)
            self.descuento.place(x=10, y=50, width=lado-20)

            self.guardarDesc = tk.Button(self.canvas, text="Confirmar Descuento", bg="yellow", fg="black", font=("Helvetica"), command=lambda: self.Crear_Descuento(self.descuento.get()))
            self.guardarDesc.place(x=10, y=95)

        else:
            self.someopen = False
            self.Descuentos_open = False

            self.label.destroy()
            self.descuento.destroy()


            self.canvas.destroy()
            self.canvas = None

    def HDF(self,nombre= None, alto=None, ancho = None):
        if self.someopen ==  False and self.facturacion_open== False:
            self.someopen = True
            self.facturacion_open = True
            archivo_principal = os.path.join("HistorialFacturacion.txt")
            columnas=["Cliente", "Estado", "Metodfo de Pago", "total", "lugar de envio", "Fecha"]
            interfaz = InterfazGenerica(self.admin.frame_scroll,archivo_principal,columnas)
        elif self.facturacion_open ==True:
            self.limpiar_frame_scroll()
            self.someopen=False
            self.facturacion_open = False
        else:
            messagebox.showwarning("Advertencia", "No puedes avanzar si tienes un proceso abierto")


    def Crear_Descuento(self, Porcentaje_Descuento):
        self.descuento.delete(0, tk.END)
        self.escritor.limpiartxt("Descuento.txt")
        self.escritor.write("Descuento.txt", Porcentaje_Descuento)

    def GRC(self):
        if self.sv_open ==  False:
            self.subV_crear()
            recibo = ReciboCosecha(self.SV, "recibos_cosecha.txt")
        else:
            self.subV_destruir()

    def VRC(self):
        if self.someopen == False and self.VRC_open == False:  # Si no están abiertas las ventanas someopen y GRC_open
            self.someopen = True
            self.VRC_open = True
            archivo_recibo = os.path.join("recibos_cosecha.txt")
            columnas = ["Fcecha", "Provedor", "Producto", "cantidad"]  # Se mantienen las columnas de VRC
            interfaz = InterfazGenerica(self.admin.frame_scroll, archivo_recibo, columnas)
        elif self.VRC_open == True:
            self.limpiar_frame_scroll()
            self.someopen = False
            self.VRC_open = False
        else:
            messagebox.showwarning("Advertencia", "No puedes avanzar si tienes un proceso abierto")

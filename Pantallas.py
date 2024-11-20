from admin import Seccion
from TXTReader import LectorTXT
from WriterEnDocumento import Writer
from Producto import Product
from logic import Instacia_B
import tkinter as tk
from tkinter import messagebox
import os
from botones import Botones 
class Pantalla_add:
    def __init__(self, ventana, notebook, archivo_usuarios= os.path.join("RegistroCompras.txt"), archivo_recetas=None, archivo_lotes=None, usuario_log= None):
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
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        self.someopen = False
        self.frame_interno= None
        self.almacen_open = False
        self.sv_open = False
        self.SV = None
        
    def crear_menu(self):
        self.Us_math = self.lector.leerTxtFile(self.archivo_usuarios)
        # Crear el menú principal en la ventana
        self.menu_bar = tk.Menu(self.ventana)

        # Submenú para los productos (solo dentro de "Ventas")
        productos_menu = tk.Menu(self.menu_bar, tearoff=0)
        productos_menu.add_command(label="Crear Producto",)
        productos_menu.add_command(label="Quitar Producto")
        productos_menu.add_command(label="Modificar Producto")
        productos_menu.add_command(label="crear descueto")

        # Submenú Ventas
        ventas_menu = tk.Menu(self.menu_bar, tearoff=0)
        ventas_menu.add_cascade(label="Productos", menu=productos_menu)  # Agregar "Productos"

        # Submenú Administrativo dentro de Opciones de Admin
        administrativo_menu = tk.Menu(self.menu_bar, tearoff=0)
        administrativo_menu.add_command(label="Historiales" , command=lambda:self.crear_vista_Historial(500,self.admin.frame_scroll, 0,0))  # Solo "Historiales" en Administrativo
        administrativo_menu.add_command(label="Almacén", command=lambda:self.almacen(self.admin.frame_scroll, 10, 50,))
        administrativo_menu.add_command(label="Facturas")

        # Crear el menú "Opciones de Admin" y añadir los submenús
        opciones_admin_menu = tk.Menu(self.menu_bar, tearoff=0)
        opciones_admin_menu.add_cascade(label="Ventas", menu=ventas_menu)  # Agregar "Ventas"
        opciones_admin_menu.add_cascade(label="Administrativo", menu=administrativo_menu)  # Agregar "Administrativo"

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
                self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

            # Vincular el evento de desplazamiento del ratón al canvas
            self.canvas.bind_all("<MouseWheel>", scroll_canvas)  # Para sistemas Windows
            # self.canvas.bind_all("<Button-4>", scroll_canvas)  # Para sistemas Linux (si es necesario)
            # self.canvas.bind_all("<Button-5>", scroll_canvas)  # Para sistemas Linux (si es necesario)

            self.historial_open = True
            self.someopen = True
            self.crear_botones_historial()
        elif self.historial_open == True:
            # Si historial_open es True, eliminar la vista de historial actual
            if hasattr(self, 'canvas'):
                self.canvas.destroy()  # Elimina el Canvas
            if hasattr(self, 'frame_interno'):
                self.frame_interno.destroy()  # Elimina el Frame interno

            self.historial_open = False 
            self.someopen = False # Cambiar el estado para indicar que la vista ha sido cerrada
        else:
             messagebox.showwarning("Advertencia", "No puedes avanzar si tienes un proceso abierto")


    def crear_botones_historial(self):
        # Asegúrate de que la matriz está cargada y no está vacía
        if self.Us_math:
            nombres_agregados = set()  # Conjunto para almacenar nombres únicos

            # Recorrer cada línea en la matriz
            for linea in self.Us_math:
                # Verificar si el nombre (primer elemento) ya fue agregado
                nombre = linea[0]  # Asumimos que el nombre está en la posición 0
                if nombre not in nombres_agregados:
                    # Agregar el nombre al conjunto para evitar duplicados
                    nombres_agregados.add(nombre)
                    
                    # Crear el botón con el nombre único
                    # Cambia esta línea en la función crear_botones_historial
                    boton = tk.Button(self.frame_interno, text=f"{nombre}", width=self.lado_hiostorial // 10, command=lambda nombre=nombre: self.comando_botones_historial(nombre))

                    boton.pack(fill=tk.X, pady=5, padx=5)
        else:
            pass
    def extraer_historial(self, linea):
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
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind_all("<MouseWheel>", scroll_con_rueda)

        # Verifica si hay datos en Us_math
        if self.Us_math:
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
    
    def almacen(self, donde, pad_x, pad_y):
        if  self.almacen_open == False and self.someopen == False:
            # Crear los botones y almacenarlos en una lista para referencia
            self.botones = []

            self.agregarlotes = tk.Button(donde, width=self.ancho // 70, height=self.alto // 70, text="Agregar Lotes", command=lambda: self.agrega_lotes("LOTES", 500, 500))
            self.agregarlotes.grid(row=0, column=0, padx=pad_x, pady=pad_y)
            self.botones.append(self.agregarlotes)

            self.crearMA = tk.Button(donde, width=self.ancho // 70, height=self.alto // 70, text="Maestro de Artículos",command= self.MA_vista)
            self.crearMA.grid(row=0, column=1, padx=pad_x, pady=pad_y)
            self.botones.append(self.crearMA)

            self.craerIPC = tk.Button(donde, width=self.ancho // 70, height=self.alto // 70, text="Productos Comprados", command= self.IPC)
            self.craerIPC.grid(row=0, column=2, padx=pad_x, pady=pad_y)
            self.botones.append(self.craerIPC)

            self.creaRP = tk.Button(donde, width=self.ancho // 70, height=self.alto // 70, text="Registro de Producción", command= self.RDP)
            self.creaRP.grid(row=0, column=3, padx=pad_x, pady=pad_y)
            self.botones.append(self.creaRP)

            self.almacen_open = True  # Marcar que el almacén está abierto
            self.someopen = True

        elif self.almacen_open ==  True:
            # Eliminar los botones almacenados
            for boton in self.botones:
                boton.destroy()
                boton = None
            
            self.botones = []  # Vaciar la lista de botones
            self.almacen_open = False  # Marcar que el almacén está cerrado
            self.someopen = False
        else:
             messagebox.showwarning("Advertencia", "No puedes avanzar si tienes un proceso abierto")

    
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

    def agrega_lotes(self, nombre=None, alto=None, ancho=None):
        if not self.sv_open:
            self.subV_crear(nombre, alto, ancho)
            
            # Obtener dimensiones de la ventana
            self.SV.update_idletasks()
            width = self.SV.winfo_width()
            height = self.SV.winfo_height()

            # Margenes y espaciado
            margin_top = 20
            margin_left = 20
            spacing = 40
            
            # Campos para el formulario
            tk.Label(self.SV, text="Nombre del producto:").place(
                x=margin_left, y=margin_top)
            Entry_nombre = tk.Entry(self.SV)
            Entry_nombre.place(
                x=margin_left + 200, y=margin_top)
            
            tk.Label(self.SV, text="Cantidad:").place(
                x=margin_left, y=margin_top + spacing)
            Entry_cantidad = tk.Entry(self.SV)
            Entry_cantidad.place(
                x=margin_left + 200, y=margin_top + spacing)
            
            tk.Label(self.SV, text="Fecha de caducidad (YYYY-MM-DD):").place(
                x=margin_left, y=margin_top + spacing * 2)
            Entry_fecha_caducidad = tk.Entry(self.SV)
            Entry_fecha_caducidad.place(
                x=margin_left + 250, y=margin_top + spacing * 2)
            
            tk.Label(self.SV, text="Proveedor:").place(
                x=margin_left, y=margin_top + spacing * 3)
            Entry_proveedor = tk.Entry(self.SV)
            Entry_proveedor.place(
                x=margin_left + 200, y=margin_top + spacing * 3)
            
            # Botón de "Listo"
            tk.Button(self.SV, text="Listo").place(
                x=(width // 2) - 40, y=margin_top + spacing * 4)



        else:
            self.subV_destruir()

    def MA_vista(self,nombre=None, alto=None, ancho = None):
        if self.sv_open ==  False:
            self.subV_crear()
            instancia_comando = Botones()
            instancia_comando.visualizar_productos(self.SV)
        else:
            self.subV_destruir()


    def IPC(self,nombre= None, alto=None, ancho = None):
        if self.sv_open ==  False:
            self.subV_crear()
        else:
            self.subV_destruir()

    def RDP(self,nombre= None, alto=None, ancho = None):
        if self.sv_open ==  False:
            self.subV_crear()
        else:
            self.subV_destruir()
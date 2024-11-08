from admin import Seccion
from TXTReader import LectorTXT
from WriterEnDocumento import Writer
from Producto import Product
from logic import Instacia_B
import tkinter as tk

class Pantalla_add:
    def __init__(self, ventana, notebook, archivo_usuarios=None, archivo_recetas=None, archivo_lotes=None):
        self.ventana = ventana
        self.notebook = notebook
        self.archivo_usuarios = archivo_usuarios
        self.archivo_recetas = archivo_recetas
        self.archivo_lotes = archivo_lotes
        self.admin = None
        self.ancho = self.ventana.winfo_screenwidth()
        self.alto = self.ventana.winfo_screenheight()
        self.historial_open = False
        
    def crear_menu(self):
        # Crear el menú principal en la ventana
        self.menu_bar = tk.Menu(self.ventana)

        # Submenú para los productos (solo dentro de "Ventas")
        productos_menu = tk.Menu(self.menu_bar, tearoff=0)
        productos_menu.add_command(label="Crear Producto")
        productos_menu.add_command(label="Quitar Producto")
        productos_menu.add_command(label="Modificar Producto")
        productos_menu.add_command(label="crear descueto")

        # Submenú Ventas
        ventas_menu = tk.Menu(self.menu_bar, tearoff=0)
        ventas_menu.add_cascade(label="Productos", menu=productos_menu)  # Agregar "Productos"

        # Submenú Administrativo dentro de Opciones de Admin
        administrativo_menu = tk.Menu(self.menu_bar, tearoff=0)
        administrativo_menu.add_command(label="Historiales" , command=lambda:self.crear_vista_Historial(500,self.admin.frame_scroll, 0,0))  # Solo "Historiales" en Administrativo
        administrativo_menu.add_command(label="Almacén")
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
        if self.historial_open == False:
            # Crear el canvas y configurarlo para llenarse dentro del lugar especificado
            self.canvas = tk.Canvas(lugar, bg="lightblue", width=lado, height=lado)
            self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=padx, pady=pady)

            # Configurar el canvas para que use el desplazamiento con el ratón
            self.canvas.config(scrollregion=(0, 0, lado, lado * 2))  # Ajustar la altura del scroll para simular más espacio hacia abajo

            # Crear un frame interno para colocar los botones dentro del canvas
            self.frame_interno = tk.Frame(self.canvas, bg="lightblue")
            self.canvas.create_window((0, 0), window=self.frame_interno, anchor="nw")

            # Agregar botones en el frame_interno para probar el scroll vertical
            for i in range(50):  # Agregar 50 botones verticalmente
                boton = tk.Button(self.frame_interno, text=f"{i+1}) usuario ", width=lado // 10)
                boton.pack(fill=tk.X, pady=5, padx=5)

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
        else:
            # Si historial_open es True, eliminar la vista de historial actual
            if hasattr(self, 'canvas'):
                self.canvas.destroy()  # Elimina el Canvas
            if hasattr(self, 'frame_interno'):
                self.frame_interno.destroy()  # Elimina el Frame interno

            self.historial_open = False  # Cambiar el estado para indicar que la vista ha sido cerrada

    def reiniciar_pantalla(self):
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





    def accion_boton(self):
        print("Botón de ejemplo presionado.")

    def abrir_archivo(self):
        # Lógica para abrir un archivo (placeholder)
        print("Abrir archivo seleccionado")

    def guardar_archivo(self):
        # Lógica para guardar un archivo (placeholder)
        print("Guardar archivo seleccionado")

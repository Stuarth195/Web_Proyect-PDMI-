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
        administrativo_menu.add_command(label="Historiales")  # Solo "Historiales" en Administrativo
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

        # Crear un botón en el frame de desplazamiento de la sección
        self.diego = tk.Button(self.admin.frame_scroll, text="Botón de ejemplo", command=self.accion_boton)
        self.diego.pack(padx=10, pady=1000)

        # Crear otros elementos en el frame según tus necesidades
        etiqueta = tk.Label(self.admin.frame_scroll, text="Etiqueta en pantalla oculta", bg="lightgray")
        etiqueta.pack(pady=20)
        
        entrada = tk.Entry(self.admin.frame_scroll)
        entrada.pack(pady=10)

        

    def accion_boton(self):
        print("Botón de ejemplo presionado.")

    def abrir_archivo(self):
        # Lógica para abrir un archivo (placeholder)
        print("Abrir archivo seleccionado")

    def guardar_archivo(self):
        # Lógica para guardar un archivo (placeholder)
        print("Guardar archivo seleccionado")

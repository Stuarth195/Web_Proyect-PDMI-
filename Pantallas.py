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
        
        # Crear el menú principal en self.ventana
        self.crear_menu()

    def crear_menu(self):
        # Crear el menú principal en la ventana
        self.menu_bar = tk.Menu(self.ventana)
        
        # Submenú Archivo
        archivo_menu = tk.Menu(self.menu_bar, tearoff=0)
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.ventana.quit)
        
        # Submenú Edición
        edicion_menu = tk.Menu(self.menu_bar, tearoff=0)
        edicion_menu.add_command(label="Copiar")
        edicion_menu.add_command(label="Pegar")
        
        # Submenú Ayuda
        ayuda_menu = tk.Menu(self.menu_bar, tearoff=0)
        ayuda_menu.add_command(label="Acerca de")
        
        # Añadir submenús al menú principal
        self.menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        self.menu_bar.add_cascade(label="Edición", menu=edicion_menu)
        self.menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)
        
        # Configurar el menú en la ventana principal
        self.ventana.config(menu=self.menu_bar)

    def pantalla_oculta(self, nombre):
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

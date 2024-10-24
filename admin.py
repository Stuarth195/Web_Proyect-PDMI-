import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Seccion:
    def __init__(self,frame,notebook, alto_canva, ancho_canva, canva, canva_color):
        self.frame = frame
        self.notebook = notebook
        self.ancho = ancho_canva
        self.alto = alto_canva
        self.canva = canva
        self.C_color = canva_color
        

    def crear(self, nombre):
        # Crea un frame simple dentro del notebook
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text=nombre)  # nombre se usa como el texto de la pestaña
        # Crear y colocar el Canvas

    def mas_canva(self,):
        self.canva = tk.Canvas(self.frame, width=self.ancho, height=self.alto, bg= self.C_color)
        self.canva.place(x=0, y=0)

    def crear_si(self, arg1, arg2, ver1, ver2, nombre, mensaje_error="datos no válido"):
        # Verifica si los argumentos coinciden antes de crear el frame
        if arg1 == ver1 and arg2 == ver2:
            self.crear(nombre)
        else:
            messagebox.showerror("Error", mensaje_error)


#class Poppop:
 #   def __init__(self, ventana):
  #      self.ventana= ventana
#
 #   def error(self, texto):


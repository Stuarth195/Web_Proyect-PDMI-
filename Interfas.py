import tkinter as tk # importa tkinter bajo la abreviatura tk
from tkinter import ttk
import os
from admin import Seccion
def Interfaz():

    alto = 900
    ancho = 1800
    ruta_ico_chrome = os.path.join('Imagenes', 'icono_g.ico')
    titulo = "Chrome"
    color_fondo ="blue"
    canva1=None
    frame1 = "fee"
    App = tk.Tk()
    App.title(titulo)
    App.geometry(f'{ancho}x{alto}')
    App.iconbitmap(ruta_ico_chrome)

    Visual_feed = ttk.Notebook(App)
    Visual_feed.pack(fill="both", expand="yes")
    feed = Seccion(frame1, Visual_feed,alto , ancho, canva1, color_fondo)
    feed.crear("page1")
    feed.mas_canva()
    



























    App.mainloop()

Interfaz()
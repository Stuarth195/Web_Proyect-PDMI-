import tkinter as tk
from tkinter import ttk
from admin import Seccion  # Asegúrate de importar la clase correctamente

def Interfaz():
    alto = 900
    ancho = 1800
    titulo = "Chrome"
    color_fondo = "pink"

    App = tk.Tk()
    App.title(titulo)
    App.geometry(f'{ancho}x{alto}')
    App.resizable(0, 0)

    # Crear el notebook donde se agregarán las pestañas
    Visual_feed = ttk.Notebook(App)
    Visual_feed.pack(fill="both", expand=True)

    # Crear una sección y añadirla como pestaña en el notebook
    feed = Seccion(Visual_feed, alto, ancho, color_fondo)
    feed.crear("page1")

    # Crear un botón en la esquina superior izquierda del Frame
    bton = tk.Button(feed.frame_scroll, text="Botón en la esquina", command=lambda: print("Botón presionado"))
    bton.pack(side="top", padx=0, pady=2000)  # Botón sin espaciado

    # Crear un espacio vacío para permitir el scroll (ajusta la altura según sea necesario)
    spacer = tk.Frame(feed.frame_scroll, height=800, bg=color_fondo)
    spacer.pack()
    
    espacio_config = tk.Canvas(feed.canva, width= ancho, height= 20, bg = "salmon")
    espacio_config.place(x=0,y=0)

    # Actualizar la región de scroll para incluir el contenido
    feed.frame_scroll.update_idletasks()
    feed.canva.config(scrollregion=feed.canva.bbox("all"))

    App.mainloop()

Interfaz()

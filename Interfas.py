import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from admin import Seccion  # Asegúrate de importar la clase correctamente
from logic import Instacia_B
from PIL import Image, ImageTk
import os


def Interfaz():


    instancia_base = None
    instancia_base = Instacia_B()

    # Crea una ruta relativa combinando carpetas o archivos.
    #    Esta ruta es relativa al directorio actual
    icono_c= os.path.join("Imagenes", "Logo_AU.ico")

    alto = 1000
    ancho = 1800
    titulo = "AgroAPP"
    Rojo = "#B90519"
    verde= "#17820E"
    naraja= "#DC8002"
    amarillo= "#FCC509"

    color_fondo = "#dcdcdc"
    App = tk.Tk()
    App.title(titulo)
    App.geometry(f'{ancho}x{alto}')
    App.resizable(0, 0)
    App.iconbitmap(icono_c)




    #parte de conexion con la base de dotos 

    try:
        instancia_base.conecting()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a Google Drive: {e}")





    #imagenes para la interfaz


    baner = Image.open(os.path.join("Imagenes", "Baner.png"))
    baner_img = ImageTk.PhotoImage(baner)

    producto1 = Image.open(os.path.join("Imagenes", "productos", "papas_dibujo.png"))
    producto_img= ImageTk.PhotoImage(producto1)


    # Crear el notebook donde se agregarán las pestañas

    Visual_feed = ttk.Notebook(App)
    Visual_feed.pack(fill="both", expand=True)

    # Crear una sección y añadirla como pestaña en el notebook
    feed = Seccion(Visual_feed, alto, ancho, color_fondo)
    feed.crear("Corporacion De Agricultores Unidos")


    # Actualizar la región de scroll para incluir el contenido
    feed.frame_scroll.update_idletasks()
    feed.canva.config(scrollregion=feed.canva.bbox("all"))

    # Crear un botón en la esquina superior izquierda del Frame
    # Crear un botón con imagen en la esquina superior izquierda del Frame
    bton = tk.Button(feed.frame_scroll, image=producto_img, text="Botón en la esquina", command=lambda: print("Botón presionado"))
    bton.pack(side="top", padx= 100, pady=1000)  # Ajuste del botón sin espaciado



    espacio_config = tk.Label(feed.canva, image= baner_img)
    espacio_config.place(x=0,y=0)

    feed2 = Seccion(Visual_feed, alto, ancho, "blue")
    feed2.crear("pagina2")

    feed2.frame_scroll.update_idletasks()
    feed2.canva.config(scrollregion=feed.canva.bbox("all"))


    bton2 = tk.Button(feed2.frame_scroll, text="Botón en la esquina", command=lambda: print("Botón presionado"))
    bton2.pack(side="top", padx=0, pady=2000)  # Botón sin espaciado


    App.mainloop()

Interfaz()

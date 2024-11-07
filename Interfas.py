import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from admin import Seccion  # Asegúrate de importar la clase correctamente
from logic import Instacia_B
from PIL import Image, ImageTk
import os
from ImageSizeAjs import AJS
from TXTReader import LectorTXT
from RevUsuarios import revUsuarios
from Registro import Emergente
from Producto import Product
import random


def Interfaz():


    instancia_base = None
    instancia_base = Instacia_B()

    # Crea una ruta relativa combinando carpetas o archivos.
    #    Esta ruta es relativa al directorio actual
    icono_c= os.path.join("Imagenes", "Logo_AU.ico")

    titulo = "AgroAPP"
    Rojo = "#B90519"
    verde= "#17820E"
    naraja= "#DC8002"
    amarillo= "#FCC509"

    color_fondo = "#dcdcdc"
    App = tk.Tk()

    ancho_pantalla = App.winfo_screenwidth()
    alto_pantalla = App.winfo_screenheight()

    margen_anchoP = ancho_pantalla//50
    margen_altoP = alto_pantalla//50

    AjustadorTam = AJS(ancho_pantalla, alto_pantalla)

    Lector = LectorTXT()

    App.title(titulo)
    App.geometry(f'{ancho_pantalla}x{alto_pantalla}')
    App.resizable(False, False)
    App.iconbitmap(icono_c)




    #parte de conexion con la base de dotos 

    try:
        instancia_base.conecting()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a Google Drive: {e}")





    #imagenes para la interfaz


    baner = Image.open(os.path.join("Imagenes", "Baner.png"))

    baner = AjustadorTam.ajustarIMG(baner, 1)

    baner_img = ImageTk.PhotoImage(baner)

    producto1 = Image.open(os.path.join("Imagenes", "productos", "papas_dibujo.png"))
    producto1 = AjustadorTam.ajustarIMG(producto1, 0.05)
    producto_img= ImageTk.PhotoImage(producto1)


    # Crear el notebook donde se agregarán las pestañas

    Visual_feed = ttk.Notebook(App)
    Visual_feed.pack(fill="both", expand=True)

    # Crear una sección y añadirla como pestaña en el notebook
    feed = Seccion(Visual_feed, alto_pantalla, ancho_pantalla, color_fondo)
    feed.crear("Corporacion De Agricultores Unidos")


    # Actualizar la región de scroll para incluir el contenido
    feed.frame_scroll.update_idletasks()
    feed.canva.config(scrollregion=feed.canva.bbox("all"))

    # Crear un botón en la esquina superior izquierda del Frame
    # Crear un botón con imagen en la esquina superior izquierda del Frame
    # Ajuste del botón sin espaciado

    REGIST = Emergente(App, margen_anchoP, margen_altoP)
    Btn_Register = tk.Button(feed.canva, text="Log In", command=lambda: REGIST.registro())
    Btn_Register.place(x=0, y=0)

    espacio_config = tk.Label(feed.canva, image = baner_img)
    espacio_config.place(x=0,y = margen_altoP*1.5)


    feed2 = Seccion(Visual_feed, alto_pantalla, ancho_pantalla, "blue")
    feed2.crear("pagina2")

    feed2.frame_scroll.update_idletasks()
    feed2.canva.config(scrollregion=feed.canva.bbox("all"))

    bton2 = tk.Button(feed2.frame_scroll, text="Botón en la esquina", command=lambda: print("Botón presionado"))
    bton2.pack(padx=margen_anchoP * 20, pady=margen_altoP)  # Botón sin espaciado


    P1 = Product(feed.frame_scroll, margen_anchoP, margen_altoP)
    i = 0
    xP = margen_anchoP
    yP = margen_altoP
    canvas_count = 0
    frame = tk.Frame(feed.frame_scroll)
    frame.pack(padx=margen_anchoP//2, pady=margen_altoP*12)
    while i < 12:
        i = i + 1
        PrecioR = random.randrange(1, 100)
        P1.mostrarImagen(producto_img, "Papa", str(PrecioR), xP, yP, frame, canvas_count)
        canvas_count = canvas_count + 1
        if canvas_count == 6:
            canvas_count = 0

    App.mainloop()

Interfaz()

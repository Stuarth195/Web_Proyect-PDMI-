import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from admin import Seccion
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
    instancia_base = Instacia_B()

    icono_c = os.path.join("Imagenes", "Logo_AU.ico")
    titulo = "AgroAPP"
    Rojo = "#B90519"
    verde = "#17820E"
    naraja = "#DC8002"
    amarillo = "#FCC509"
    color_fondo = "#dcdcdc"
    
    App = tk.Tk()
    ancho_pantalla = App.winfo_screenwidth()
    alto_pantalla = App.winfo_screenheight()
    margen_anchoP = ancho_pantalla // 50
    margen_altoP = alto_pantalla // 50
    AjustadorTam = AJS(ancho_pantalla, alto_pantalla)
    Lector = LectorTXT()

    App.title(titulo)
    App.geometry(f'{ancho_pantalla}x{alto_pantalla}')
    App.resizable(False, False)
    App.iconbitmap(icono_c)

    try:
        instancia_base.conecting()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a Google Drive: {e}")

    # Imagen de banner para la interfaz
    baner = Image.open(os.path.join("Imagenes", "Baner.png"))
    baner = AjustadorTam.ajustarIMG(baner, 1)
    baner_img = ImageTk.PhotoImage(baner)

    producto1 = Image.open(os.path.join("Imagenes", "productos", "papas_dibujo.png"))
    producto1 = AjustadorTam.ajustarIMG(producto1, 0.05)
    producto_img = ImageTk.PhotoImage(producto1)

    # Crear el notebook donde se agregarán las pestañas
    Visual_feed = ttk.Notebook(App)
    Visual_feed.pack(fill="both", expand=True)

    # Crear una sección y añadirla como pestaña en el notebook
    feed = Seccion(Visual_feed, alto_pantalla, ancho_pantalla, color_fondo)
    feed.crear("Corporacion De Agricultores Unidos")

    # Ajustar la región de scroll del Canvas
    feed.frame_scroll.update_idletasks()
    feed.canva.config(scrollregion=feed.canva.bbox("all"))

    # Configurar los eventos de teclado para desplazarse con flechas
    feed.canva.bind("<Up>", feed.scroll_up)
    feed.canva.bind("<Down>", feed.scroll_down)
    feed.canva.focus_set()  # Asegurar que el Canvas tenga el enfoque para capturar las teclas

    espacio_config = tk.Label(feed.canva, image=baner_img)
    espacio_config.place(x=0, y=0)

    # Crear un botón con imagen en la esquina superior izquierda del Frame
    REGIST = Emergente(App, margen_anchoP, margen_altoP, Visual_feed)
    Btn_Register = tk.Button(feed.canva, text="Log In", bg= amarillo, width= margen_anchoP, height= margen_altoP // 3 , command=lambda: REGIST.registro())
    Btn_Register.place(x=1600, y=20)



    # Crear productos en el frame de scroll
    P1 = Product(feed.frame_scroll, margen_anchoP, margen_altoP)
    i = 0
    xP = margen_anchoP
    yP = margen_altoP
    canvas_count = 0
    frame = tk.Frame(feed.frame_scroll)
    frame.pack(padx=margen_anchoP//2, pady=margen_altoP*12)
    
    while i < 30:
        i += 1
        PrecioR = random.randrange(1, 100)
        P1.mostrarImagen(producto_img, "Papa", str(PrecioR), xP, yP, frame, canvas_count)
        canvas_count += 1
        if canvas_count == 6:
            canvas_count = 0

    App.mainloop()

Interfaz()

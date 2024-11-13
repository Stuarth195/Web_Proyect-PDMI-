import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from admin import Seccion
from logic import Instacia_B
from PIL import Image, ImageTk
import os
from ImageSizeAjs import AJS
from TXTReader import LectorTXT
from Carrito import MCarrito
from Registro import Emergente
from Producto import Product
import random

def Interfaz():
    instancia_base = Instacia_B()
    #rutas de descarga
    ruta_defecto= os.path.join("Web_Proyect-PDMI-")
    #ids de los archivos
    id_usuarios= "1VC7trYLyHziTpeFfH5K8gsSW3k8xKSLh"
    id_admins= "1j--oyLkPszHwCyUqV4H-ySb_XNxzP2Dz"
    id_carrito="1D-Vm_10a2UtLsARG0ZA5sLi7Q2KXMFnn"
    id_productos="18k2JcSh1Q2gZj065ASOeNLrBTLQSOv5n"
    id_registroC = "1B0YTc-MnKXk9pKNfOzuLgRotYtmEpD23"
    id_receta = None



    icono_c = os.path.join("Imagenes", "Logo_AU.ico")
    titulo = "AgroAPP"
    Rojo = "#B90519"
    verde = "#17820E"
    naraja = "#DC8002"
    amarillo = "#FCC509"
    color_fondo = "#dcdcdc"

    try:
        instancia_base.conecting()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a Google Drive: {e}")
    
    instancia_base.download_A(id_admins , ruta_defecto)
    instancia_base.download_A(id_carrito , ruta_defecto)
    instancia_base.download_A(id_productos, ruta_defecto)
    instancia_base.download_A(id_usuarios , ruta_defecto)
    instancia_base.download_A(id_registroC , ruta_defecto)


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



    # Imagen de banner para la interfaz
    baner = Image.open(os.path.join("Imagenes", "Baner.png"))
    baner = AjustadorTam.ajustarIMG(baner, 1)
    baner_img = ImageTk.PhotoImage(baner)


    p1 =os.path.join("Imagenes", "productos", "papas_dibujo.png")

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
    REGIST = Emergente(App,feed.canva, margen_anchoP, margen_altoP, Visual_feed)

    # Construir la ruta de la imagen usando os.path.join
    ruta_imagen = os.path.join("imagenes", "boton_register.png")

    # Cargar la imagen
    boton_register_img = PhotoImage(file=ruta_imagen)

    # Crear el botón con la imagen
    Btn_Register = tk.Button(feed.canva, image=boton_register_img, command=lambda: REGIST.registro())
    Btn_Register.place(x=margen_anchoP*45, y=margen_altoP*2)
    
    Car = MCarrito()

    Btn_Carrito = tk.Button(feed.canva, text="Carrito", command=lambda:Car.Mostrar_Carrito(REGIST.getUsername()))
    Btn_Carrito.place(x=margen_anchoP * 45, y=margen_altoP * 6)

    # Crear productos en el frame de scroll
    P1 = Product(App, feed.frame_scroll, margen_anchoP, margen_altoP)
    i = 0
    xP = margen_anchoP
    yP = margen_altoP
    canvas_count = 0
    frame = tk.Frame(feed.frame_scroll)
    frame.pack(padx=margen_anchoP//2, pady=margen_altoP*12)

    while i < 12:
        i += 1
        PrecioR = random.randrange(1, 100)
        P1.mostrarImagen(producto_img, "Papa", str(PrecioR), xP, yP, frame, canvas_count, str(32), "PA0000", "asdadsa", p1)
        canvas_count += 1
        if canvas_count == 7:
            canvas_count = 0



    App.mainloop()

Interfaz()

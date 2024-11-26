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
import re
import sys
class Visual:
    def __init__(self):
        self.usuarios_txt = "1H_eK_sheQeS-F5BeJH0fBsr1sp_dPKVq"
        self.registro_compras_txt = "1DKo4evwlAow4FvwZKwKqCgzzCjKmei_R"
        self.recibos_cosecha_txt = "1Xzu9n_GvC2Dzsh81rQRpSCb6z8dcSqz8"
        self.p_ty_txt = "1rkG7ENvohQvs2_g9N8aP5VQgWPLd2JSS"
        self.p_txt = "1o4I0Nq9-_nvadR4vjhxW7uBVOyHnhR20"
        self.historial_facturacion_txt = "1JbCyELPiUJs3dnyjm8Aiagpm0lE1rBcm"
        self.descuento_txt = "1H8UjFu9uTMzk1k79Bmab9TDSikL3dwSw"
        self.carrito_txt = "1EuUKbAImYMm4L2KW3aUUrQaufL2ddHPM"
        self.admins_txt = "1pe21CvSFMz-jaxKaaj3ynb_tgJwLrGb-"
        self.lista_producto_y_recetas = "1K_PsCWRXs6pI8UZwyVrPLync02QdTUQA"
        self.Imagenes = "1vIgA69_T7Kstp6WuqEZCpU6EXFJeVfGf"
        self.instancia_base = Instacia_B()
        self.RutaImagenes =os.path.join("Imagenes")
        self.RutaVarios =os.path.join("LISTA PRODUCTO Y RECETAS")
        

    def descargar_todo(self):
        try:
            # Descargar la carpeta "Imagenes" y su contenido
            self.instancia_base.descargar_carpeta(self.Imagenes)
            print("Carpeta 'Imagenes' descargada exitosamente.")

            # Descargar la carpeta "LISTA PRODUCTO Y RECETAS" y su contenido
            self.instancia_base.descargar_carpeta(self.lista_producto_y_recetas)
            print("Carpeta 'LISTA PRODUCTO Y RECETAS' descargada exitosamente.")
        except Exception as e:
            # Manejar errores globales
            messagebox.showerror("Error", f"Error al descargar carpetas: {e}")
            raise e  # Para detener cualquier flujo adicional si es necesario
        
    def descargar_txt(self):
        try:
            # Descargar los archivos .txt desde el directorio actual
            self.instancia_base.descargar_archivo(self.usuarios_txt)
            self.instancia_base.descargar_archivo(self.registro_compras_txt)
            self.instancia_base.descargar_archivo(self.recibos_cosecha_txt)
            self.instancia_base.descargar_archivo(self.p_ty_txt)
            self.instancia_base.descargar_archivo(self.p_txt)
            self.instancia_base.descargar_archivo(self.historial_facturacion_txt)
            self.instancia_base.descargar_archivo(self.descuento_txt)
            self.instancia_base.descargar_archivo(self.carrito_txt)
            self.instancia_base.descargar_archivo(self.admins_txt)
            self.instancia_base.descargar_archivo(self.lista_producto_y_recetas)
            print("Archivos .txt descargados exitosamente.")
        except Exception as e:
            print(f"Error al descargar archivos .txt: {e}")
            raise e


    def actualiza(self):
        # Actualizar carpeta 'Imagenes' con el contenido de la ruta local
        self.instancia_base.actualizar_carpeta(self.Imagenes, self.RutaImagenes)

        # Actualizar carpeta 'LISTA PRODUCTO Y RECETAS' con el contenido de la ruta local
        self.instancia_base.actualizar_carpeta(self.lista_producto_y_recetas, self.RutaVarios)


    def Interfaz(self):
        # Intentar conectar a Google Drive
        try:
            self.instancia_base.conecting()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a Google Drive: {e}")
            sys.exit()  # Detener la ejecución si no se puede conectar

        # Descargar los archivos utilizando los métodos actualizados
        try:
            print("hola")
            #instancia_base.descargar_archivo(id_admins)
            #instancia_base.descargar_archivo(id_carrito)
            #instancia_base.descargar_archivo(id_productos)
            #instancia_base.descargar_archivo(id_usuarios)
            #instancia_base.descargar_archivo(id_registroC)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al descargar los archivos: {e}")
            sys.exit()  # Detener la ejecución si falla alguna descarga

        



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

        # Imagen de banner para la interfaz
        baner = Image.open(os.path.join("Imagenes", "Baner.png"))
        baner = AjustadorTam.ajustarIMG(baner, 1)
        baner_img = ImageTk.PhotoImage(baner)

        p1 = os.path.join("Imagenes", "productos", "papas_dibujo.png")

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
        REGIST = Emergente(App, feed.canva, margen_anchoP, margen_altoP, Visual_feed)

        # Construir la ruta de la imagen usando os.path.join
        ruta_imagen = os.path.join("imagenes", "boton_register.png")

        # Cargar la imagen
        boton_register_img = PhotoImage(file=ruta_imagen)

        # Crear el botón con la imagen
        Btn_Register = tk.Button(feed.canva, image=boton_register_img, command=lambda: REGIST.registro())
        Btn_Register.place(x=margen_anchoP * 45, y=margen_altoP * 2)

        Car = MCarrito(App)

        Btn_Carrito = tk.Button(feed.canva, text="Carrito", command=lambda: Car.Mostrar_Carrito(REGIST.getUsername()))
        Btn_Carrito.place(x=margen_anchoP * 45, y=margen_altoP * 6)

        # Crear productos en el frame de scroll
        P1 = Product(App, feed.frame_scroll, margen_anchoP, margen_altoP)
        Des = 1
        Iimagen = 0
        xP = margen_anchoP
        yP = margen_altoP *2
        canvas_count = 0
        frame = tk.Frame(feed.frame_scroll)
        frame.pack(padx=margen_anchoP, pady=margen_altoP * 12)
        listaImagenes = []
        listaPathImagenes = []

        prod = Lector.leerTxtFile("LISTA PRODUCTO Y RECETAS/M_A.txt")
        desc = Lector.leerTxtFile("Descuento.txt")
        for fila in desc:
            for i in fila:
                if i != "":
                    try:
                        Des = (100 - int(i)) / 100
                    except ValueError:
                        print("No es un numero")

        for produc in prod:
            producto1 = Image.open(os.path.join("Imagenes", "productos", produc[0] + ".png"))
            producto2 = AjustadorTam.ajustarIMG(producto1, 0.14)
            producto1 = AjustadorTam.ajustarIMG(producto1, 0.17)
            producto_img = ImageTk.PhotoImage(producto1)
            producto_img2 = ImageTk.PhotoImage(producto2)
            listaImagenes.append(producto_img)
            listaPathImagenes.append(producto_img2)


        for produ in prod:
            if produ != []:
                nombreProd = re.findall(r'\((.*?)\)', produ[1])
                if nombreProd == [] or nombreProd[0] == "kg":
                    precio = round(int(produ[5]) * Des, 2)
                    P1.mostrarImagen(listaImagenes[Iimagen], produ[1], str(precio), xP, yP, frame, canvas_count, produ[3], produ[0],
                                    produ[2], listaPathImagenes[Iimagen])
                else:
                    precio = round(int(produ[5]) * Des, 2)
                    P1.mostrarImagen(listaImagenes[Iimagen], nombreProd[0], str(precio), xP, yP, frame, canvas_count, produ[3], produ[0],
                                    produ[2], listaPathImagenes[Iimagen])
                canvas_count += 1
                Iimagen+=1
                if canvas_count == 4:
                    canvas_count = 0

        App.mainloop()

Aplicacion = Visual()
Aplicacion.Interfaz()





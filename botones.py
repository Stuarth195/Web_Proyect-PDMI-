from TXTReader import LectorTXT
import os
import tkinter as tk
from tkinter import Label, Button, Toplevel
from tkinter import Toplevel
from tkinter import Label, Button
from PIL import Image, ImageTk  # Importar Pillow para manejar imágenes

class Botones:
    def __init__(self, archivo_MA=os.path.join("LISTA PRODUCTO Y RECETAS", "M_A.txt"), 
                 archivo_PE=os.path.join("LISTA PRODUCTO Y RECETAS", "PE.txt"), 
                 archivo_Receta=os.path.join("LISTA PRODUCTO Y RECETAS", "Receta.txt"), 
                 archivo_cosecha=os.path.join("LISTA PRODUCTO Y RECETAS", "COSECHA.txt"), 
                 archivo_lotes =os.path.join("LISTA PRODUCTO Y RECETAS", "Lotes.txt")):
        # Instanciamos el lector de archivos
        self.Lector = LectorTXT()
        self.archivo_MA = archivo_MA
        self.archivo_PE = archivo_PE
        self.archivo_Receta = archivo_Receta
        self.archivo_cosecha = archivo_cosecha
        self.archivo_lotes = archivo_lotes

    def actualizar_cantidades(self):
        """
        Actualiza las cantidades totales de productos en el archivo M_A.txt 
        sumando las cantidades de los lotes correspondientes en el archivo Lotes.txt.
        """
        # Leer los datos de M_A y Lotes
        matriz_MA = self.Lector.leerTxtFilenUM(self.archivo_MA)
        matriz_lotes = self.Lector.leerTxtFilenUM(self.archivo_lotes)

        # Crear un diccionario para acumular las cantidades por código de producto
        cantidades_totales = {}

        # Recorrer la matriz de lotes y sumar las cantidades
        for fila in matriz_lotes:
            codigo_producto = fila[1]  # Código de producto en segunda posición
            cantidad = int(fila[-1])   # Cantidad en la última posición
            if codigo_producto in cantidades_totales:
                cantidades_totales[codigo_producto] += cantidad
            else:
                cantidades_totales[codigo_producto] = cantidad

        # Actualizar las cantidades en la matriz M_A
        for fila in matriz_MA:
            codigo_producto = fila[0]  # Código de producto en primera posición
            if codigo_producto in cantidades_totales:
                fila[3] = str(cantidades_totales[codigo_producto])  # Actualizar la cantidad (cuarta posición)

        # Escribir la matriz actualizada en M_A.txt
        with open(self.archivo_MA, "w") as archivo:
            for fila in matriz_MA:
                archivo.write(" ".join(fila) + "\n")

    def visualizar_productos(self, ventana):
        """
        Muestra un botón por cada producto en M_A. Al hacer clic, se despliega una ventana
        con la información del producto y espacio para una imagen.
        """
        # Leer los productos desde el archivo M_A
        matriz_MA = self.Lector.leerTxtFilenUM(self.archivo_MA)

        # Crear un marco de desplazamiento para contener los botones
        frame = tk.Frame(ventana)
        frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Crear botones para cada producto
        for producto in matriz_MA:
            codigo = producto[0]
            nombre = producto[1]
            descripcion = producto[2]
            cantidad = producto[3]

            # Crear botón
            boton = Button(scrollable_frame, text=f"{nombre}", command=lambda p=producto: self.mostrar_detalle_producto(p))
            boton.pack(pady=5, padx=10, fill="x")

    def mostrar_detalle_producto(self, producto):
        self.actualizar_cantidades
        """
        Muestra una ventana con los detalles del producto y un espacio para una imagen.
        """
        # Desempaquetar datos del producto
        codigo, nombre, descripcion, cantidad, unidad_medida, precio = producto

        # Crear la ventana de detalle
        ventana_detalle = Toplevel()
        ventana_detalle.title(f"Detalles de {nombre}")

        # Ruta de la imagen (se espera que las imágenes estén en 'Imagenes/Productos')
        ruta_imagen = os.path.join("Imagenes", "Productos", f"{codigo}.png")

        # Intentar cargar la imagen
        try:
            imagen = Image.open(ruta_imagen)
            imagen.thumbnail((200, 200))  # Redimensionar la imagen para que no sea demasiado grande
            imagen_tk = ImageTk.PhotoImage(imagen)

            # Mostrar la imagen en la ventana
            label_imagen = Label(ventana_detalle, image=imagen_tk)
            label_imagen.image = imagen_tk  # Necesario para mantener una referencia a la imagen
            label_imagen.pack(pady=10)
        except FileNotFoundError:
            # Si la imagen no se encuentra, mostrar un mensaje
            label_imagen = Label(ventana_detalle, text="Imagen no disponible", bg="gray", width=50, height=20)
            label_imagen.pack(pady=10)

        # Mostrar la información del producto
        label_info = Label(
            ventana_detalle,
            text=f"Código: {codigo}\nNombre: {nombre}\nDescripción: {descripcion}\nCantidad: {cantidad}\n"
                 f"Unidad de Medida: {unidad_medida}\nPrecio: ${precio}",
            justify="left",
            anchor="w"
        )
        label_info.pack(pady=10, padx=10)

        # Botón de cerrar
        boton_cerrar = Button(ventana_detalle, text="Cerrar", command=ventana_detalle.destroy)
        boton_cerrar.pack(pady=10)

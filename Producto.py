import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from ProductInf import InfProducto  # Importa la clase InfProducto para mostrar más información del producto
import os

class Product:
    # Constructor de la clase Product, inicializa la ventana, el canvas, y los márgenes
    def __init__(self, ventana, canva, margenx, margeny):
        self.vetana = ventana  # Ventana principal
        self.canva = canva  # Canvas donde se dibujarán los productos
        self.margenx = margenx  # Margen en el eje X
        self.margeny = margeny  # Margen en el eje Y
        self.current_row = None  # Variable para gestionar las filas de productos

    # Método para mostrar un producto en el canvas
    def mostrarImagen(self, imagen, nombre, precio, x, y, fila, canvas_count, unidades, codigo, descripcion, productopath):
        """
        Muestra un producto en un canvas dentro de la ventana principal.
        
        Parámetros:
        - imagen: imagen del producto a mostrar.
        - nombre: nombre del producto.
        - precio: precio del producto.
        - x, y: posiciones de margen para colocar el producto en el canvas.
        - fila: contenedor donde se agruparán los productos.
        - canvas_count: contador que determina si se debe crear una nueva fila para el producto.
        - unidades: cantidad disponible del producto.
        - codigo: código identificador del producto.
        - descripcion: descripción del producto.
        - productopath: ruta para obtener más información del producto al hacer clic.
        """

        TempP = tk.Canvas(self.canva, width=self.margenx * 8, height=self.margeny * 10, bg="white")
        Inf = InfProducto(self.vetana)  # Instancia de la clase InfProducto para mostrar más información

        # Verifica si el contador de canvas está en cero o en siete para crear una nueva fila
        if canvas_count == 0 or canvas_count == 5:
            self.current_row = tk.Frame(fila)  # Crea un nuevo contenedor de fila
            self.current_row.pack(anchor='w')  # Empaqueta la fila
            canvas_count = 0  # Resetea el contador de canvas

        TempP.pack(in_=self.current_row, side=tk.LEFT, padx=x, pady=y)  # Empaqueta el canvas en la fila

        # Crea un botón que muestra más detalles del producto al hacer clic
        bton = tk.Button(TempP, image=imagen, command=lambda: Inf.ventanaProducto(productopath, nombre, precio, unidades, codigo, descripcion))
        bton.place(x=5, y=5)  # Ubica el botón en la esquina superior izquierda

        # Muestra el nombre del producto
        Nombre = tk.Label(TempP, text=nombre, bg="white", font=("Verdana", self.margenx // 2, "bold"))
        Nombre.place(x=5, y=self.margeny * 6)  # Ubica el nombre en el canvas

        # Muestra el precio del producto
        Precio = tk.Label(TempP, text=precio + "$", bg="white", font=("Verdana", self.margenx // 2, "bold"))
        Precio.place(x=5, y=self.margeny * 8)  # Ubica el precio en el canvas

        # Muestra las unidades disponibles del producto
        Unidades = tk.Label(TempP, text="U: " + unidades, bg="white", font=("Verdana", self.margenx // 3, "bold"))
        Unidades.place(x=self.margenx * 3, y=self.margeny // 2)  # Ubica la cantidad en el canvas

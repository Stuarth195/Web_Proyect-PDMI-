import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
class Product:
    def __init__(self, canva, margenx, margeny):
        self.canva = canva
        self.margenx = margenx
        self.margeny = margeny
        self.current_row = None
    def mostrarImagen(self, imagen, nombre, precio, x, y, fila, canvas_count):

        TempP = tk.Canvas(self.canva, width=self.margenx * 5, height=self.margeny * 10, bg="white")

        # Colocar el Canvas
        if canvas_count == 0 or canvas_count == 6:
            # Crear una nueva fila
            self.current_row = tk.Frame(fila)
            self.current_row.pack(anchor='w')
            canvas_count = 0  # Resetear el contador

        TempP.pack(in_=self.current_row, side=tk.LEFT, padx=x, pady=y)

        bton = tk.Button(TempP, image=imagen)
        bton.place(x=5, y = 5)
        Nombre = tk.Label(TempP, text=nombre, bg="white", font=("Verdana", self.margenx//2, "bold"))
        Nombre.place(x=5, y=self.margeny * 5)
        Precio = tk.Label(TempP, text=precio + "$", bg="white", font=("Verdana", self.margenx//2, "bold"))
        Precio.place(x= 5, y= self.margeny*7)

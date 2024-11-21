import tkinter as tk
from tkinter import messagebox
import os

class LoteInfo:
    def __init__(self, root, file_path=os.path.join("LISTA PRODUCTO Y RECETAS", "Lotes.txt")):
        self.root = root
        self.file_path = file_path
        self.load_data()

    def load_data(self):
        # Leer los datos del archivo cada vez que se carguen los botones
        data = self.read_file(self.file_path)

        # Crear un ScrollFrame
        scroll_frame = self.create_scroll_frame()

        # Crear un botón por cada fila de la matriz de datos
        for row in data:
            if len(row) >= 7:
                id_lote = row[0]  # ID_LOTE
                codigo_producto = row[1]  # CÓDIGO PRODUCTO
                descripcion = row[2]  # DESCRIPCIÓN
                fecha_caducidad = row[3]  # FECHA CADUCIDAD
                proveedor = row[4]  # PROVEEDOR
                unidad_medida = row[5]  # UNIDAD DE MEDIDA
                cantidad = row[6]  # CANTIDAD

                # Crear el botón con el ID_LOTE en el ScrollFrame
                button = tk.Button(scroll_frame, text=f"{id_lote} - {codigo_producto}", command=lambda p=row: self.show_description(p))
                button.pack(fill=tk.X, pady=2)
            else:
                print(f"Linea incompleta o malformada: {row}")  # Para depurar líneas mal formadas

    def create_scroll_frame(self):
        # Crear un frame con canvas y scrollbar
        scroll_frame = tk.Frame(self.root)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scroll_frame)
        scrollbar = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un Frame dentro del Canvas que contendrá los botones
        button_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=button_frame, anchor=tk.NW)

        # Empaquetar el scrollbar y el canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Actualizar la barra de desplazamiento y la ventana del Canvas
        button_frame.update_idletasks()  # Actualiza el tamaño del frame para que funcione el scroll
        canvas.config(scrollregion=canvas.bbox("all"))  # Actualiza el área del scroll

        return button_frame

    def read_file(self, file_path):
        # Leer el archivo y devolver los datos como una lista de listas
        data = []
        with open(file_path, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                lista = linea.split()  # Se separan las palabras por espacios
                data.append(lista)
        return data

    def show_description(self, product_data):
        # Crear una nueva ventana Toplevel
        description_window = tk.Toplevel(self.root)
        description_window.resizable(0,0)
        description_window.title(f"Descripción de {product_data[0]}")

        # Crear el texto con los detalles del lote
        description_text = (
            f"ID Lote: {product_data[0]}\n"
            f"Código Producto: {product_data[1]}\n"
            f"Descripción: {product_data[2]}\n"
            f"Fecha Caducidad: {product_data[3]}\n"
            f"Proveedor: {product_data[4]}\n"
            f"Unidad de Medida: {product_data[5]}\n"
            f"Cantidad: {product_data[6]}"
        )

        # Crear un label en la nueva ventana para mostrar los detalles
        label = tk.Label(description_window, text=description_text, justify=tk.LEFT, padx=10, pady=10)
        label.pack()

    def refresh_data(self):
        # Elimina todos los botones y recarga los datos
        for widget in self.root.winfo_children():
            widget.destroy()

        # Recargar y mostrar los datos nuevamente
        self.load_data()


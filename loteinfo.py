import tkinter as tk
from tkinter import messagebox
import os

class LoteInfo:
    def __init__(self, root, file_path=os.path.join("LISTA PRODUCTO Y RECETAS", "Lotes.txt")):
        self.root = root
        self.file_path = file_path
        self.buttons = []  # Lista para almacenar los botones creados
        self.buttons_created = False  # Controla si los botones han sido creados o no

    def toggle_buttons(self):
        if not self.buttons_created:
            # Si los botones no han sido creados, los creamos
            self.load_data()
            self.buttons_created = True  # Marcar que los botones han sido creados
        else:
            # Si los botones ya han sido creados, los eliminamos
            self.remove_buttons()
            self.buttons_created = False  # Marcar que los botones ya han sido eliminados

    def load_data(self):
        # Leer los datos del archivo cada vez que se carguen los botones
        data = self.read_file(self.file_path)

        # Cambiar el índice inicial de las filas para comenzar en una fila más abajo
        row_index = 5  # Comienza desde la fila 5 en lugar de la 0

        # Crear botones en una estructura dinámica
        for i, row in enumerate(data):
            if len(row) >= 7:
                # Cada fila de datos tiene la información que será usada en los botones
                id_lote = row[0]  # ID_LOTE
                codigo_producto = row[1]  # CÓDIGO PRODUCTO
                descripcion = row[2]  # DESCRIPCIÓN
                fecha_caducidad = row[3]  # FECHA CADUCIDAD
                proveedor = row[4]  # PROVEEDOR
                unidad_medida = row[5]  # UNIDAD DE MEDIDA
                cantidad = row[6]  # CANTIDAD

                # Crear el botón con el ID_LOTE en el Frame
                button = tk.Button(self.root, text=f"{id_lote} - {codigo_producto}", command=lambda p=row: self.show_description(p))
                button.grid(row=row_index, column=0, sticky="ew", pady=2, padx=5)  # Usar grid con sticky para expandir horizontalmente
                self.buttons.append(button)  # Agregar el botón a la lista
                row_index += 1  # Incrementar el índice de fila
            else:
                print(f"Linea incompleta o malformada: {row}")  # Para depurar líneas mal formadas

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
        description_window.resizable(0, 0)
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

    def remove_buttons(self):
        # Elimina todos los botones de la lista
        for button in self.buttons:
            button.destroy()  # Destruir el botón
        self.buttons.clear()  # Limpiar la lista de botones

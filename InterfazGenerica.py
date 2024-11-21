import tkinter as tk
from tkinter import messagebox, Label, Frame, Button
from TXTReader import LectorTXT  # Asegúrate de tener este archivo correctamente importado

class InterfazGenerica:
    def __init__(self, ventana, archivo_principal, columnas):
        """
        Clase para generar una interfaz genérica que trabaja con datos de archivos TXT.

        Args:
            ventana (tk.Tk o tk.Toplevel): Ventana donde se mostrará la información.
            archivo_principal (str): Ruta del archivo principal a leer.
            columnas (list): Lista de nombres para cada columna en el archivo principal.
        """
        self.ventana = ventana
        self.archivo_principal = archivo_principal
        self.columnas = columnas
        self.lector = LectorTXT()

        # Verificar parámetros iniciales
        if not isinstance(self.columnas, list) or not all(isinstance(c, str) for c in self.columnas):
            raise ValueError("columnas debe ser una lista de cadenas.")
        
        # Crear la interfaz
        self._crear_interfaz()

    def _crear_interfaz(self):
        """Crea la interfaz gráfica."""
        frame = Frame(self.ventana)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botón para actualizar la información
        actualizar_btn = Button(frame, text="Actualizar", command=self.mostrar_datos)
        actualizar_btn.pack(pady=5)

        # Contenedor para los datos
        self.datos_frame = Frame(frame)
        self.datos_frame.pack(fill=tk.BOTH, expand=True)

    def mostrar_datos(self):
        """Lee y muestra los datos del archivo principal sin modificar las cantidades."""
        # Limpiar la vista anterior
        for widget in self.datos_frame.winfo_children():
            widget.destroy()

        # Leer datos del archivo principal
        try:
            datos = self.lector.leerTxtFilenUMII(self.archivo_principal)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {self.archivo_principal}.")
            return

        # Filtrar filas vacías
        datos = [fila for fila in datos if fila]

        # Verificar que los datos coincidan con las columnas
        for fila in datos:
            if len(fila) != len(self.columnas):
                messagebox.showerror(
                    "Error",
                    f"El formato del archivo no coincide con las columnas especificadas.\n"
                    f"Fila con error: {fila}"
                )
                return

        # Mostrar encabezados
        for i, col in enumerate(self.columnas):
            Label(self.datos_frame, text=col, font=("Arial", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)

        # Mostrar filas de datos sin modificar las cantidades
        for fila_idx, fila in enumerate(datos, start=1):
            for col_idx, valor in enumerate(fila):
                Label(self.datos_frame, text=str(valor)).grid(row=fila_idx, column=col_idx, padx=5, pady=5)

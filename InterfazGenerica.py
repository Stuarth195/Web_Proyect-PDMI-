import tkinter as tk
from tkinter import messagebox, Label, Frame, Button
from TXTReader import LectorTXT  # Asegúrate de tener este archivo correctamente importado

class InterfazGenerica:
    def __init__(self, ventana, archivo_principal, columnas, operar_lotes=False, archivo_lotes=None):
        """
        Clase para generar una interfaz genérica que trabaja con datos de archivos TXT.

        Args:
            ventana (tk.Tk o tk.Toplevel): Ventana donde se mostrará la información.
            archivo_principal (str): Ruta del archivo principal a leer.
            columnas (list): Lista de nombres para cada columna en el archivo principal.
            operar_lotes (bool): Si es True, realiza operaciones con el archivo de lotes.
            archivo_lotes (str): Ruta del archivo de lotes (requerido si operar_lotes es True).
        """
        self.ventana = ventana
        self.archivo_principal = archivo_principal
        self.columnas = columnas
        self.operar_lotes = operar_lotes
        self.archivo_lotes = archivo_lotes
        self.lector = LectorTXT()

        # Verificar parámetros iniciales
        if self.operar_lotes and not self.archivo_lotes:
            raise ValueError("Si operar_lotes es True, debe proporcionarse archivo_lotes.")
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
        """Lee y muestra los datos del archivo principal."""
        # Limpiar la vista anterior
        for widget in self.datos_frame.winfo_children():
            widget.destroy()

        # Leer datos del archivo principal con el nuevo método
        try:
            datos = self.lector.leerTxtFilenUMII(self.archivo_principal)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {self.archivo_principal}.")
            return

        # Filtrar filas vacías
        datos = [fila for fila in datos if fila]

        # Verificar que los datos coincidan con las columnas
        for fila in datos:
            print(fila)  # Imprimir cada fila para ver qué estamos leyendo
            if len(fila) != len(self.columnas):
                messagebox.showerror(
                    "Error",
                    f"El formato del archivo no coincide con las columnas especificadas.\n"
                    f"Fila con error: {fila}"
                )
                return

        # Si operar_lotes es True, actualizar datos con base en el archivo de lotes
        if self.operar_lotes:
            datos = self.actualizar_con_lotes(datos)

        # Mostrar encabezados
        for i, col in enumerate(self.columnas):
            Label(self.datos_frame, text=col, font=("Arial", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)

        # Mostrar filas de datos
        for fila_idx, fila in enumerate(datos, start=1):
            for col_idx, valor in enumerate(fila):
                Label(self.datos_frame, text=str(valor)).grid(row=fila_idx, column=col_idx, padx=5, pady=5)

    def actualizar_con_lotes(self, datos):
        """
        Actualiza las cantidades en COSECHA.txt basándose en la cantidad total de los lotes en Lotes.txt,
        reemplazando la cantidad en el archivo COSECHA.txt por la cantidad total de los lotes.

        Args:
            datos (list): Datos del archivo principal (COSECHA.txt).

        Returns:
            list: Datos actualizados con las cantidades de los lotes reemplazadas.
        """
        try:
            lotes = self.lector.leerTxtFilenUMII(self.archivo_lotes)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {self.archivo_lotes}.")
            return datos

        # Crear un diccionario con las cantidades totales de lotes por código de producto
        cantidades_lotes = {}
        for lote in lotes:
            try:
                codigo = lote[1]  # El código del producto es la segunda columna en el lote
                cantidad = float(lote[-1])  # La cantidad es la última columna del lote
                
                # Sumamos las cantidades para cada código
                if codigo in cantidades_lotes:
                    cantidades_lotes[codigo] += cantidad
                else:
                    cantidades_lotes[codigo] = cantidad
            except ValueError:
                messagebox.showerror("Error", f"Formato incorrecto en lote: {lote}")
                continue

        # Reemplazar las cantidades en los productos del archivo principal con la cantidad total de los lotes
        for fila in datos:
            codigo = fila[0]  # El código del producto está en la primera columna del archivo COSECHA.txt
            if codigo in cantidades_lotes:
                try:
                    # Reemplazamos la cantidad existente por la cantidad total de los lotes
                    fila[-1] = str(cantidades_lotes[codigo])  # Reemplazamos con el total de los lotes
                except ValueError:
                    messagebox.showerror("Error", f"Cantidad no válida en producto: '{fila[-1]}'.")

        return datos
 
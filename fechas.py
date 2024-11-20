import tkinter as tk
from tkinter import messagebox
import re

class FechaEntradaApp:
    def __init__(self):
        self.fecha_guardada = None  # Variable para almacenar la fecha ingresada

    def fecha(self, ventana_principal):
        # Crear una nueva ventana Toplevel para la fecha
        ventana_fecha = tk.Toplevel(ventana_principal)
        ventana_fecha.title("Ingreso de Fecha")
        
        # Crear el Label para la fecha
        label = tk.Label(ventana_fecha, text="Ingrese la fecha en formato YYYY-MM-DD:")
        label.pack(pady=10)

        # Campo de entrada para la fecha
        entrada_fecha = tk.Entry(ventana_fecha, width=15)
        entrada_fecha.pack(pady=5)

        # Función para restringir la entrada de caracteres
        def validar_entrada(event):
            fecha = entrada_fecha.get()
            # Solo permitir 4 dígitos para el año y luego un guion
            if len(fecha) == 4 and not fecha.endswith('-'):
                entrada_fecha.insert(4, '-')
            # Solo permitir 2 dígitos para el mes (01-12)
            elif len(fecha) == 7 and not fecha.endswith('-'):
                entrada_fecha.insert(7, '-')
            # Restringir los días (01-31)
            if len(fecha) == 10:
                mes = fecha[5:7]
                if mes in ["01", "03", "05", "07", "08", "10", "12"]:
                    max_dia = "31"
                elif mes in ["04", "06", "09", "11"]:
                    max_dia = "30"
                else:  # Febrero
                    max_dia = "28"  # No estamos considerando años bisiestos aquí
                # Limitar el día máximo según el mes
                dia = fecha[8:]
                if dia > max_dia:
                    entrada_fecha.delete(8, tk.END)

        # Asignar el evento para controlar la entrada de caracteres
        entrada_fecha.bind("<KeyRelease>", validar_entrada)

        # Función para verificar y guardar la fecha en la variable sin guiones
        def verificarYAceptar():
            fecha = entrada_fecha.get()
            if self.verificarFormatoFecha(fecha):
                # Eliminar los guiones y guardar la fecha
                fecha_sin_guiones = fecha.replace('-', '')
                self.fecha_guardada = fecha_sin_guiones
                ventana_fecha.destroy()
                print(f"Fecha guardada: {self.fecha_guardada}")  # Ejemplo: 20241203
            else:
                # Si la fecha no es válida, mostrar mensaje de error
                messagebox.showerror("Error", "La fecha no está en el formato correcto (YYYY-MM-DD).")

        # Botón para verificar y aceptar la fecha
        boton_aceptar = tk.Button(ventana_fecha, text="Aceptar", command=verificarYAceptar)
        boton_aceptar.pack(pady=10)

        # Ejecutar la ventana
        ventana_fecha.mainloop()

    def verificarFormatoFecha(self, fecha):
        # Expresión regular para verificar si la fecha tiene el formato año-mes-día
        patron = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
        return bool(re.match(patron, fecha))



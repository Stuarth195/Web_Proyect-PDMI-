import tkinter as tk
import os
from InterfazGenerica import InterfazGenerica  # Asegúrate de importar correctamente la clase

# Ruta de los archivos
archivo_principal = os.path.join("LISTA PRODUCTO Y RECETAS", "COSECHA.txt")

# Crear la ventana principal
root = tk.Tk()

# Instanciar la clase InterfazGenerica
interfaz = InterfazGenerica(
    ventana=root,
    archivo_principal=archivo_principal,
    columnas=["Código", "Descripción", "Unidad", "Cantidad"],  # Ajustado para tu archivo
)

# Ejecutar la interfaz gráfica
root.mainloop()

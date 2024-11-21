import tkinter as tk
import os
from InterfazGenerica import InterfazGenerica  # Asegúrate de importar correctamente la clase

root = tk.Tk()
interfaz = InterfazGenerica(
    ventana=root,
    archivo_principal=os.path.join("LISTA PRODUCTO Y RECETAS", "COSECHA.txt"),
    columnas=["Código", "Descripción", "Unidad", "Cantidad"],  # Ajustado para tu archivo
    operar_lotes=True,
    archivo_lotes=os.path.join("LISTA PRODUCTO Y RECETAS", "Lotes.txt")
)
root.mainloop()

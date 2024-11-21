from admin import Seccion
from TXTReader import LectorTXT
from WriterEnDocumento import Writer
from Producto import Product
from logic import Instacia_B
import tkinter as tk
from tkinter import messagebox
import os
from botones import Botones, BotonesPE, ReciboCosecha
from verify import FechaEntradaApp, CodigoApp, CantidadApp, ProvedorApp
from loteinfo import LoteInfo
from InterfazGenerica import InterfazGenerica



if __name__ == "__main__":
    import tkinter as tk

    class App:
        def __init__(self, root):
            self.root = root
            self.frame_scroll = tk.Frame(root)
            self.frame_scroll.pack(fill="both", expand=True)
            self.someopen = False

        def GRC(self):
            if not self.someopen:
                self.recibo = ReciboCosecha(self.frame_scroll, "recibos_cosecha.txt")
                self.recibo.on_form_closed = self.formulario_terminado
                self.someopen = True
            else:
                messagebox.showwarning("Advertencia", "No puedes avanzar si tienes un proceso abierto")

        def formulario_terminado(self):
            self.someopen = False
            messagebox.showinfo("Proceso Finalizado", "Formulario cerrado con éxito.")

    root = tk.Tk()
    app = App(root)
    tk.Button(root, text="Crear Formulario", command=app.GRC).pack(pady=10)
    root.mainloop()

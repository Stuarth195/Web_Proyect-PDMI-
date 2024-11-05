import tkinter as tk
from tkinter import ttk

class Seccion:
    def __init__(self, notebook, alto_canva, ancho_canva, canva_color="blue"):
        self.notebook = notebook
        self.alto = alto_canva
        self.ancho = ancho_canva
        self.C_color = canva_color
        self.frame = None
        self.canva = None
        self.scroll = None
        self.frame_scroll = None

    def crear(self, nombre):
        self.nombre = nombre
        # Crear el frame del notebook
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text=self.nombre)

        # Crear el canvas
        self.canva = tk.Canvas(self.frame, bg=self.C_color)
        self.canva.pack(side="left", fill="both", expand=True)

        # Crear la scrollbar vertical
        self.scroll = tk.Scrollbar(self.frame, orient="vertical", command=self.canva.yview)
        self.scroll.pack(side="right", fill="y")

        # Configurar el canvas para que sincronice con la scrollbar
        self.canva.configure(yscrollcommand=self.scroll.set)

        # Crear un frame dentro del canvas para contener otros widgets
        self.frame_scroll = tk.Frame(self.canva, bg=self.C_color)
        self.canva.create_window((0, 0), window=self.frame_scroll, anchor='nw')

        # Ajustar la región de scroll del Canvas según el tamaño del contenido
        self.frame_scroll.bind("<Configure>", lambda e: self.canva.configure(scrollregion=self.canva.bbox("all")))

        # Capturar el evento de desplazamiento del mouse en el canvas y en el frame_scroll
        self.canva.bind("<MouseWheel>", self.on_mouse_wheel)
        self.frame_scroll.bind("<MouseWheel>", self.on_mouse_wheel)

        # Capturar las teclas de flechas para el desplazamiento
        self.canva.bind("<Up>", self.scroll_up)
        self.canva.bind("<Down>", self.scroll_down)
        
        # Establecer el foco en el canvas para que reciba los eventos de teclado
        self.canva.focus_set()

    def on_mouse_wheel(self, event):
        # Desplazar el canvas con la rueda del ratón
        self.canva.yview_scroll(int(-1 * (event.delta / 120)), "units")  # 120 es el valor estándar para la rueda

    def scroll_up(self, event):
        # Desplazar hacia arriba con la tecla de flecha hacia arriba
        self.canva.yview_scroll(-1, "units")

    def scroll_down(self, event):
        # Desplazar hacia abajo con la tecla de flecha hacia abajo
        self.canva.yview_scroll(1, "units")


# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    seccion = Seccion(notebook, 600, 780)
    seccion.crear("Ejemplo de Sección")

    root.mainloop()

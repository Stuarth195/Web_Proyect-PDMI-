import tkinter as tk
from tkinter import ttk

class Seccion:
    def __init__(self, notebook, alto_canva, ancho_canva, canva_color):
        self.notebook = notebook
        self.alto = alto_canva
        self.ancho = ancho_canva
        self.C_color = canva_color
        self.frame = None
        self.canva = None
        self.scroll = None
        self.frame_scroll = None

    def crear(self, nombre):
        # Crear el frame del notebook
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text=nombre)

        # Crear el canvas
        self.canva = tk.Canvas(self.frame, width=self.ancho, height=self.alto, bg=self.C_color)
        self.canva.grid(row=0, column=0, sticky="nsew")

        # Crear la scrollbar vertical
        self.scroll = tk.Scrollbar(self.frame, orient="vertical", command=self.canva.yview)
        self.scroll.grid(row=0, column=1, sticky="ns")

        # Configurar el canvas
        self.canva.configure(yscrollcommand=self.scroll.set)

        # Crear un frame dentro del canvas para contener otros widgets
        self.frame_scroll = tk.Frame(self.canva, bg=self.C_color)
        self.canva.create_window((0, 0), window=self.frame_scroll, anchor='nw')

        # Ajustar la región de scroll del Canvas según el tamaño del contenido
        self.frame_scroll.bind("<Configure>", lambda e: self.canva.configure(scrollregion=self.canva.bbox("all")))

        # Habilitar el scroll con el ratón
        self.canva.bind("<MouseWheel>", self.on_mouse_wheel)  # Para Windows
        self.canva.bind("<Button-4>", self.on_mouse_wheel)  # Para Linux (scroll up)
        self.canva.bind("<Button-5>", self.on_mouse_wheel)  # Para Linux (scroll down)

        # Habilitar el desplazamiento con las teclas de flecha
        self.canva.bind("<Up>", self.scroll_up)
        self.canva.bind("<Down>", self.scroll_down)

        # Hacer que el canvas tenga el foco
        self.canva.focus_set()

    def on_mouse_wheel(self, event):
        # Desplazar el canvas según la rueda del ratón
        self.canva.yview_scroll(int(-1*(event.delta/120)), "units")  # 120 es el valor estándar para la rueda

    def scroll_up(self, event):
        self.canva.yview_scroll(1, "units")  # Desplaza hacia arriba

    def scroll_down(self, event):
        self.canva.yview_scroll(-1, "units")  # Desplaza hacia abajo

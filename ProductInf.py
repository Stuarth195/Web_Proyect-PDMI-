import tkinter as tk
from PIL import Image, ImageTk  # Necesario para manejar imágenes
from WriterEnDocumento import Writer  # Asegúrate de que Writer esté correctamente importado

class InfProducto:
    def __init__(self, ventana):
        self.ventana = ventana

    def ventanaProducto(self, imagen, nombre=None, precio=None, unidades=None, codigo=None, descripcion=None):
        # Crear la ventana principal
        window = tk.Toplevel(self.ventana)
        window.title(f"{nombre}")
        window.resizable(False, False)

        escritor = Writer()

        # Crear el canvas con tamaño 350x450
        canvas = tk.Canvas(window, width=500, height=300, bg="green")
        canvas.pack()

        fondo = tk.Label(canvas, image=imagen)
        fondo.place(x=15, y=20)

        # Función para crear texto con fondo blanco
        def crear_texto_con_fondo(x, y, texto):
            # Dibujar un rectángulo blanco detrás del texto
            canvas.create_rectangle(x, y, x + 210, y + 40, fill="green", outline="")
            # Crear el texto en color negro sobre el fondo blanco
            canvas.create_text(x + 5, y + 5, anchor=tk.NW, text=texto, font=("Arial", 13, "bold"), fill="white")

        # Crear las etiquetas de texto con fondo blanco y texto negro
        crear_texto_con_fondo(250, 20, f"Nombre: {nombre}")
        crear_texto_con_fondo(250, 50, f"Precio: {precio} €")
        crear_texto_con_fondo(250, 80, f"Unidades: {unidades}")
        crear_texto_con_fondo(250, 110, f"Código: {codigo}")
        crear_texto_con_fondo(250, 140, f"Descripción: {descripcion}")

        # Entrada para que el usuario agregue la cantidad al carrito
        entrada = tk.Entry(window, width=11, font=("Arial", 12))
        entrada.place(x=250, y=180)

        # Botón para agregar al carrito
        boton = tk.Button(window, text="Agregar al carrito", command=lambda: (escritor.write("Carrito.txt", f"{nombre} {entrada.get()} {precio}"), destruir_ventana()))
        boton.place(x=250, y=210)

        def destruir_ventana():
            window.destroy()

        # Iniciar el ciclo principal de la ventana Tkinter
        window.mainloop()

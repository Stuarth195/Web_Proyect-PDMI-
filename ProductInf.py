import tkinter as tk
from PIL import Image, ImageTk
import os
from WriterEnDocumento import Writer

class InfProducto:
    def __init__(self, ventana):
        self.ventana = ventana

    def ventanaProducto(self, imagen_path, nombre=None, precio=None, unidades=None, codigo=None, descripcion=None):
        # Crear la ventana principal
        window = tk.Toplevel(self.ventana)
        window.title(f"{nombre}")

        escritor = Writer()

        try:
            # Intenta abrir la imagen con PIL
            self.img = Image.open(imagen_path)
            self.img_tk = ImageTk.PhotoImage(self.img)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            # Si no se puede cargar la imagen, usar una imagen predeterminada o no mostrar nada
            self.img_tk = None

        # Almacenar la referencia a la imagen para evitar que sea recogida por el garbage collector
        window.img_tk = self.img_tk  # Guardar la referencia a la imagen

        # Crear el canvas con tamaño 350x450
        canvas = tk.Canvas(window, width=350, height=450, bg="green")
        canvas.pack()

        if self.img_tk:
            # Mostrar la imagen en el canvas
            canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        # Función para crear texto con fondo blanco
        def crear_texto_con_fondo(x, y, texto):
            # Dibujar un rectángulo blanco detrás del texto
            canvas.create_rectangle(x, y, x + 345, y + 30, fill="white", outline="")
            # Crear el texto en color negro sobre el fondo blanco
            canvas.create_text(x + 5, y + 5, anchor=tk.NW, text=texto, font=("Arial", 12), fill="black")

        # Crear las etiquetas de texto con fondo blanco y texto negro
        crear_texto_con_fondo(5, 200, f"Nombre: {nombre}")
        crear_texto_con_fondo(5, 230, f"Precio: {precio} €")
        crear_texto_con_fondo(5, 260, f"Unidades: {unidades}")
        crear_texto_con_fondo(5, 290, f"Código: {codigo}")
        crear_texto_con_fondo(5, 320, f"Descripción: {descripcion}")

        # Entrada para que el usuario agregue la cantidad al carrito
        entrada = tk.Entry(window, width=40, font=("Arial", 12))
        entrada.place(x=250, y=1)

        # Botón para agregar al carrito
        boton = tk.Button(window, text="Agregar al carrito", command=lambda: (escritor.write("Carrito.txt", f"{nombre} {entrada.get()} {precio}"), destruir_ventana()))
        boton.place(x=250, y=40)

        def destruir_ventana():
            window.destroy()

        # Iniciar el ciclo principal de la ventana Tkinter
        window.mainloop()

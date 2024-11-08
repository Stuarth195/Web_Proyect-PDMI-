import tkinter as tk
from PIL import Image, ImageTk
from TXTReader import LectorTXT  # Suponiendo que esta clase está definida correctamente

class MCarrito:
    def __init__(self):
        self.Lector = LectorTXT()  # Inicializa el lector de archivos
        self.matriz = []

    def Mostrar_Carrito(self):
        # Crear la ventana principal
        root = tk.Tk()
        root.title("Carrito de Compras")

        # Leer el archivo de texto y almacenar el contenido en la matriz
        self.matriz = self.Lector.leerTxtFile("Carrito.txt")

        # Crear el canvas para mostrar los datos
        canva = tk.Canvas(root, width=250, height=500, bg="#f0cf27")
        canva.pack()

        # Título de la ventana
        label = tk.Label(canva, text="Carrito", font=("Verdana", 16), bg="white")
        label.place(x=5, y=0)

        fila = 30  # Posición inicial de las etiquetas
        for item in self.matriz:
            # Convertir cada fila de la matriz a una cadena de texto
            tempI = " | ".join(item)  # Usar " | " para separar cada elemento de la fila

            # Crear una etiqueta con el texto y ubicarla en el canvas
            label = tk.Label(canva, text=tempI, font=("Verdana", 10), bg="white", anchor="w")
            label.place(x=5, y=fila)

            # Incrementar la fila para la siguiente etiqueta
            fila += 30

        boton = tk.Button(root, text="Cerrar", font=("Verdana", 12), bg="white", command=lambda:cerrar_ventana())
        boton.place(x=180, y=460)

        boton = tk.Button(root, text="Finalizar Compra", font=("Verdana", 12), bg="white", command=lambda: cerrar_ventana())
        boton.place(x=5, y=460)

        def cerrar_ventana():
            root.destroy()

        # Iniciar el ciclo principal de la ventana Tkinter
        root.mainloop()


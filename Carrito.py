import tkinter as tk
from PIL import Image, ImageTk
from TXTReader import LectorTXT
from WriterEnDocumento import Writer
from Pagar import Pagos

class MCarrito:
    def __init__(self):
        self.Lector = LectorTXT()  # Inicializa el lector de archivos
        self.matriz = []
        self.Escritor = Writer()
        self.Pagos = Pagos()

    def Mostrar_Carrito(self, usuario):
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
        label.place(x=5, y=5)

        User = tk.Label(canva, text=usuario, font=("Verdana", 16), bg="White")
        User.place(x=125, y=5)

        fila = 40  # Posición inicial de las etiquetas
        for item in self.matriz:
            # Convertir cada fila de la matriz a una cadena de texto
            tempI = " | ".join(item)  # Usar " | " para separar cada elemento de la fila
            mensaje = " ".join(item)

            # Crear el botón primero
            label_button = tk.Button(canva, text=tempI, font=("Verdana", 10), bg="white", anchor="w")

            # Luego, asociamos la función eliminar con el botón usando lambda
            label_button.config(command=lambda label=label_button: eliminar(label, mensaje))

            # Ubicar el botón en el canvas
            label_button.place(x=5, y=fila)

            # Incrementar la fila para la siguiente etiqueta
            fila += 30

        # Botón para cerrar la ventana
        boton = tk.Button(root, text="Cerrar", font=("Verdana", 12), bg="white", command=lambda: cerrar_ventana())
        boton.place(x=180, y=460)

        # Botón para finalizar la compra
        boton = tk.Button(root, text="Finalizar Compra", font=("Verdana", 12), bg="white",
                          command=lambda: confirmarCompra())
        boton.place(x=5, y=460)

        # Función para cerrar la ventana
        def cerrar_ventana():
            root.destroy()

        def confirmarCompra():
            root.destroy()
            self.Pagos.menu_compra(usuario)

        # Función para eliminar un botón
        def eliminar(labelE, mensaje):
            labelE.destroy()
            self.Escritor.reemplazar_linea_en_archivo("Carrito.txt", mensaje)


        # Iniciar el ciclo principal de la ventana Tkinter
        root.mainloop()

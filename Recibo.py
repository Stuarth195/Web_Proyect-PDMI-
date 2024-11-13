import tkinter as tk
from PIL import Image, ImageTk
from WriterEnDocumento import Writer
import os
from TXTReader import LectorTXT

class Reb:
    def __init__(self, user, total):
        self.user = user + ";"
        self.total = total * 1.03  # Agregar un pequeño incremento al total (1%)
        self.escritor = Writer()
        self.imagen = os.path.join("Imagenes", "logotipo.png")
        self.lector = LectorTXT()
        self.Carrito = self.lector.leerTxtFile("Carrito.txt")
        self.Productos = []
        self.Unidades = []
        for item in self.Carrito:
            self.Productos.append(item[0])
            self.Unidades.append(item[1])

    def deliverReb(self, direccion, tiempo_espera, metodo_pago, Tipo_entrega):
        # Crear la ventana
        Rev = tk.Tk()
        Rev.title("Recibo de Compra")
        Rev.resizable(False, False)

        if direccion == "":
            direccion = "Fabrica Aguas Calientes"

        # Crear el fondo del canvas
        Fondo = tk.Canvas(Rev, width=500, height=600, bg="lightgray")
        Fondo.pack()

        # Agregar título al recibo
        titulo = tk.Label(Rev, text="Recibo de Compra", font=("Verdana", 20, "bold"), fg="black", bg="lightgray")
        titulo.place(x=100, y=20)

        # Mostrar el nombre del usuario
        label_usuario = tk.Label(Rev, text=f"Nombre del Usuario: {self.user}", font=("Verdana", 14), fg="black", bg="lightgray")
        label_usuario.place(x=20, y=80)

        # Mostrar el total a pagar
        label_total = tk.Label(Rev, text=f"Total a Pagar: ${self.total:.2f}", font=("Verdana", 14), fg="black", bg="lightgray")
        label_total.place(x=20, y=120)

        # Mostrar la dirección de entrega
        label_direccion = tk.Label(Rev, text=f"Dirección: {direccion}", font=("Verdana", 14), fg="black", bg="lightgray")
        label_direccion.place(x=20, y=160)

        # Mostrar el tiempo estimado de espera
        label_tiempo = tk.Label(Rev, text=f"Tiempo de espera: {tiempo_espera} minutos", font=("Verdana", 14), fg="black", bg="lightgray")
        label_tiempo.place(x=20, y=200)

        # Mostrar el método de pago
        label_metodo_pago = tk.Label(Rev, text=f"Método de Pago: {metodo_pago}", font=("Verdana", 14), fg="black", bg="lightgray")
        label_metodo_pago.place(x=20, y=240)

        # Mostrar un mensaje de confirmación
        mensaje_confirmacion = tk.Label(Rev, text="¡Gracias por tu compra!", font=("Verdana", 16, "italic"), fg="green", bg="lightgray")
        mensaje_confirmacion.place(x=100, y=550)

        # Mostrar el tipo de entrega
        Tipo_Entrega_label = tk.Label(Rev, text=f"Metod de Entrega: {Tipo_entrega}", font=("Verdana", 14), fg="black", bg="lightgray")
        Tipo_Entrega_label.place(x=20, y=280)

        try:
            # Asegúrate de que la imagen esté en la carpeta 'images'

            logo_tk = Image.open(self.imagen)
            logo_tk_img = ImageTk.PhotoImage(logo_tk)

            # Mostrar la imagen en un Label
            label_logo = tk.Label(Fondo, image=logo_tk_img, bg="lightgray")
            label_logo.image = logo_tk  # Mantener una referencia a la imagen para que no se pierda
            label_logo.pack(padx=10, pady=10)  # Coloca la imagen en la posición deseada

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        StrProductos = ""
        i = 0

        print(self.Productos, self.Unidades)

        self.escritor.write("RegistroCompras.txt", self.user + " " + str(self.total))

        # Iniciar el bucle principal
        Rev.mainloop()



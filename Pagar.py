import tkinter as tk
from PIL import Image, ImageTk
from TXTReader import LectorTXT

class Pagos:
    def __init__(self):
        self.lector = LectorTXT()
        self.total = 0

    def menu_compra(self, user):
        ventana_Compra = tk.Tk()
        ventana_Compra.title('Comprar')
        ventana_Compra.resizable(False, False)

        OpcionesPago = ["Pago Efectivo", "Pago Tarjeta", "Pago Simpe"]

        # Función que actualizará el label con la opción seleccionada
        def actualizar_seleccion(metodo):
            LabelTarjeta.config(text=f"Seleccionaste: {metodo}")

        # Inicializar la variable que almacenará la opción seleccionada
        var = tk.StringVar()
        var.set(OpcionesPago[0])  # Establecer un valor por defecto

        # Crear el label para mostrar el método de pago seleccionado
        label_seleccion = tk.Label(ventana_Compra, text=f"Seleccionaste: {var.get()}", font=("Verdana", 16), fg="black", bg="white")
        label_seleccion.place(x=5, y=300)

        # Otras etiquetas y elementos de la interfaz
        self.total = 0
        Carrito = self.lector.leerTxtFile("Carrito.txt")
        for compra in Carrito:
            if len(compra) > 2:
                self.total = self.total + int(compra[1]) * int(compra[2])

        Fondo = tk.Canvas(ventana_Compra, width=1000, height=800, bg="grey")
        Fondo.pack()

        Total_a_pagar = tk.Label(ventana_Compra, text=str(self.total) + "$", font=("Verdana", 20), fg="black", bg="white")
        Total_a_pagar.place(x=210, y=10)

        LabelTotal = tk.Label(ventana_Compra, text="Total a pagar:", font=("Verdana", 20), fg="black", bg="white")
        LabelTotal.place(x=5, y=10)

        LabelUser = tk.Label(ventana_Compra, text=user, font=("Verdana", 20), fg="black", bg="white")
        LabelUser.place(x=450, y=10)

        LabelTarjeta = tk.Label(ventana_Compra, text="Seleccionar metodo de pago", font=("Verdana", 20), fg="black", bg="white")
        LabelTarjeta.place(x=5, y=200)

        # Crear los Radio Buttons para las opciones de pago
        rb1 = tk.Radiobutton(ventana_Compra, text=OpcionesPago[0], variable=var, value=OpcionesPago[0], font=("Verdana", 14), fg="black", bg="white", command=lambda:actualizar_seleccion(OpcionesPago[0]))
        rb1.place(x=5, y=240)
        rb2 = tk.Radiobutton(ventana_Compra, text=OpcionesPago[1], variable=var, value=OpcionesPago[1], font=("Verdana", 14), fg="black", bg="white", command=lambda:actualizar_seleccion(OpcionesPago[1]))
        rb2.place(x=5, y=280)
        rb3 = tk.Radiobutton(ventana_Compra, text=OpcionesPago[2], variable=var, value=OpcionesPago[2], font=("Verdana", 14), fg="black", bg="white", command=lambda:actualizar_seleccion(OpcionesPago[2]))
        rb3.place(x=5, y=320)

        # Mostrar el método de entrega (otro label, que no está completo en tu código)
        LabelEntrega = tk.Label(ventana_Compra, text="Seleccionar metodo entrega", font=("Verdana", 20), fg="black", bg="white")
        LabelEntrega.place(x=5, y=100)

        ventana_Compra.mainloop()

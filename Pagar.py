import tkinter as tk
from TXTReader import LectorTXT
from Recibo import Reb
from WriterEnDocumento import Writer
from Timer import TimerApp
import random


class Pagos:
    def __init__(self, root):
        self.lector = LectorTXT()
        self.total = 0.0
        self.metodoPago = "No seleccionado"
        self.escritor = Writer()
        self.root = root
        self.tiempoEntrega = random.randint(15, 60)

    def menu_compra(self, user):
        self.ventana_Compra = tk.Tk()
        self.ventana_Compra.title('Comprar')
        self.ventana_Compra.resizable(False, False)

        OpcionesPago = ["Pago Efectivo", "Pago Tarjeta", "Pago Simpe"]

        # Función que actualizará el label con la opción seleccionada
        def actualizar_seleccion(metodo):
            LabelTarjeta.config(text=f"Seleccionaste: {metodo}")

            # Si el método seleccionado es 'Pago Efectivo', mostramos el Entry
            if metodo == "Pago Efectivo":
                Entry1.place(x=600, y=140)
                Entry2.place_forget()
                Tarjeta1.place_forget()
                Tarjeta2.place_forget()
                Simpe.place_forget()
                Efectivo1.place(x=600, y=60)
                self.metodoPago = metodo
            elif metodo == "Pago Tarjeta":
                Entry1.place(x=600, y=100)
                Tarjeta1.place(x=600, y=60)
                Tarjeta2.place(x=600, y=130)
                Entry2.place(x=600, y=170)
                Simpe.place_forget()
                Efectivo1.place_forget()
                self.metodoPago = metodo
            else:
                Entry1.place(x=600, y=100)  # Si no es Pago Efectivo, ocultamos el Entry
                Entry2.place_forget()
                Tarjeta1.place_forget()
                Tarjeta2.place_forget()
                Efectivo1.place_forget()
                Simpe.place(x=600, y=60)
                self.metodoPago = metodo

        # Inicializar la variable que almacenará la opción seleccionada
        var = tk.StringVar()
        var.set(OpcionesPago[0])  # Establecer un valor por defecto

        # Crear el label para mostrar el método de pago seleccionado
        label_seleccion = tk.Label(self.ventana_Compra, text=f"Seleccionaste: {var.get()}", font=("Verdana", 16), fg="black",
                                   bg="white")
        label_seleccion.place(x=5, y=300)

        # Calcular el total de la compra (esto ya está en tu código)
        self.total = 0
        Carrito = self.lector.leerTxtFile("Carrito.txt")
        for compra in Carrito:
            if len(compra) > 2:
                self.total = self.total + float(compra[1]) * float(compra[2])

        self.Recivos = Reb(user, self.total,self.ventana_Compra)

        # Crear el fondo (canvas)
        Fondo = tk.Canvas(self.ventana_Compra, width=1000, height=600, bg="grey")
        Fondo.pack()

        # Mostrar el total a pagar
        Total_a_pagar = tk.Label(self.ventana_Compra, text=str(self.total) + "$", font=("Verdana", 20), fg="black",
                                 bg="white")
        Total_a_pagar.place(x=210, y=10)

        LabelTotal = tk.Label(self.ventana_Compra, text="Total a pagar:", font=("Verdana", 20), fg="black", bg="white")
        LabelTotal.place(x=5, y=10)

        LabelUser = tk.Label(self.ventana_Compra, text=user, font=("Verdana", 20), fg="black", bg="white")
        LabelUser.place(x=450, y=10)

        LabelTarjeta = tk.Label(self.ventana_Compra, text="Seleccionar metodo de pago", font=("Verdana", 20), fg="black",
                                bg="white")
        LabelTarjeta.place(x=5, y=100)

        # Crear los Radio Buttons para las opciones de pago
        rb1 = tk.Radiobutton(self.ventana_Compra, text=OpcionesPago[0], variable=var, value=OpcionesPago[0],
                             font=("Verdana", 14), fg="black", bg="white",
                             command=lambda: actualizar_seleccion(OpcionesPago[0]))
        rb1.place(x=5, y=140)
        rb2 = tk.Radiobutton(self.ventana_Compra, text=OpcionesPago[1], variable=var, value=OpcionesPago[1],
                             font=("Verdana", 14), fg="black", bg="white",
                             command=lambda: actualizar_seleccion(OpcionesPago[1]))
        rb2.place(x=5, y=180)
        rb3 = tk.Radiobutton(self.ventana_Compra, text=OpcionesPago[2], variable=var, value=OpcionesPago[2],
                             font=("Verdana", 14), fg="black", bg="white",
                             command=lambda: actualizar_seleccion(OpcionesPago[2]))
        rb3.place(x=5, y=220)

        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # Crear el campo de entrada (Entry) para Pago Efectivo, pero ocultarlo inicialmente
        Entry1 = tk.Entry(self.ventana_Compra, width=50)
        Entry1.place_forget()  # Esto asegura que no se vea al inicio

        Entry2 = tk.Entry(self.ventana_Compra, width=50)
        Entry2.place_forget()  # Esto asegura que no se vea al inicio

        Tarjeta1 = tk.Label(self.ventana_Compra, text="Ingrese su numero de tarjeta", font=("Verdana", 20), fg="black",
                            bg="white")
        Tarjeta1.place_forget()

        Tarjeta2 = tk.Label(self.ventana_Compra, text="Ingrese el pin de la tarjeta", font=("Verdana", 20), fg="black",
                            bg="white")
        Tarjeta2.place_forget()

        Simpe = tk.Label(self.ventana_Compra, text="Digite Numero de Telefono", font=("Verdana", 20), fg="black", bg="white")
        Simpe.place_forget()

        Efectivo1 = tk.Label(self.ventana_Compra, text="Nombre y apellidos de la \n persona", font=("Verdana", 20),
                             fg="black",
                             bg="white")
        Efectivo1.place_forget()
        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        # Mostrar el método de entrega (otro label, que no está completo en tu código)
        LabelEntrega = tk.Label(self.ventana_Compra, text="Seleccionar metodo entrega", font=("Verdana", 20), fg="black",
                                bg="white")
        LabelEntrega.place(x=5, y=300)

        LabelLocacion = tk.Label(self.ventana_Compra, text="Recoger en local o fabrica", font=("Verdana", 16), fg="black",
                                 bg="white")
        LabelLocacion.place(x=5, y=340)

        ConfirmarEnLocacion = tk.Button(self.ventana_Compra, text="Confirmar", font=("Verdana", 16), bg="white", fg="black",
                                        command=lambda: confirmarCompra(1))
        ConfirmarEnLocacion.place(x=5, y=380)

        LabelEmail = tk.Label(self.ventana_Compra, text="Ingrese su correo electronico", font=("Verdana", 16), fg="black",
                                 bg="white")
        LabelEmail.place(x=600, y=210)
        EmailE = tk.Entry(self.ventana_Compra, width=50, font=("Verdana", 16))
        EmailE.place(x=600, y=250)

        Nota = tk.Label(self.ventana_Compra, text=f"* en caso de no ingresar un correo @gmail.com valido no le\nllegara la confirmacion de compra", font=("Verdana", 10), fg="black",
                                 bg="white")
        Nota.place(x=600, y=290)

        if user != "User0000":
            Direccion = tk.Label(self.ventana_Compra, text="Ingrese la direccion", font=("Verdana", 16), fg="black",
                                 bg="white")
            Direccion.place(x=5, y=450)

            DireccionUser = tk.Entry(self.ventana_Compra, width=50, font=("Verdana", 16))
            DireccionUser.place(x=5, y=490)

            ConfirmarDireccion = tk.Button(self.ventana_Compra, text="Confirmar", font=("Verdana", 16), bg="white",
                                           fg="black", command=lambda: confirmarCompra(2))
            ConfirmarDireccion.place(x=5, y=530)

        def confirmarCompra(Tipo):
            self.escritor.limpiartxt("Carrito.txt")

            info_Correcta = False

            if self.metodoPago == "Pago Tarjeta":
                if Entry1.get().strip() != "" and Entry2.get().strip() != "":
                    info_Correcta = True
                else:
                    info_Correcta = False

            elif self.metodoPago == "Pago Efectivo":
                if Entry1.get().strip() != "":
                    info_Correcta = True

            elif self.metodoPago == "Pago Simpe":
                if Entry1.get().strip() != "":
                    info_Correcta = True

            if info_Correcta:
                if EmailE.get().strip() != "":

                    self.timer = TimerApp(self.root)
                    self.timer.start_timer(self.tiempoEntrega)
                    Email = EmailE.get().strip()

                    if Tipo == 2:
                        Dir = DireccionUser.get()  # Usamos .get() para obtener la dirección del Entry
                        self.Recivos.deliverReb(Dir, self.tiempoEntrega, self.metodoPago, "Entrega Domicilio", Email, self.metodoPago, "Delivery")
                    elif Tipo == 1:
                        self.Recivos.deliverReb("", self.tiempoEntrega, self.metodoPago, "Recoger en Local", Email, self.metodoPago, "Local")

                    # Cerrar la ventana después de confirmar la compra
                    self.ventana_Compra.destroy()

            else:
                Error = tk.Tk()

                canva = tk.Canvas(Error, width=100, height=50)
                canva.pack()

                Text = tk.Label(Error, text="Ingrese los datos correctamente", font=("Verdana", 16))
                Text.place(relx=0, rely=0)

                Error.mainloop()

        # Iniciar el bucle principal de la ventana
        self.ventana_Compra.mainloop()

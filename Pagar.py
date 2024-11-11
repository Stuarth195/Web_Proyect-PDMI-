import tkinter as tk
from PIL import Image, ImageTk
from TXTReader import LectorTXT
class Pagos:
    def __init__(self):
        self.lector =  LectorTXT()
        self.total = 0

    def menu_compra(self):
        ventana_Compra = tk.Tk()
        ventana_Compra.title('Comprar')
        ventana_Compra.resizable(False, False)
        self.total = 0

        Carrito = self.lector.leerTxtFile("Carrito.txt")
        for compra in Carrito:
            if len(compra) > 2:
                self.total = self.total + int(compra[1])*int(compra[2])

        Fondo = tk.Canvas(ventana_Compra, width=600, height=500, bg="grey")
        Fondo.pack()

        Total_a_pagar = tk.Label(ventana_Compra, text=self.total, font=("Verdana", 20), fg="black", bg="white")
        Total_a_pagar.place(x=100, y=10)

        ventana_Compra.mainloop()

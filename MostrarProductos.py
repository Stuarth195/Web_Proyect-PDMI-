from TXTReader import LectorTXT
from Producto import Product
class MP:
    def __init__(self, feed, margenx, margeny):
        self.feed = feed
        self.margenx = margenx
        self.margeny = margeny
    def Mostrar_Productos(self, imagen):
        lector = LectorTXT()
        productos = lector.leerTxtFile("Productos.txt")
        print(productos)
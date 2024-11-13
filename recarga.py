import os
import tkinter as tk

class RecargadorArchivos:
    def __init__(self, ruta_directorio=None, extension='.txt'):
        self.ruta_directorio = ruta_directorio if ruta_directorio else os.getcwd()
        self.extension = extension
        self.archivos = {}

    def recargar_archivos(self):
        """Recarga los archivos del directorio con la extensión especificada."""
        self.archivos = {}
        try:
            for archivo_nombre in os.listdir(self.ruta_directorio):
                if archivo_nombre.endswith(self.extension):
                    archivo_ruta = os.path.join(self.ruta_directorio, archivo_nombre)
                    with open(archivo_ruta, 'r') as archivo:
                        self.archivos[archivo_nombre] = archivo.readlines()
        except FileNotFoundError:
            print(f"Error: El directorio {self.ruta_directorio} no fue encontrado.")
    
    def obtener_archivos(self):
        """Devuelve los archivos recargados."""
        return self.archivos


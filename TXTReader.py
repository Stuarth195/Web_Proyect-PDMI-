import os

class LectorTXT:

    def leerTxtFile(self, txtFilePath):
        matriz = []
        with open(txtFilePath, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                lista = []
                palabras = linea.split()  # Se separan las palabras por espacios
                for palabra in palabras:
                    lista.append(palabra)
                matriz.append(lista)
        return matriz

    def leerTxtFilenUM(self, txtFilePath):
        matriz = []
        with open(txtFilePath, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                lista = []
                palabras = linea.split()  # Se separan las palabras por espacios
                for palabra in palabras:
                    # Verificar si la palabra es un número
                    try:
                        # Intentar convertir a float
                        if '.' in palabra:
                            lista.append(float(palabra))
                        else:
                            # Si no tiene punto, intentar convertir a int
                            lista.append(int(palabra))
                    except ValueError:
                        # Si no es ni int ni float, se mantiene como string
                        lista.append(palabra)
                matriz.append(lista)
        return matriz


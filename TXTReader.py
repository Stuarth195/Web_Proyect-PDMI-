
class LectorTXT:

    def leerTxtFile(self, txtFilePath):
        matriz = []
        with open(txtFilePath, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                lista = []
                palabras = linea.split()
                for palabra in palabras:
                    lista.append(palabra)
                matriz.append(lista)
        return matriz
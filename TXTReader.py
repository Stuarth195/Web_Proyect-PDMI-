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

# Crear instancia de LectorTXT
ABC = LectorTXT()

# Asegúrate de que la ruta del archivo sea correcta
ruta_archivo = os.path.join("LISTA PRODUCTO Y RECETAS", "Receta.txt")

# Leer el archivo con el método adecuado
abcmayh = ABC.leerTxtFilenUM(ruta_archivo)

# Mostrar los resultados
print((abcmayh[0][5])*2)

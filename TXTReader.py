import tkinter as tk
from tkinter import messagebox
import re

class LectorTXT:
    def leerTxtFile(self, txtFilePath):

        """
        Lee un archivo TXT y devuelve una matriz de palabras por línea,
        eliminando previamente las líneas en blanco.
        """
        matriz = []
        try:
            with open(txtFilePath, 'r', encoding='utf-8') as archivo:
                # Filtrar y procesar solo las líneas que no estén vacías
                lineas = [linea.strip() for linea in archivo if linea.strip()]
                for linea in lineas:
                    palabras = linea.split()  # Dividir la línea en palabras
                    matriz.append(palabras)
        except FileNotFoundError:
            print(f"El archivo '{txtFilePath}' no fue encontrado.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
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

    def verificarYContarFecha(self, txtFilePath, fecha):
        if not self.verificarFormatoFecha(fecha):
            print(f"Fecha '{fecha}' no tiene el formato correcto (año-mes-día).")
            return
        
        matriz = self.leerTxtFile(txtFilePath)
        fecha_encontrada = False
        for linea in matriz:
            if linea and linea[0] == fecha:  # Asumimos que la fecha está en la primera columna
                fecha_encontrada = True
                # Incrementamos el contador
                contador = int(linea[1]) + 1  # Suponemos que el contador está en la segunda columna
                linea[1] = f"{contador:03}"  # Formateamos el contador a tres dígitos
                break
        
        if not fecha_encontrada:
            # Si la fecha no se encuentra, la agregamos con el contador en 000
            matriz.append([fecha, "000"])
        
        # Guardamos el archivo de nuevo con los cambios
        with open(txtFilePath, 'w', encoding='utf-8') as archivo:
            for linea in matriz:
                archivo.write(" ".join(linea) + '\n')

    def verificarFormatoFecha(self, fecha):
        # Expresión regular para verificar si la fecha tiene el formato año-mes-día
        patron = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
        return bool(re.match(patron, fecha))
    
    def leerTxtFilenUMII(self, txtFilePath):
        """
        Lee un archivo TXT y retorna una matriz con cada fila como lista de cadenas,
        limpiando espacios adicionales en los elementos.
        """
        matriz = []
        with open(txtFilePath, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                columnas = [col.strip() for col in linea.split()]  # Limpia espacios en cada columna
                if columnas:  # Evita agregar filas vacías
                    matriz.append(columnas)
        return matriz

    def eliminar_lineas_blanco(self, ruta_archivo):
        """
        Elimina las líneas en blanco de un archivo de texto y sobrescribe el archivo original.
        
        Parámetros:
        ruta_archivo (str): Ruta del archivo que se va a procesar.
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

            # Filtrar líneas que no están vacías o no son espacios en blanco
            lineas_no_vacias = [linea for linea in lineas if linea.strip()]

            # Sobrescribir el archivo original con las líneas filtradas
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.writelines(lineas_no_vacias)

            print(f"Líneas en blanco eliminadas. El archivo '{ruta_archivo}' ha sido actualizado.")
        except FileNotFoundError:
            print(f"Error: El archivo '{ruta_archivo}' no existe.")
        except Exception as e:
            print(f"Se produjo un error: {e}")


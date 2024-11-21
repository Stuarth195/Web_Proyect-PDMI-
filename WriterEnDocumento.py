
from TXTReader import LectorTXT

class Writer():

    def __init__(self):
        self.Lector = LectorTXT()
    def write(self, Filepath, mensaje):
        try:
            with open(Filepath, 'a', encoding='utf-8') as archivo:
                archivo.write("\n" + mensaje)
        except FileNotFoundError:
            print("No existe el archivo")

    def reemplazar_linea_en_archivo(self, nombre_archivo, mensaje_buscar):
        try:
            # Abrir el archivo en modo lectura
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

            # Abrir el archivo en modo escritura (se sobrescribirá)
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                for linea in lineas:
                    # Si la línea contiene el mensaje a buscar, reemplazarla
                    if mensaje_buscar in linea:
                        archivo.write("")
                    else:
                        archivo.write(linea)
        except FileNotFoundError:
            print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
        except Exception as e:
            print(f"Error: {e}")

    def Agregar_al_final(self, nombre_archivo, mensaje_buscar, mensaje, user):
        try:
            # Leer el contenido del archivo
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

            # Procesar las líneas y añadir el mensaje cuando se encuentra el texto buscado
            encontrado = False
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                for linea in lineas:
                    if mensaje_buscar in linea:
                        # Si encontramos el mensaje a buscar, agregamos el mensaje al final de la línea
                        archivo.write(linea.strip() + mensaje + "\n")
                        encontrado = True
                    else:
                        # Si no es la línea que buscamos, escribimos la línea original
                        archivo.write(linea)

                # Si no se encontró el mensaje buscado, lo agregamos al final
                if not encontrado:
                    archivo.write(user + mensaje + "\n")

        except FileNotFoundError:
            print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
        except Exception as e:
            print(f"Error: {e}")

    def limpiartxt(self, nombre_archivo):
        try:
            # Abrimos el archivo en modo escritura, lo que borra todo su contenido
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                pass  # No escribimos nada, solo cerramos el archivo vacío
            print(f"El contenido del archivo '{nombre_archivo}' ha sido borrado.")
        except FileNotFoundError:
            print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
        except Exception as e:
            print(f"Error: {e}")

    def rebajar_Lote(self, nombre_archivo, cantidad, producto):
        try:
            # Abre el archivo para leer las líneas
            lineas = self.Lector.leerTxtFile(nombre_archivo)

            Nuevas_lineas = []

            # Itera sobre las líneas para encontrar las entradas del producto
            for linea in lineas:
                ProductoTemp = ""
                Tipo_producto = False

                if linea != []:
                # Busca el producto en la línea
                    for letra in linea[1]:
                        if letra == "(":
                            ProductoTemp = ""  # Comienza a capturar el nombre del producto
                            Tipo_producto = True
                        elif letra == ")":
                            Tipo_producto = False
                        elif Tipo_producto:
                            ProductoTemp += letra
                    if ProductoTemp.strip() == "":
                        ProductoTemp = linea[1]

                    if ProductoTemp == producto:
                        linea[3] = float(linea[3]) - cantidad
                        linea[3] = str(linea[3])

                    strTemp = ""
                    for palabra in linea:
                        strTemp += palabra + " "

                    Nuevas_lineas.append(strTemp)
            self.limpiartxt(nombre_archivo)
            for linea in Nuevas_lineas:
                self.write(nombre_archivo, linea)


        except FileNotFoundError:
            print("No existe el archivo")


    # Ejecución
if __name__ == "__main__":
    Escritor = Writer()
    Escritor.rebajar_Lote("LISTA PRODUCTO Y RECETAS/M_A.txt", 17.0, "Paquete_de_500g")
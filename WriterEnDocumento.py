
class Writer():
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
                        # Si encontramos el mensaje a buscar, modificamos la línea
                        archivo.write(linea + " " + mensaje + "\n")
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


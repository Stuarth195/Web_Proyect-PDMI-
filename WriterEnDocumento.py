
class Writer():
    def write(self, Filepath, mensaje):
        with open(Filepath, 'a', encoding='utf-8') as archivo:
            archivo.write("\n" + mensaje)

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
import re


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
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

            cantidad_restante = cantidad  # La cantidad que aún necesitamos rebajar
            print(f"Cantidad total a rebajar: {cantidad_restante}")

            # Itera sobre las líneas para encontrar las entradas del producto
            for i, linea in enumerate(lineas):
                linea = linea.strip()
                ProductoTemp = ""
                Tipo_producto = False

                # Busca el producto en la línea
                for letra in linea:
                    if letra == "(":
                        ProductoTemp = ""  # Comienza a capturar el nombre del producto
                        Tipo_producto = True
                    elif Tipo_producto:
                        if letra == ")":
                            if ProductoTemp == producto:
                                Tipo_producto = False
                        ProductoTemp += letra
                    elif Tipo_producto == False and ProductoTemp != "":
                        # Verifica si el producto encontrado es el correcto
                        ProductoTemp = ProductoTemp.strip()
                        if producto in ProductoTemp:  # Usa 'in' para coincidencias parciales

                            # Busca el número al final de la línea (cantidad)
                            match = re.search(r'(\d+)$', linea.strip())
                            if match:
                                cantidad_actual = int(match.group(1))

                                if cantidad_restante <= cantidad_actual:
                                    # Si hay suficiente cantidad en esta línea, rebaja y termina
                                    nueva_cantidad = cantidad_actual - cantidad_restante
                                    lineas[i] = re.sub(r'(\d+)$', str(nueva_cantidad), linea.strip())
                                    cantidad_restante = 0  # Ya se ha rebajado todo lo necesario
                                    break  # Ya se ha rebajado la cantidad, terminamos
                                else:
                                    # Si no hay suficiente cantidad, rebaja todo lo que pueda y pasa a la siguiente línea
                                    cantidad_restante -= cantidad_actual
                                    lineas[i] = re.sub(r'(\d+)$', '0', linea.strip())

                            else:
                                print(f"No se encontró una cantidad válida en la línea: {linea}")

                # Si hemos rebajado toda la cantidad necesaria, ya no necesitamos seguir buscando
                if cantidad_restante == 0:
                    break

            # Si la cantidad restante es mayor a 0 después de recorrer todas las líneas, significa que no había suficiente stock
            if cantidad_restante > 0:
                print(
                    f"Error: No hay suficiente cantidad de {producto} en el archivo para rebajar la cantidad solicitada.")
            else:
                # Reescribe el archivo con las nuevas cantidades
                with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                    for linea in lineas:
                        if linea.split() != "":
                            archivo.write(linea + '\n')

        except Exception as e:
            print(f"Se produjo un error: {e}")
        try:
            # Abre el archivo para leer las líneas
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

            # Elimina las líneas vacías o que solo tienen espacios en blanco
            lineas_sin_vacias = [linea for linea in lineas if linea.strip() != ""]

            # Reescribe el archivo sin las líneas vacías
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.writelines(lineas_sin_vacias)

        except Exception as e:
            print(f"Se produjo un error: {e}")


    # Ejecución
if __name__ == "__main__":
    Escritor = Writer()
    Escritor.rebajar_Lote("LISTA PRODUCTO Y RECETAS/Lotes.txt", 9, "Paquete_de_200g")
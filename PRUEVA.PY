def eliminar_lineas_blanco(ruta_archivo):
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

# Ejemplo de uso
eliminar_lineas_blanco("RegistroCompras.txt")

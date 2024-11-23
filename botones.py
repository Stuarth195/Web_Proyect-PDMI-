import os
import tkinter as tk
from tkinter import Label, Button, Toplevel, messagebox
from PIL import Image, ImageTk  # Manejo de imágenes
from TXTReader import LectorTXT
import verify as vr
class Botones:
    def __init__(self, base_dir="LISTA PRODUCTO Y RECETAS"):
        """
        Inicializa la clase Botones con las rutas absolutas de los archivos necesarios.
        """
        # Base directory donde se encuentran los archivos
        base_dir = os.path.abspath(base_dir)

        # Instanciamos el lector de archivos
        self.Lector = LectorTXT()

        # Rutas absolutas de los archivos
        self.archivo_MA = os.path.join(base_dir, "M_A.txt")
        self.archivo_PE = os.path.join(base_dir, "PE.txt")
        self.archivo_Receta = os.path.join(base_dir, "Receta.txt")
        self.archivo_cosecha = os.path.join(base_dir, "COSECHA.txt")
        self.archivo_lotes = os.path.join(base_dir, "Lotes.txt")

        # Verificar existencia de archivos
        self._verificar_archivos()

    def _verificar_archivos(self):
        """Verifica que todos los archivos necesarios existan."""
        archivos = [self.archivo_MA, self.archivo_lotes]
        for archivo in archivos:
            if not os.path.exists(archivo):
                raise FileNotFoundError(f"El archivo '{archivo}' no se encuentra.")

    def leer_lotes(self):
        """Lee el archivo Lotes.txt y suma las cantidades por código de producto."""
        matriz_lotes = self.Lector.leerTxtFilenUM(self.archivo_lotes)
        cantidades_totales = {}

        for fila in matriz_lotes:
            codigo_producto = fila[1]  # Código de producto en segunda posición
            cantidad = int(fila[-1])  # Cantidad en la última posición
            if codigo_producto in cantidades_totales:
                cantidades_totales[codigo_producto] += cantidad
            else:
                cantidades_totales[codigo_producto] = cantidad

        return cantidades_totales

    def actualizar_cantidades(self):
        """Actualiza las cantidades en el archivo M_A.txt según los datos de Lotes.txt."""
        # Leer las cantidades de los lotes
        cantidades_totales = self.leer_lotes()
        matriz_MA = self.Lector.leerTxtFilenUM(self.archivo_MA)

        # Actualizar las cantidades en M_A
        for fila in matriz_MA:
            codigo_producto = fila[0]  # Código de producto en primera posición
            if codigo_producto in cantidades_totales:
                fila[3] = str(cantidades_totales[codigo_producto])  # Actualizar cantidad

        # Guardar los cambios
        self.escribir_MA(matriz_MA)

    def escribir_MA(self, matriz_MA):
        """Escribe la matriz actualizada de productos en el archivo M_A.txt."""
        with open(self.archivo_MA, "w", encoding="utf-8") as archivo:
            for fila in matriz_MA:
                # Convertir todos los elementos de fila a cadenas antes de unirlos
                fila_str = [str(elemento) for elemento in fila]
                archivo.write(" ".join(fila_str) + "\n")

    def visualizar_productos(self, ventana):
        """Muestra botones de productos en la ventana principal."""
        # Leer los productos desde M_A.txt
        matriz_MA = self.Lector.leerTxtFilenUM(self.archivo_MA)

        # Crear un marco de desplazamiento
        frame = tk.Frame(ventana)
        frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Crear botones para cada producto
        for producto in matriz_MA:
            # Verificar si la fila tiene suficientes elementos
            if len(producto) > 1:
                nombre = producto[1]
                boton = Button(scrollable_frame, text=f"{nombre}", command=lambda p=producto: self.mostrar_detalle_producto(p))
                boton.pack(pady=5, padx=10, fill="x")
            else:
                print(f"Advertencia: la fila {producto} no tiene suficientes elementos.")

    def mostrar_detalle_producto(self, producto):
        """Actualiza los datos y muestra una ventana con los detalles del producto."""
        # Leer los datos actualizados de M_A.txt
        matriz_MA = self.Lector.leerTxtFilenUM(self.archivo_MA)

        # Buscar el producto actualizado en la matriz
        codigo_producto = producto[0]
        producto_actualizado = None
        for fila in matriz_MA:
            # Verificar si la fila tiene suficientes elementos antes de acceder a ella
            if len(fila) > 0 and fila[0] == codigo_producto:
                producto_actualizado = fila
                break

        if not producto_actualizado:
            raise ValueError(f"El producto con código {codigo_producto} no se encontró después de actualizar.")

        # Desempaquetar datos del producto actualizado
        codigo, nombre, descripcion, cantidad, unidad_medida, precio = producto_actualizado

        # Crear la ventana de detalle
        ventana_detalle = Toplevel()
        ventana_detalle.title(f"Detalles de {nombre}")

        # Ruta de la imagen
        ruta_imagen = os.path.join("Imagenes", "Productos", f"{codigo}.png")

        # Cargar imagen
        try:
            imagen = Image.open(ruta_imagen)
            imagen.thumbnail((200, 200))
            imagen_tk = ImageTk.PhotoImage(imagen)

            label_imagen = Label(ventana_detalle, image=imagen_tk)
            label_imagen.image = imagen_tk  # Mantener referencia
            label_imagen.pack(pady=10)
        except FileNotFoundError:
            label_imagen = Label(ventana_detalle, text="Imagen no disponible", bg="gray", width=50, height=20)
            label_imagen.pack(pady=10)

        # Mostrar la información del producto
        label_info = Label(
            ventana_detalle,
            text=f"Código: {codigo}\nNombre: {nombre}\nDescripción: {descripcion}\nCantidad: {cantidad}\n"
                f"Unidad de Medida: {unidad_medida}\nPrecio: ${precio}",
            justify="left",
            anchor="w"
        )
        label_info.pack(pady=10, padx=10)

        # Botón cerrar
        boton_cerrar = Button(ventana_detalle, text="Cerrar", command=ventana_detalle.destroy)
        boton_cerrar.pack(pady=10)

#-___________________________________________________________________________________________________-

    def verifica_codigo(self, codigo):
        """
        Verifica si el código existe en los archivos correspondientes.
        
        Args:
            codigo (str): El código a buscar.
        
        Returns:
            bool: True si el código existe en alguno de los archivos, False en caso contrario.
        """
        # Leer los datos de los archivos usando LectorTXT
        matriz_ac = self.Lector.leerTxtFile(self.archivo_cosecha)
        matriz_MA = self.Lector.leerTxtFile(self.archivo_MA)
        matriz_PE = self.Lector.leerTxtFile(self.archivo_PE)

        # Verificar en cada archivo si el código está presente
        for linea in matriz_ac:
            if linea and linea[0] == codigo:
                self.descripcion =linea[1]
                return True  # Código encontrado en archivo_cosecha
        for linea in matriz_MA:
            if linea and linea[0] == codigo:
                self.descripcion =linea[1]
                return True  # Código encontrado en archivo_MA
                print("se pudo")
        for linea in matriz_PE:
            if linea and linea[0] == codigo:
                self.descripcion =linea[1]
                return True
                print("se pudo")  # Código encontrado en archivo_PE

        return False
        print("NO se pudo")  # Código no encontrado en ningún archivo


    def escribe_lote(self, ventana_form, fecha, codigo, cantidad, unidad, proveedor, ruta_archivo):
        """
        Escribe la información de un lote en el archivo proporcionado por el usuario.

        Args:
            ventana_form: Ventana que activa el formulario.
            fecha (str): Fecha del lote (formato yyyymmdd).
            codigo (str): Código del producto.
            cantidad (str): Cantidad del lote (validada y convertida a número).
            unidad (str): Unidad de medida (Paquete, Litros, etc.).
            proveedor (str): Nombre del proveedor.
            ruta_archivo (str): Ruta donde se guardará el archivo de lotes.
        """
        # Verifica si el código existe y obtiene la descripción
        if not self.verifica_codigo(codigo):
            messagebox.showerror("Error", f"El código '{codigo}' no existe en los archivos. Vuelve a intentarlo.")
            return False

        # Validar cantidad como entero o flotante según la unidad
        cantidad = int(cantidad) if unidad in ["Unidad", "Lata", "Botella", "Paquete"] else float(cantidad)

        # Obtener el contador del lote
        instvr = vr.FechaContador()
        instvr.procesar_fecha(fecha, codigo)
        contador = instvr.obtener_contador(fecha, codigo)

        # Formatear la fecha
        fecha_formateada = instvr.formatear_fecha(fecha)

        # Construir el identificador del lote
        identificador_lote = f"{codigo}_{fecha}_{contador}"

        # Obtener la descripción del producto
        descripcion = self.descripcion  # Esta es la descripción obtenida con `verifica_codigo`

        # Formatear la línea del lote
        linea_lote = f"{identificador_lote} {codigo} {descripcion} {fecha_formateada} {proveedor} {unidad} {cantidad}\n"

        # Abrir el archivo y asegurarse de que no haya una línea vacía al final antes de escribir
        with open(ruta_archivo, "a+", encoding="utf-8") as archivo:
            # Mover el cursor al final del archivo
            archivo.seek(0, 2)
            # Si la última línea está vacía, eliminarla
            archivo.seek(archivo.tell() - 1, 0)
            if archivo.read(1) == "\n":
                archivo.truncate()
            
            # Escribir la línea del lote
            archivo.write(linea_lote)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", f"Lote registrado en: {ruta_archivo}\n{linea_lote.strip()}")
        cantidad_numerica = int(cantidad) if unidad in ["Unidad", "Lata", "Botella", "Paquete"] else float(cantidad)
        self.buscar_y_actualizar_lote(codigo, cantidad_numerica)

        print(f"Lote registrado: {linea_lote.strip()} en {ruta_archivo}")  # Para depuración

    def buscar_y_actualizar_lote(self, codigo, cantidad_a_sumar):
        """
        Busca un código en los archivos M_A.txt, PE.txt y COSECHA.txt y actualiza la cantidad correspondiente.
        
        Args:
            codigo (str): El código del producto a buscar.
            cantidad_a_sumar (int o float): La cantidad que se debe sumar al campo correspondiente.
        """
        archivos = {
            "M_A": {"ruta": self.archivo_MA, "indice_cantidad": 3},  # La cantidad está en el cuarto elemento.
            "PE": {"ruta": self.archivo_PE, "indice_cantidad": -1},  # La cantidad está en el último elemento.
            "COSECHA": {"ruta": self.archivo_cosecha, "indice_cantidad": -1}  # Igual que en PE.
        }
        
        for nombre, datos in archivos.items():
            ruta = datos["ruta"]
            indice_cantidad = datos["indice_cantidad"]
            
            # Leer el archivo
            matriz = self.Lector.leerTxtFilenUM(ruta)
            codigo_encontrado = False

            for fila in matriz:
                if fila[0] == codigo:  # Si el código coincide
                    try:
                        fila[indice_cantidad] = str(float(fila[indice_cantidad]) + cantidad_a_sumar)
                        codigo_encontrado = True
                    except ValueError:
                        print(f"Error al convertir la cantidad en el archivo {nombre}. Verifica los datos.")
                    break
            
            if codigo_encontrado:
                # Guardar los cambios en el archivo
                with open(ruta, "w", encoding="utf-8") as archivo:
                    for fila in matriz:
                        archivo.write(" ".join(map(str, fila)) + "\n")
                print(f"Código '{codigo}' actualizado exitosamente en {nombre}.")
                return
        
        print(f"Código '{codigo}' no encontrado en ninguno de los archivos.")

import os
import tkinter as tk
from tkinter import Button, Label, Entry, Toplevel, messagebox
from PIL import Image, ImageTk  # Manejo de imágenes
from TXTReader import LectorTXT
import verify as vr

class BotonesPE:
    def __init__(self, base_dir="LISTA PRODUCTO Y RECETAS"):
        """
        Inicializa la clase BotonesPE con las rutas absolutas de los archivos necesarios.
        """
        base_dir = os.path.abspath(base_dir)

        self.Lector = LectorTXT()

        # Rutas absolutas de los archivos
        self.archivo_PE = os.path.join(base_dir, "PE.txt")
        self.archivo_lotes = os.path.join(base_dir, "Lotes.txt")

        # Verificar existencia de archivos
        self._verificar_archivos()

    def _verificar_archivos(self):
        """Verifica que los archivos PE.txt y Lotes.txt existan."""
        archivos = [self.archivo_PE, self.archivo_lotes]
        for archivo in archivos:
            if not os.path.exists(archivo):
                raise FileNotFoundError(f"El archivo '{archivo}' no se encuentra.")

    def leer_lotes(self):
        """Lee el archivo Lotes.txt y suma las cantidades por código de producto."""
        matriz_lotes = self.Lector.leerTxtFilenUM(self.archivo_lotes)
        cantidades_totales = {}

        for fila in matriz_lotes:
            codigo_producto = fila[1]  # Código de producto en segunda posición
            cantidad = int(fila[-1])  # Cantidad en la última posición
            if codigo_producto in cantidades_totales:
                cantidades_totales[codigo_producto] += cantidad
            else:
                cantidades_totales[codigo_producto] = cantidad

        return cantidades_totales

    def actualizar_cantidades(self):
        """Actualiza las cantidades en el archivo PE.txt según los datos de Lotes.txt."""
        cantidades_totales = self.leer_lotes
        matriz_PE = self.Lector.leerTxtFilenUM(self.archivo_PE)

        # Actualizar las cantidades en PE
        for fila in matriz_PE:
            if len(fila) < 5:
                print(f"Error: la fila {fila} no tiene suficiente longitud.")
                continue

            codigo_producto = fila[0]  # Código de producto en primera posición
            if codigo_producto in cantidades_totales:
                fila[4] = str(cantidades_totales[codigo_producto])  # Actualizar cantidad

        # Guardar los cambios
        self.escribir_PE(matriz_PE)

    def escribir_PE(self, matriz_PE):
        """Escribe la matriz actualizada de productos en el archivo PE.txt."""
        with open(self.archivo_PE, "w", encoding="utf-8") as archivo:
            for fila in matriz_PE:
                fila_str = [str(elemento) for elemento in fila]
                archivo.write(" ".join(fila_str) + "\n")

    def visualizar_productos(self, ventana):
        """Muestra botones de productos de PE.txt en la ventana principal."""
        self.matriz_PE = self.Lector.leerTxtFilenUM(self.archivo_PE)

        # Crear un marco de desplazamiento
        frame = tk.Frame(ventana)
        frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Crear los botones de productos
        self.crear_botones_productos()

    def crear_botones_productos(self):
        """Crea los botones para cada producto en la lista PE."""
        for producto in self.matriz_PE:
            codigo, nombre, descripcion = producto[0], producto[1], producto[2]
            boton = Button(self.scrollable_frame, text=f"{nombre} ({codigo})", 
                           command=lambda p=producto: self.mostrar_detalle_producto(p))
            boton.pack(pady=5, padx=10, fill="x")

    def mostrar_detalle_producto(self, producto):
        """Muestra una ventana con los detalles del producto de PE.txt."""
        # Actualizar las cantidades en tiempo real


        matriz_PE = self.Lector.leerTxtFilenUM(self.archivo_PE)
        codigo_producto = producto[0]
        producto_actualizado = None
        for fila in matriz_PE:
            if fila[0] == codigo_producto:
                producto_actualizado = fila
                break

        if not producto_actualizado:
            raise ValueError(f"El producto con código {codigo_producto} no se encontró después de actualizar.")

        codigo, nombre, precio, unidad, cantidad = producto_actualizado[:5]

        ventana_detalle = Toplevel()
        ventana_detalle.title(f"Detalles de {nombre}")

        # Mostrar la información del producto
        label_info = Label(
            ventana_detalle,
            text=f"Código: {codigo}\nNombre: {nombre}\nPrecio: ${precio}\nUnidad: {unidad}\nCantidad: {cantidad}",
            justify="left",
            anchor="w"
        )
        label_info.pack(pady=10, padx=10)

        # Botón cerrar
        boton_cerrar = Button(ventana_detalle, text="Cerrar", command=ventana_detalle.destroy)
        boton_cerrar.pack(pady=10)
#_________________________________________________________________________________________

import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime

class ReciboCosecha:
    def __init__(self, contenedor, ruta_txt):
        self.contenedor = contenedor
        self.ruta_txt = ruta_txt
        self.crear_interfaz()

    def guardar_datos(self, fecha, finca, productos):
        with open(self.ruta_txt, "a") as file:
            for producto, cantidad in productos:
                line = f"{fecha} {finca} {producto} {cantidad}\n"
                file.write(line)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")

    def obtener_datos(self):
        fecha = self.entry_fecha.get()
        if not self.validar_fecha(fecha):
            messagebox.showwarning("Advertencia", "La fecha debe estar en formato YYYY-MM-DD.")
            return

        finca = self.entry_finca.get()
        if not finca or " " in finca:
            messagebox.showwarning("Advertencia", "El campo 'Finca' no puede estar vacío ni contener espacios.")
            return

        productos = []
        if self.var_papas.get():
            cantidad_papas = self.cantidad_papas_entry.get()
            if cantidad_papas.isdigit():
                productos.append(("Papas", cantidad_papas))
            else:
                messagebox.showwarning("Advertencia", "La cantidad de Papas debe ser un número válido.")
                return
        if self.var_tomates.get():
            cantidad_tomates = self.cantidad_tomates_entry.get()
            if cantidad_tomates.isdigit():
                productos.append(("Tomates", cantidad_tomates))
            else:
                messagebox.showwarning("Advertencia", "La cantidad de Tomates debe ser un número válido.")
                return
        if self.var_otros.get():
            cantidad_otros = self.cantidad_otros_entry.get()
            descripcion = self.descripcion_otros_entry.get()
            if cantidad_otros.isdigit() and descripcion and re.match("^[A-Za-z_]+$", descripcion):
                productos.append((descripcion, cantidad_otros))
            else:
                messagebox.showwarning("Advertencia", "La cantidad y descripción de 'Otros' deben ser válidas.")
                return

        if not productos:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos un producto.")
            return

        self.guardar_datos(fecha, finca, productos)

    def validar_fecha(self, fecha):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validar_sin_espacios(self, texto):
        return " " not in texto

    def crear_interfaz(self):
        frame = tk.Frame(self.contenedor)
        frame.pack(padx=10, pady=10)

        validate_entry = self.contenedor.register(self.validar_sin_espacios)

        # Fecha de Cosecha
        tk.Label(frame, text="Fecha de Cosecha (YYYY-MM-DD)").grid(row=0, column=0, padx=10, pady=5)
        self.entry_fecha = tk.Entry(frame, validate="key", validatecommand=(validate_entry, "%P"))
        self.entry_fecha.grid(row=0, column=1, padx=10, pady=5)

        # Finca
        tk.Label(frame, text="Finca o Proveedor").grid(row=1, column=0, padx=10, pady=5)
        self.entry_finca = tk.Entry(frame, validate="key", validatecommand=(validate_entry, "%P"))
        self.entry_finca.grid(row=1, column=1, padx=10, pady=5)

        # Selección de productos
        tk.Label(frame, text="Selecciona Productos").grid(row=2, column=0, padx=10, pady=5)

        # Papas
        self.var_papas = tk.BooleanVar()
        tk.Checkbutton(frame, text="Papas", variable=self.var_papas, command=self.toggle_papas).grid(row=3, column=0, padx=10, pady=5)
        self.cantidad_papas_entry = tk.Entry(frame, state="disabled", validate="key", validatecommand=(validate_entry, "%P"))
        tk.Label(frame, text="Cantidad").grid(row=3, column=1, padx=5, pady=5)
        self.cantidad_papas_entry.grid(row=3, column=2, padx=10, pady=5)

        # Tomates
        self.var_tomates = tk.BooleanVar()
        tk.Checkbutton(frame, text="Tomates", variable=self.var_tomates, command=self.toggle_tomates).grid(row=4, column=0, padx=10, pady=5)
        self.cantidad_tomates_entry = tk.Entry(frame, state="disabled", validate="key", validatecommand=(validate_entry, "%P"))
        tk.Label(frame, text="Cantidad").grid(row=4, column=1, padx=5, pady=5)
        self.cantidad_tomates_entry.grid(row=4, column=2, padx=10, pady=5)

        # Otros
        self.var_otros = tk.BooleanVar()
        tk.Checkbutton(frame, text="Otros", variable=self.var_otros, command=self.toggle_otros).grid(row=5, column=0, padx=10, pady=5)
        self.cantidad_otros_entry = tk.Entry(frame, state="disabled", validate="key", validatecommand=(validate_entry, "%P"))
        tk.Label(frame, text="Cantidad").grid(row=5, column=1, padx=5, pady=5)
        self.cantidad_otros_entry.grid(row=5, column=2, padx=10, pady=5)
        tk.Label(frame, text="Descripción").grid(row=6, column=0, padx=10, pady=5)
        self.descripcion_otros_entry = tk.Entry(frame, state="disabled", validate="key", validatecommand=(validate_entry, "%P"))
        self.descripcion_otros_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=5)

        # Botón para guardar
        tk.Button(frame, text="Guardar", command=self.obtener_datos).grid(row=7, column=0, columnspan=3, pady=10)

    def toggle_papas(self):
        self.cantidad_papas_entry.config(state="normal" if self.var_papas.get() else "disabled")

    def toggle_tomates(self):
        self.cantidad_tomates_entry.config(state="normal" if self.var_tomates.get() else "disabled")

    def toggle_otros(self):
        estado = "normal" if self.var_otros.get() else "disabled"
        self.cantidad_otros_entry.config(state=estado)
        self.descripcion_otros_entry.config(state=estado)

    def limpiar_interfaz(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    

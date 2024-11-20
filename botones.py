import os
import tkinter as tk
from tkinter import Label, Button, Toplevel
from PIL import Image, ImageTk  # Manejo de imágenes
from TXTReader import LectorTXT

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
        # Actualizar las cantidades antes de visualizar
        self.actualizar_cantidades()
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
            nombre = producto[1]
            boton = Button(scrollable_frame, text=f"{nombre}", command=lambda p=producto: self.mostrar_detalle_producto(p))
            boton.pack(pady=5, padx=10, fill="x")

    def mostrar_detalle_producto(self, producto):
        """Actualiza los datos y muestra una ventana con los detalles del producto."""
        # Actualizar las cantidades en tiempo real
        self.actualizar_cantidades()

        # Leer los datos actualizados de M_A.txt
        matriz_MA = self.Lector.leerTxtFilenUM(self.archivo_MA)

        # Buscar el producto actualizado en la matriz
        codigo_producto = producto[0]
        producto_actualizado = None
        for fila in matriz_MA:
            if fila[0] == codigo_producto:
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

        # Mostrar información del producto
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

    def verifica_codigo(self,codigo, fecha_str, cantidad, proveedor):
        # Convertir la fecha a formato datetime
        self.matriz_ac =LectorTXT.leerTxtFile(self.archivo_cosecha)
        self.matrizMA = LectorTXT.leerTxtFile(self.archivo_MA)
        self.matrizPE = LectorTXT.leerTxtFile(self.archivo_PE)

        for linea in self.matriz_ac:
            if linea[0] == codigo:
                print("hola")
        for linea in self.matrizMA:
            if linea[0] == codigo:
                print("hola")
        for linea in self.matrizPE:
            if linea[0] == codigo:
                print("hola")

    #def escribe_lote(rutatxt ,codigo, fecha, cantidad, provedor):
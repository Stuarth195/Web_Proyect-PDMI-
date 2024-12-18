import tkinter as tk
from tkinter import messagebox, Toplevel
import re
import os
from datetime import datetime, timedelta


class FechaEntradaApp:
    def __init__(self, ventana_principal):
        self.fecha_guardada = None  # Variable para almacenar la fecha ingresada
        self.ventana_principal = ventana_principal

        # Asignar el manejador al evento de cierre de la ventana principal
        self.ventana_principal.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.crear_interfaz()

    def crear_interfaz(self):
        # Crear el Label para la fecha dentro de la ventana principal
        label = tk.Label(self.ventana_principal, text="Ingrese la fecha en formato YYYY-MM-DD:")
        label.pack(pady=10)

        # Campo de entrada para la fecha
        self.entrada_fecha = tk.Entry(self.ventana_principal, width=15)
        self.entrada_fecha.pack(pady=5)

        # Asignar el evento para controlar la entrada de caracteres
        self.entrada_fecha.bind("<KeyRelease>", self.validar_entrada)

        # Crear un Frame para colocar los botones de forma horizontal
        frame_botones = tk.Frame(self.ventana_principal)
        frame_botones.pack(pady=10)

        # Botón para verificar y aceptar la fecha
        boton_aceptar = tk.Button(frame_botones, text="Aceptar", command=self.verificarYAceptar)
        boton_aceptar.pack(side=tk.LEFT, padx=5)

        # Botón para mostrar la fecha guardada
        boton_mostrar = tk.Button(frame_botones, text="Mostrar Fecha Guardada", command=self.mostrar_fecha)
        boton_mostrar.pack(side=tk.LEFT, padx=5)


    def validar_entrada(self, event):
        fecha = self.entrada_fecha.get()
        # Solo permitir 4 dígitos para el año y luego un guion
        if len(fecha) == 4 and not fecha.endswith('-'):
            self.entrada_fecha.insert(4, '-')
        # Solo permitir 2 dígitos para el mes (01-12)
        elif len(fecha) == 7 and not fecha.endswith('-'):
            self.entrada_fecha.insert(7, '-')
        # Restringir los días (01-31)
        if len(fecha) == 10:
            mes = fecha[5:7]
            if mes in ["01", "03", "05", "07", "08", "10", "12"]:
                max_dia = "31"
            elif mes in ["04", "06", "09", "11"]:
                max_dia = "30"
            else:  # Febrero
                max_dia = "28"  # No estamos considerando años bisiestos aquí
            # Limitar el día máximo según el mes
            dia = fecha[8:]
            if dia > max_dia:
                self.entrada_fecha.delete(8, tk.END)

    def verificarYAceptar(self):
        fecha = self.entrada_fecha.get()
        if self.verificarFormatoFecha(fecha):
            # Eliminar los guiones y guardar la fecha
            fecha_sin_guiones = fecha.replace('-', '')
            self.fecha_guardada = fecha_sin_guiones
            print(f"Fecha guardada: {self.fecha_guardada}")  # Ejemplo: 20241203
        else:
            # Si la fecha no es válida, mostrar mensaje de error
            messagebox.showerror("Error", "La fecha no está en el formato correcto (YYYY-MM-DD).")
        self.ventana_principal.focus()

    def verificarFormatoFecha(self, fecha):
        # Expresión regular para verificar si la fecha tiene el formato año-mes-día
        patron = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
        return bool(re.match(patron, fecha))

    def mostrar_fecha(self):
        if self.fecha_guardada:
            messagebox.showinfo("Fecha Guardada", f"La fecha ingresada es: {self.fecha_guardada}")
        else:
            messagebox.showwarning("Advertencia", "Aún no se ha ingresado una fecha válida.")
        
        # Hacer foco en la ventana principal después de cerrar el messagebox
        self.ventana_principal.focus()


    def cerrar_ventana(self):
        # Restablecer el valor de la fecha guardada a None
        self.fecha_guardada = None
        print("Fecha guardada restablecida a None.")
        self.ventana_principal.destroy()  # Cerrar la ventana principal

class CodigoApp:
    def __init__(self, ventana_principal):
        self.codigo_guardado = None  # Variable para almacenar el código ingresado
        self.ventana_principal = ventana_principal

        # Asignar el manejador al evento de cierre de la ventana principal
        self.ventana_principal.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.crear_interfaz()

    def crear_interfaz(self):
        # Crear el Label para el código dentro de la ventana principal
        label = tk.Label(self.ventana_principal, text="Ingrese el código (2-3 letras seguidas de un guion y 3 dígitos):")
        label.pack(pady=10)

        # Campo de entrada para el código
        self.entrada_codigo = tk.Entry(self.ventana_principal, width=15)
        self.entrada_codigo.pack(pady=5)

        # Asignar el evento para controlar la entrada de caracteres
        self.entrada_codigo.bind("<KeyRelease>", self.validar_entrada)

        # Crear un Frame para colocar los botones de forma horizontal
        frame_botones = tk.Frame(self.ventana_principal)
        frame_botones.pack(pady=10)

        # Botón para verificar y aceptar el código
        boton_aceptar = tk.Button(frame_botones, text="Aceptar", command=self.verificarYAceptar)
        boton_aceptar.pack(side=tk.LEFT, padx=5)

        # Botón para mostrar el código guardado
        boton_mostrar = tk.Button(frame_botones, text="Mostrar Código Guardado", command=self.mostrar_codigo)
        boton_mostrar.pack(side=tk.LEFT, padx=5)

    def validar_entrada(self, event):
        codigo = self.entrada_codigo.get()
        # Convertir a mayúsculas automáticamente
        self.entrada_codigo.delete(0, tk.END)
        self.entrada_codigo.insert(0, codigo.upper())

        # Asegurarse de que el código tenga el formato correcto
        if len(codigo) == 3 and not codigo.endswith('-'):
            self.entrada_codigo.insert(3, '-')
        elif len(codigo) == 7 and not codigo[4:].isdigit():
            self.entrada_codigo.delete(4, tk.END)

    def verificarYAceptar(self):
        codigo = self.entrada_codigo.get()
        if self.verificarFormatoCodigo(codigo):
            # Guardar el código tal cual (con guion incluido)
            self.codigo_guardado = codigo
            print(f"Código guardado: {self.codigo_guardado}")  # Ejemplo: TOM-001
        else:
            # Si el código no es válido, mostrar mensaje de error
            messagebox.showerror("Error", "El código no está en el formato correcto (XX-XXX).")
        self.ventana_principal.focus()

    def verificarFormatoCodigo(self, codigo):
        # Expresión regular para verificar si el código tiene el formato correcto
        patron = r"^[A-Z]{2,3}-\d{3}$"
        return bool(re.match(patron, codigo))

    def mostrar_codigo(self):
        if self.codigo_guardado:
            messagebox.showinfo("Código Guardado", f"El código ingresado es: {self.codigo_guardado}")
        else:
            messagebox.showwarning("Advertencia", "Aún no se ha ingresado un código válido.")
        
        # Hacer foco en la ventana principal después de cerrar el messagebox
        self.ventana_principal.focus()

    def cerrar_ventana(self):
        # Restablecer el valor del código guardado a None
        self.codigo_guardado = None
        print("Código guardado restablecido a None.")
        self.ventana_principal.destroy()  # Cerrar la ventana principal


class CantidadApp:
    def __init__(self, ventana_principal):
        self.cantidad_guardada = None  # Variable para almacenar la cantidad ingresada
        self.unidad = None  # Variable para almacenar la unidad seleccionada
        self.ventana_principal = ventana_principal

        # Asignar el manejador al evento de cierre de la ventana principal
        self.ventana_principal.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.crear_interfaz()
    def crear_interfaz(self):
        """Crea la interfaz gráfica para ingresar cantidad y seleccionar unidad."""
        # Crear el Label para la cantidad dentro de la ventana principal
        label = tk.Label(self.ventana_principal, text="Ingrese la cantidad:")
        label.pack(pady=10)

        # Campo de entrada para la cantidad
        self.entrada_cantidad = tk.Entry(self.ventana_principal, width=15)
        self.entrada_cantidad.pack(pady=5)

        # Asignar el evento para controlar la entrada de caracteres
        self.entrada_cantidad.bind("<KeyRelease>", self.validar_entrada)

        # Crear un Frame para los botones de selección de unidad
        frame_unidad = tk.Frame(self.ventana_principal)
        frame_unidad.pack(pady=10)

        # Botones de selección de unidad
        self.var_unidad = tk.StringVar(value="Kilogramos")  # Default es Kilogramos

        opciones = [
            ("Mililitros", "Mililitros"),
            ("Litros", "Litros"),
            ("Kilogramos", "Kilogramos"),
            ("Gramos", "Gramos"),
            ("Unidad", "Unidad"),
            ("Lata", "Lata"),
            ("Botella", "Botella"),
            ("Paquete", "Paquete")
        ]

        for texto, valor in opciones:
            boton = tk.Radiobutton(frame_unidad, text=texto, variable=self.var_unidad, value=valor)
            boton.pack(side=tk.LEFT, padx=10)

        # Crear un Frame para los botones de Aceptar y Mostrar en horizontal
        frame_botones = tk.Frame(self.ventana_principal)
        frame_botones.pack(pady=10)

        # Botón para verificar y aceptar la cantidad
        boton_aceptar = tk.Button(frame_botones, text="Aceptar", command=self.verificarYAceptar)
        boton_aceptar.pack(side=tk.LEFT, padx=10)

        # Botón para mostrar la cantidad guardada
        boton_mostrar = tk.Button(frame_botones, text="Mostrar Cantidad Guardada", command=self.mostrar_cantidad)
        boton_mostrar.pack(side=tk.LEFT, padx=10)


    def validar_entrada(self, event):
        cantidad = self.entrada_cantidad.get()

        # Permitir solo números y punto decimal
        if cantidad and not re.match(r'^\d*\.?\d*$', cantidad):
            self.entrada_cantidad.delete(len(cantidad)-1, tk.END)

    def verificarYAceptar(self):
        cantidad = self.entrada_cantidad.get()
        unidad_seleccionada = self.var_unidad.get()

        # Verificar que la cantidad ingresada sea válida
        if unidad_seleccionada == "Unidad" and '.' in cantidad:
            # Si la unidad es "Unidad", no puede ser un número flotante
            messagebox.showerror("Error", "Para 'Unidad' solo se permite números enteros.")
        elif cantidad and (cantidad.replace('.', '', 1).isdigit()):  # Permitir flotantes si no es unidad
            # Guardar la cantidad y la unidad seleccionada
            self.cantidad_guardada = cantidad
            self.unidad = unidad_seleccionada
            print(f"Cantidad guardada: {self.cantidad_guardada} {self.unidad}")
        else:
            # Si la cantidad no es válida
            messagebox.showerror("Error", "La cantidad ingresada no es válida.")
        
        self.ventana_principal.focus()

    def mostrar_cantidad(self):
        if self.cantidad_guardada:
            messagebox.showinfo("Cantidad Guardada", f"La cantidad ingresada es: {self.cantidad_guardada} {self.unidad}")
        else:
            messagebox.showwarning("Advertencia", "Aún no se ha ingresado una cantidad válida.")
        
        # Hacer foco en la ventana principal después de cerrar el messagebox
        self.ventana_principal.focus()

    def cerrar_ventana(self):
        # Restablecer el valor de la cantidad guardada a None
        self.cantidad_guardada = None
        self.unidad = None
        print("Cantidad guardada restablecida a None.")
        self.ventana_principal.destroy()  # Cerrar la ventana principal


class ProvedorApp:
    def __init__(self, ventana_principal):
        self.nombre_guardado = None  # Variable para almacenar el nombre del proveedor ingresado
        self.ventana_principal = ventana_principal

        # Asignar el manejador al evento de cierre de la ventana principal
        self.ventana_principal.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.crear_interfaz()

    def crear_interfaz(self):
        # Crear el Label para el nombre del proveedor dentro de la ventana principal
        label = tk.Label(self.ventana_principal, text="Ingrese el nombre del proveedor (letras, números y guion bajo):")
        label.pack(pady=10)

        # Campo de entrada para el nombre del proveedor
        self.entrada_nombre = tk.Entry(self.ventana_principal, width=25)
        self.entrada_nombre.pack(pady=5)

        # Asignar el evento para controlar la entrada de caracteres
        self.entrada_nombre.bind("<KeyRelease>", self.validar_entrada)

        # Crear un Frame para los botones de Aceptar y Mostrar en horizontal
        frame_botones = tk.Frame(self.ventana_principal)
        frame_botones.pack(pady=10)

        # Botón para verificar y aceptar el nombre
        boton_aceptar = tk.Button(frame_botones, text="Aceptar", command=self.verificarYAceptar)
        boton_aceptar.pack(side=tk.LEFT, padx=10)

        # Botón para mostrar el nombre guardado
        boton_mostrar = tk.Button(frame_botones, text="Mostrar Nombre Guardado", command=self.mostrar_nombre)
        boton_mostrar.pack(side=tk.LEFT, padx=10)

    def validar_entrada(self, event):
        nombre = self.entrada_nombre.get()

        # Verificar que no haya espacios y permitir letras, números y guion bajo
        if " " in nombre or not re.match("^[a-zA-Z0-9_]*$", nombre):
            messagebox.showerror("Error", "El nombre solo debe contener letras, números y guion bajo, sin espacios.")
            self.entrada_nombre.delete(0, tk.END)  # Limpiar el campo

    def verificarYAceptar(self):
        nombre = self.entrada_nombre.get()

        # Verificar que el nombre no esté vacío y sea válido
        if nombre and re.match("^[a-zA-Z0-9_]*$", nombre):  # Permitimos letras, números y guion bajo
            # Guardar el nombre ingresado
            self.nombre_guardado = nombre
            print(f"Nombre guardado: {self.nombre_guardado}")
        else:
            # Si el nombre no es válido
            messagebox.showerror("Error", "El nombre ingresado no es válido. Solo letras, números y guion bajo permitidos.")
        
        self.ventana_principal.focus()

    def mostrar_nombre(self):
        if self.nombre_guardado:
            messagebox.showinfo("Nombre Guardado", f"El nombre del proveedor es: {self.nombre_guardado}")
        else:
            messagebox.showwarning("Advertencia", "Aún no se ha ingresado un nombre válido.")
        
        # Hacer foco en la ventana principal después de cerrar el messagebox
        self.ventana_principal.focus()

    def cerrar_ventana(self):
        # Restablecer el valor del nombre guardado a None
        self.nombre_guardado = None
        print("Nombre guardado restablecido a None.")
        self.ventana_principal.destroy()  # Cerrar la ventana principal


# Ejecutar la prueba
import os
import re

class FechaContador:
    def __init__(self, ruta=os.path.join("LISTA PRODUCTO Y RECETAS", "contador_dia.txt")):
        self.ruta = ruta
        # Asegurarse de que el archivo existe al inicializar
        self._verificar_archivo()

    def _verificar_archivo(self):
        """Crea el archivo si no existe."""
        if not os.path.exists(self.ruta):
            with open(self.ruta, 'w') as archivo:
                pass  # Crear archivo vacío

    def procesar_fecha(self, fecha, codigo):
        """Procesa la fecha y el código para verificar o agregar al archivo."""
        # Validar el formato de la fecha y el código
        if len(fecha) != 8 or not fecha.isdigit():
            raise ValueError("La fecha debe tener el formato yyyymmdd.")
        if not re.match(r"^[A-Z]{2,3}-\d{3}$", codigo):
            raise ValueError("El código debe tener el formato XX-XXX.")

        with open(self.ruta, 'r') as archivo:
            lineas = archivo.readlines()

        # Buscar si ya existe la combinación de fecha y código
        nueva_linea = True
        for i, linea in enumerate(lineas):
            if linea.startswith(f"{fecha}") and linea.strip().endswith(codigo):
                # Si existe, incrementar el contador
                partes = linea.strip().split()
                contador = int(partes[1]) + 1
                lineas[i] = f"{fecha} {contador:03d} {codigo}\n"
                nueva_linea = False
                break

        if nueva_linea:
            # Si no existe, agregar una nueva línea
            lineas.append(f"{fecha} 001 {codigo}\n")

        # Guardar los cambios en el archivo
        with open(self.ruta, 'w') as archivo:
            archivo.writelines(lineas)

        print(f"Fecha {fecha} y código {codigo} procesados con éxito.")

    def obtener_contador(self, fecha, codigo):
        """Obtiene el contador para una fecha y código específicos."""
        # Validar el formato de la fecha y el código
        if len(fecha) != 8 or not fecha.isdigit():
            raise ValueError("La fecha debe tener el formato yyyymmdd.")
        if not re.match(r"^[A-Z]{2,3}-\d{3}$", codigo):
            raise ValueError("El código debe tener el formato XX-XXX.")

        with open(self.ruta, 'r') as archivo:
            lineas = archivo.readlines()

        for linea in lineas:
            if linea.startswith(f"{fecha}") and linea.strip().endswith(codigo):
                _, contador, _ = linea.strip().split()
                return f"{int(contador):03d}"

        # Si no se encuentra la combinación, retorna "000"
        return "000"


    def sumar_15_dias(self, fecha):
        """Suma 15 días a la fecha proporcionada en formato yyyymmdd."""
        # Convertir la fecha de string 'yyyymmdd' a un objeto datetime
        fecha_dt = datetime.strptime(fecha, "%Y%m%d")
        
        # Sumar 15 días
        fecha_dt += timedelta(days=15)
        
        # Retornar la fecha sumada en formato 'yyyymmdd'
        return fecha_dt.strftime("%Y%m%d")

    def formatear_fecha(self, fecha):
        fecha = self.sumar_15_dias(fecha)
        """Convierte la fecha del formato yyyymmdd a yyyy_mm_dd."""
        # Asumiendo que la fecha es un string con el formato 'yyyymmdd'
        año = fecha[:4]
        mes = fecha[4:6]
        dia = fecha[6:]
        formateada = f"{año}_{mes}_{dia}"
        return formateada
    


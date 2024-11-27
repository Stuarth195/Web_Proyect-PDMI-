import tkinter as tk
from tkinter import messagebox, Entry, Radiobutton, Label, Button
from pathlib import Path

class Precios:
    def __init__(self, frame, archivo_articulos, archivo_admins):
        self.frame = frame
        self.archivo_articulos = Path(archivo_articulos)
        self.archivo_admins = Path(archivo_admins)
        self.productos = {}
        self.radio_var = tk.StringVar()
        self.entries = {}

        self.cargar_articulos()
        self.crear_interfaz()

    def cargar_articulos(self):
        """Carga los artículos desde el archivo y los almacena en un diccionario."""
        if not self.archivo_articulos.exists():
            messagebox.showerror("Error", f"No se encontró {self.archivo_articulos}")
            return

        with open(self.archivo_articulos, 'r') as f:
            for linea in f:
                partes = linea.strip().split()
                if len(partes) >= 6:
                    codigo = partes[0]
                    descripcion = partes[1]
                    precio = partes[-1]  # Último elemento de la línea es el precio
                    self.productos[codigo] = {"descripcion": descripcion, "precio": precio, "linea": partes}

    def crear_interfaz(self):
        """Crea la interfaz de usuario con Radiobuttons y entradas para los precios."""
        row = 0
        for codigo, datos in self.productos.items():
            # Radiobutton para seleccionar el producto
            rad = Radiobutton(
                self.frame,
                text=f"{codigo} {datos['descripcion']}",
                variable=self.radio_var,
                value=codigo,
                command=self.habilitar_entry
            )
            rad.grid(row=row, column=0, sticky="w")

            # Entry para modificar el precio
            entry = Entry(self.frame, state="disabled")
            entry.insert(0, datos["precio"])
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries[codigo] = entry

            row += 1

        # Botón para aceptar cambios
        Button(self.frame, text="Aceptar", command=self.validar_cambios).grid(row=row, column=0, columnspan=2, pady=10)

    def habilitar_entry(self):
        """Habilita el Entry correspondiente al producto seleccionado."""
        codigo_seleccionado = self.radio_var.get()
        for codigo, entry in self.entries.items():
            if codigo == codigo_seleccionado:
                entry.config(state="normal")
            else:
                entry.config(state="disabled")

    def validar_cambios(self):
        """Valida los cambios en el precio e intenta guardar los datos."""
        codigo_seleccionado = self.radio_var.get()
        if not codigo_seleccionado:
            messagebox.showerror("Error", "Seleccione un producto.")
            return

        entry = self.entries[codigo_seleccionado]
        nuevo_precio = entry.get()

        try:
            # Validar que el nuevo precio sea un número válido
            nuevo_precio = float(nuevo_precio)
            if nuevo_precio <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número mayor a 0.")
            return

        # Pedir contraseña de administrador
        if not self.validar_admin():
            return

        # Actualizar solo el precio del producto seleccionado
        self.productos[codigo_seleccionado]["precio"] = str(nuevo_precio)
        self.productos[codigo_seleccionado]["linea"][-1] = str(nuevo_precio)
        self.guardar_cambios()
        messagebox.showinfo("Éxito", f"Precio de {codigo_seleccionado} actualizado a {nuevo_precio}.")

    def validar_admin(self):
        """Valida si la contraseña ingresada pertenece a un administrador."""
        if not self.archivo_admins.exists():
            messagebox.showerror("Error", f"No se encontró {self.archivo_admins}")
            return False

        with open(self.archivo_admins, 'r') as f:
            contrasenas = [line.strip().split()[1] for line in f if len(line.split()) > 1]

        # Crear ventana para pedir contraseña
        ventana = tk.Toplevel(self.frame)
        ventana.title("Autenticación")
        ventana.grab_set()  # Bloquea la interacción con la ventana principal

        Label(ventana, text="Ingrese la contraseña de administrador:").grid(row=0, column=0, padx=10, pady=10)
        entry = Entry(ventana, show="*")
        entry.grid(row=0, column=1, padx=10, pady=10)

        validacion_exitosa = tk.BooleanVar(value=False)

        def validar():
            if entry.get() in contrasenas:
                validacion_exitosa.set(True)
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")

        Button(ventana, text="Validar", command=validar).grid(row=1, column=0, columnspan=2, pady=10)
        ventana.wait_window()  # Espera a que se cierre la ventana
        return validacion_exitosa.get()

    def guardar_cambios(self):
        """Guarda los cambios en el archivo de artículos."""
        with open(self.archivo_articulos, 'w') as f:
            for datos in self.productos.values():
                f.write(" ".join(datos["linea"]) + "\n")

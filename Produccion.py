import tkinter as tk
from tkinter import messagebox, Radiobutton, Label, Entry, Button
from pathlib import Path


class Produccion:
    def __init__(self, frame, umbral_file, pe_file, cosecha_file, recetas_file, ma_file):
        self.frame = frame
        self.umbral_file = Path(umbral_file)
        self.pe_file = Path(pe_file)
        self.cosecha_file = Path(cosecha_file)
        self.recetas_file = Path(recetas_file)
        self.ma_file = Path(ma_file)
        self.umbral_data = {}
        self.pe_data = {}
        self.cosecha_data = {}
        self.recetas_data = {}
        self.ma_data = {}
        self.alerts = []

        self.load_files()
        self.check_umbrales()
        if not self.alerts:
            self.create_interface()

    def load_files(self):
        """Carga los archivos necesarios en estructuras de datos."""
        # Leer Umbral
        if self.umbral_file.exists():
            with open(self.umbral_file, 'r') as f:
                for line in f:
                    try:
                        codigo, numero = line.strip().split()
                        self.umbral_data[codigo] = float(numero)
                    except ValueError:
                        messagebox.showerror("Error", f"Formato incorrecto en Umbral: {line.strip()}")

        # Leer PE
        with open(self.pe_file, 'r') as f:
            for line in f:
                try:
                    parts = line.strip().split()
                    codigo, numero = parts[0], float(parts[-1])
                    self.pe_data[codigo] = numero
                except ValueError:
                    messagebox.showerror("Error", f"Formato incorrecto en PE: {line.strip()}")

        # Leer Cosecha
        with open(self.cosecha_file, 'r') as f:
            for line in f:
                try:
                    parts = line.strip().split()
                    codigo, numero = parts[0], float(parts[-1])
                    self.cosecha_data[codigo] = numero
                except ValueError:
                    messagebox.showerror("Error", f"Formato incorrecto en Cosecha: {line.strip()}")

        # Leer Recetas
        with open(self.recetas_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    codigo = parts[0]
                    descripcion = parts[1]
                    ingredientes = parts[2:]
                    self.recetas_data[codigo] = {"descripcion": descripcion, "ingredientes": ingredientes}

        # Leer M_A
        with open(self.ma_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    codigo = parts[0]
                    descripcion = parts[1]
                    cantidad = float(parts[-3])  # Usamos la posición -3 como cantidad a actualizar
                    self.ma_data[codigo] = {"descripcion": descripcion, "cantidad": cantidad, "linea": parts}

    def guardar_cambios(self):
        """Guarda los cambios realizados en los archivos PE.txt, Cosecha.txt y M_A.txt."""
        # Guardar PE
        with open(self.pe_file, 'w') as f:
            for codigo, cantidad in self.pe_data.items():
                f.write(f"{codigo} {cantidad}\n")

        # Guardar Cosecha
        with open(self.cosecha_file, 'w') as f:
            for codigo, cantidad in self.cosecha_data.items():
                f.write(f"{codigo} {cantidad}\n")

        # Guardar M_A
        with open(self.ma_file, 'w') as f:
            for codigo, data in self.ma_data.items():
                f.write(" ".join(data["linea"]) + "\n")

    def check_umbrales(self):
        """Valida los umbrales en PE y Cosecha y genera alertas si es necesario."""
        for codigo, umbral in self.umbral_data.items():
            inventario_pe = self.pe_data.get(codigo, 0.0)
            inventario_cosecha = self.cosecha_data.get(codigo, 0.0)
            total_inventario = inventario_pe + inventario_cosecha

            if total_inventario < umbral:
                alerta = (
                    f"Alerta: {codigo} - Inventario total bajo el umbral "
                    f"(Umbral: {umbral}, Total: {total_inventario})."
                )
                self.alerts.append(alerta)
                messagebox.showwarning("Alerta de Umbral", alerta)

    def create_interface(self):
        """Crea la interfaz con Radiobuttons y habilita solo el Entry asociado al seleccionado."""
        self.selected_product = tk.StringVar()  # Variable para rastrear el radiobutton seleccionado
        self.entry_widgets = {}
        self.validate_buttons = {}

        row = 0
        for codigo, data in self.ma_data.items():
            rad_button = Radiobutton(
                self.frame, 
                text=data["descripcion"], 
                value=codigo, 
                variable=self.selected_product, 
                indicatoron=1, 
                command=self.update_entries
            )
            rad_button.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            Label(self.frame, text=f"{codigo}: {data['descripcion']}").grid(row=row, column=1, padx=5, pady=5, sticky="w")

            entry = Entry(self.frame, state='disabled')
            entry.grid(row=row, column=2, padx=5, pady=5)
            self.entry_widgets[codigo] = entry

            validate_button = Button(
                self.frame, 
                text="Validar", 
                state='disabled', 
                command=lambda c=codigo, e=entry: self.producir(c, e)
            )
            validate_button.grid(row=row, column=3, padx=5, pady=5)
            self.validate_buttons[codigo] = validate_button

            row += 1

    def update_entries(self):
        """Habilita el Entry y el botón 'Validar' asociado al Radiobutton seleccionado."""
        selected_code = self.selected_product.get()
        for codigo, entry in self.entry_widgets.items():
            if codigo == selected_code:
                entry.config(state='normal')
                self.validate_buttons[codigo].config(state='normal')
            else:
                entry.config(state='disabled')
                self.validate_buttons[codigo].config(state='disabled')

    def producir(self, codigo_producto, entry_widget):
        """Valida y procesa la producción del producto seleccionado."""
        try:
            cantidad = float(entry_widget.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "Por favor, ingrese una cantidad mayor a 0.")
                return

            # Validar y descontar ingredientes
            if self.validar_receta(codigo_producto, cantidad):
                # Sumar la cantidad producida al inventario de M_A (posición -3)
                if codigo_producto in self.ma_data:
                    # Actualizar la cantidad en la posición -3
                    self.ma_data[codigo_producto]["cantidad"] += cantidad
                    self.ma_data[codigo_producto]["linea"][-3] = str(self.ma_data[codigo_producto]["cantidad"])
                    
                    # Guardar los cambios en los archivos
                    self.guardar_cambios()
                    
                    messagebox.showinfo(
                        "Producción",
                        f"Producto {codigo_producto} producido con éxito.\nCantidad: {cantidad}\n"
                        f"Nuevo inventario: {self.ma_data[codigo_producto]['cantidad']}"
                    )
                else:
                    messagebox.showerror("Error", f"Producto {codigo_producto} no encontrado en M_A.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido.")


    def validar_receta(self, codigo_producto, cantidad):
        """Valida si se puede producir la cantidad de un producto basado en las recetas."""
        if codigo_producto not in self.recetas_data:
            messagebox.showerror("Error", f"El producto {codigo_producto} no tiene receta registrada.")
            return False

        receta = self.recetas_data[codigo_producto]
        ingredientes_insuficientes = []

        # Validar cada ingrediente
        for i in range(0, len(receta["ingredientes"]), 2):
            ing_codigo = receta["ingredientes"][i]
            ing_cantidad = float(receta["ingredientes"][i + 1]) * cantidad  # Cantidad total requerida

            disponible_pe = self.pe_data.get(ing_codigo, 0)
            disponible_cosecha = self.cosecha_data.get(ing_codigo, 0)
            total_disponible = disponible_pe + disponible_cosecha

            if ing_cantidad > total_disponible:
                ingredientes_insuficientes.append((ing_codigo, ing_cantidad, total_disponible))

        if ingredientes_insuficientes:
            # Si no hay suficiente inventario de un ingrediente, muestra el error
            for ing_codigo, requerido, disponible in ingredientes_insuficientes:
                messagebox.showerror(
                    "Error",
                    f"Insumo insuficiente para {ing_codigo}. Requerido: {requerido}, Disponible: {disponible}."
                )
            return False

        # Si la receta es válida, actualizamos los inventarios
        for i in range(0, len(receta["ingredientes"]), 2):
            ing_codigo = receta["ingredientes"][i]
            ing_cantidad = float(receta["ingredientes"][i + 1]) * cantidad  # Cantidad total requerida

            # Descontar primero de PE, luego de Cosecha si es necesario
            if ing_codigo in self.pe_data:
                if self.pe_data[ing_codigo] >= ing_cantidad:
                    self.pe_data[ing_codigo] -= ing_cantidad  # Descontar todo de PE
                    ing_cantidad = 0
                else:
                    ing_cantidad -= self.pe_data[ing_codigo]
                    self.pe_data[ing_codigo] = 0  # Restar todo lo disponible en PE

            if ing_codigo in self.cosecha_data and ing_cantidad > 0:
                if self.cosecha_data[ing_codigo] >= ing_cantidad:
                    self.cosecha_data[ing_codigo] -= ing_cantidad  # Descontar de Cosecha
                else:
                    # Si no hay suficiente en Cosecha, muestra error (esto no debería ocurrir si la validación inicial es correcta)
                    messagebox.showerror("Error", f"No hay suficiente inventario para {ing_codigo} en Cosecha.")
                    return False

        return True

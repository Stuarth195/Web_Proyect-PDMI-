import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import re
import shutil
from datetime import datetime, timedelta
import os


class ProductManager:
    def __init__(self, parent, file_path, admins_path):
        self.parent = parent
        self.file_path = file_path
        self.admins_path = admins_path
        self.selected_product = tk.StringVar(value="")  # Para rastrear la selección

        # Cargar productos y crear la interfaz
        self.products = self.load_products()
        self.create_interface()

    def load_products(self):
        """Carga los productos desde el archivo."""
        try:
            with open(self.file_path, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {self.file_path}.")
            return []

    def load_admins(self):
        """Carga los códigos de administrador y sus contraseñas."""
        try:
            with open(self.admins_path, 'r') as file:
                return [line.strip().split() for line in file.readlines()]
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {self.admins_path}.")
            return []

    def create_interface(self):
        """Crea la interfaz de botones de selección y eliminar."""
        # Crear botones de selección con grid
        for i, product in enumerate(self.products):
            elements = product.split()
            if len(elements) < 2:
                continue  # Ignorar líneas mal formateadas

            code_and_name = f"{elements[0]} {elements[1]}"  # Primeros dos elementos
            tk.Radiobutton(
                self.parent,
                text=code_and_name,
                variable=self.selected_product,
                value=elements[0]  # Solo el código se almacena como valor
            ).grid(row=i, column=0, sticky="w", padx=10, pady=5)

        # Botón de eliminar
        tk.Button(self.parent, text="Eliminar", command=self.delete_product).grid(
            row=len(self.products), column=0, pady=20
        )

    def validate_admin(self):
        """Pide un código de administrador y lo valida."""
        admins = self.load_admins()
        if not admins:
            return False

        admin_codes = [admin[1] for admin in admins]  # Tomar solo las contraseñas
        admin_code = simpledialog.askstring("Validación", "Ingrese código de administrador:")

        if admin_code in admin_codes:
            return True
        else:
            messagebox.showerror("Error", "Código de administrador no válido.")
            return False

    def delete_product(self):
        """Elimina el producto seleccionado tras validar al administrador."""
        selected = self.selected_product.get()

        if not selected:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para eliminar.")
            return

        if not self.validate_admin():
            return

        # Eliminar el producto del archivo
        new_products = [line for line in self.products if not line.startswith(selected)]

        try:
            with open(self.file_path, 'w') as file:
                file.write("\n".join(new_products) + "\n")

            # Actualizar la interfaz
            self.products = new_products
            self.refresh_interface()

            messagebox.showinfo("Éxito", f"Producto {selected} eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

    def refresh_interface(self):
        """Refresca la interfaz después de eliminar un producto."""
        for widget in self.parent.winfo_children():
            widget.destroy()  # Eliminar todos los widgets actuales
        self.create_interface()

class ProductCreator:
    def __init__(self, ventana_receta, parent, output_path, admins_path, image_folder, batch_file):
        self.ventana_receta = ventana_receta
        self.parent = parent
        self.output_path = output_path
        self.admins_path = admins_path
        self.image_folder = image_folder
        self.batch_file = batch_file
        self.selected_unit = tk.StringVar(value="")
        self.include_image = tk.BooleanVar(value=False)
        self.selected_image_path = None

        # Crear interfaz
        self.create_interface()

    def create_interface(self):
        """Crea los elementos de la interfaz."""
        # Código
        tk.Label(self.parent, text="Código (LLL-###):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.code_entry = tk.Entry(self.parent)
        self.code_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Descripción
        tk.Label(self.parent, text="Descripción:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.description_entry = tk.Entry(self.parent)
        self.description_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Presentación
        tk.Label(self.parent, text="Presentación:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.presentation_entry = tk.Entry(self.parent)
        self.presentation_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Unidad de medida
        tk.Label(self.parent, text="Unidad de Medida:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        units = ["Litros", "Mililitros", "Gramos", "Kilogramos", "Lata", "Botella", "Unidad"]
        for i, unit in enumerate(units):
            tk.Radiobutton(
                self.parent, text=unit, variable=self.selected_unit, value=unit
            ).grid(row=3 + i, column=1, sticky="w", padx=10, pady=2)

        # Precio
        tk.Label(self.parent, text="Precio (entero):").grid(row=10, column=0, sticky="w", padx=10, pady=5)
        self.price_entry = tk.Entry(self.parent)
        self.price_entry.grid(row=10, column=1, sticky="w", padx=10, pady=5)

        # Cantidad (opcional)
        tk.Label(self.parent, text="Cantidad (opcional):").grid(row=11, column=0, sticky="w", padx=10, pady=5)
        self.quantity_entry = tk.Entry(self.parent)
        self.quantity_entry.grid(row=11, column=1, sticky="w", padx=10, pady=5)

        # Agregar Imagen
        tk.Checkbutton(
            self.parent, text="Incluir Imagen", variable=self.include_image, command=self.toggle_image_selection
        ).grid(row=12, column=0, sticky="w", padx=10, pady=5)
        self.image_button = tk.Button(self.parent, text="Seleccionar Imagen", state="disabled", command=self.select_image)
        self.image_button.grid(row=12, column=1, sticky="w", padx=10, pady=5)

        # Botón Crear Producto
        tk.Button(self.parent, text="Crear Producto", command=self.initiate_recipe_creation).grid(row=13, column=0, columnspan=2, pady=10)

    def toggle_image_selection(self):
        """Habilita o deshabilita la selección de imágenes."""
        if self.include_image.get():
            self.image_button.config(state="normal")
        else:
            self.image_button.config(state="disabled")
            self.selected_image_path = None

    def select_image(self):
        """Abre el explorador de archivos para seleccionar una imagen PNG."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[("Archivo PNG", "*.png")]
        )
        if file_path:
            if file_path.lower().endswith(".png"):
                self.selected_image_path = file_path
            else:
                messagebox.showerror("Error", "Formato de imagen inválido. Seleccione un archivo PNG.")
                self.selected_image_path = None

    def validate_inputs(self):
        """Valida los datos ingresados."""
        # Validar código
        code = self.code_entry.get().strip()
        if not re.match(r"^[A-Z]{3}-\d{3}$", code):
            messagebox.showerror("Error", "Formato de código incorrecto. Use el formato LLL-###.")
            return False

        # Verificar si el código ya existe
        if self.is_code_exists(code):
            messagebox.showerror("Error", "Código ya existente.")
            return False

        # Validar descripción (al menos dos letras, sin espacios)
        description = self.description_entry.get().strip()
        if not re.match(r"^(?=.*[A-Za-z])[A-Za-z0-9_()-]+$", description):
            messagebox.showerror("Error", "Descripción inválida. Debe contener al menos dos letras y no puede tener espacios.")
            return False

        # Validar presentación
        presentation = self.presentation_entry.get().strip()
        if not re.match(r"^[A-Za-z_]+$", presentation):
            messagebox.showerror("Error", "Presentación inválida. Use solo letras y guiones bajos.")
            return False

        # Validar unidad de medida
        unit = self.selected_unit.get()
        if not unit:
            messagebox.showerror("Error", "Debe seleccionar una unidad de medida.")
            return False

        # Validar precio
        try:
            price = int(self.price_entry.get().strip())
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número entero positivo.")
            return False

        # Validar cantidad
        quantity = self.quantity_entry.get().strip()
        if quantity:
            try:
                if unit in ["Lata", "Botella", "Unidad"]:
                    quantity = int(quantity)
                else:
                    quantity = float(quantity)
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número válido.")
                return False
        else:
            quantity = 0

        # Validar imagen
        if self.include_image.get():
            if not self.selected_image_path:
                messagebox.showerror("Error", "Error 404: Imagen no encontrada.")
                return False

        self.valid_data = {
            "code": code,
            "description": description,
            "presentation": presentation,
            "unit": unit,
            "price": price,
            "quantity": quantity,
        }
        return True

    def is_code_exists(self, code):
        """Verifica si el código ya existe en el archivo de productos."""
        try:
            with open(self.output_path, 'r') as file:
                for line in file:
                    if line.startswith(code):
                        return True
        except FileNotFoundError:
            pass
        return False

    def save_product(self):
        """Guarda el producto en el archivo y renombra la imagen."""
        data = self.valid_data
        with open(self.output_path, "a") as file:
            file.write("\n") 
            file.write(f"{data['code']} {data['description']} {data['presentation']} {data['quantity']} {data['unit']} {data['price']}\n")

        if self.include_image.get():
            image_name = f"{data['code']}.png"
            shutil.copy(self.selected_image_path, f"{self.image_folder}/{image_name}")

    def initiate_recipe_creation(self):
        """Inicia la creación de una receta después de validar los datos del Producto."""
        if not self.validate_inputs():
            return

        # Una vez validado, abre la ventana de recetas (RecipeManager)
        self.ventana_receta.deiconify()  # Muestra la ventana de recetas
        RecipeManager(
            parent=self.ventana_receta,
            product_file=os.path.join("LISTA PRODUCTO Y RECETAS", "M_A.txt"),
            pe_file=os.path.join("LISTA PRODUCTO Y RECETAS", "PE.txt"),
            cosecha_file=os.path.join("LISTA PRODUCTO Y RECETAS", "COSECHA.txt"),
            recipe_file=os.path.join("LISTA PRODUCTO Y RECETAS", "Receta.txt"),
            code=self.valid_data["code"],
            description=self.valid_data["description"],
            on_recipe_success=self.save_product_and_reset
        )

    def save_product_and_reset(self):
        """Guarda el producto en el archivo y reinicia el formulario."""
        self.save_product()
        self.reset_form()

    def reset_form(self):
        """Limpia los campos del formulario."""
        self.code_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.presentation_entry.delete(0, tk.END)
        self.selected_unit.set("")
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.include_image.set(False)
        self.selected_image_path = None

    def save_batch(self):
        """Guarda el lote inicial del producto en el archivo batch_file."""
        data = self.valid_data
        try:
            batch_identifier = f"{data['code']}_00000000_000"  # Formato del identificador del lote
            expiration_date = (datetime.now() + timedelta(days=15)).strftime("%Y_%m_%d")  # Fecha de vencimiento a 15 días
            with open(self.batch_file, "a") as file:
                file.write("\n") 
                file.write(
                    f" {batch_identifier} {data['code']} {data['description']} {expiration_date} Propio {data['unit']} {data['quantity']}\n"
                )
            print(f"Lote guardado: {batch_identifier}")  # Para depuración
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el lote: {e}")

    def save_product_and_reset(self):
        """Guarda el producto y el lote, y reinicia el formulario."""
        self.save_product()
        self.save_batch()  # Lógica de guardado de lotes
        self.reset_form()

class RecipeManager:
    def __init__(self, parent, product_file, pe_file, cosecha_file, recipe_file, code=None, description=None, on_recipe_success=None):
        self.parent = parent  # Ventana donde se muestran los elementos de RecipeManager
        self.product_file = product_file
        self.pe_file = pe_file
        self.cosecha_file = cosecha_file
        self.recipe_file = recipe_file
        self.code = code
        self.description = description
        self.ingredients = {}
        self.on_recipe_success = on_recipe_success  # Callback para ProductCreator si se guarda la receta con éxito
        self.create_interface()

    def create_interface(self):
        """Crea la interfaz para gestionar recetas."""
        row = 0
        # Mostrar el código del producto o pedirlo si no existe
        if self.code is None:
            tk.Label(self.parent, text="Código del Producto:").grid(row=row, column=0, sticky="w", padx=10, pady=5)
            self.code_entry = tk.Entry(self.parent)
            self.code_entry.grid(row=row, column=1, padx=10, pady=5)
            row += 1
        else:
            tk.Label(self.parent, text=f"Código del Producto: {self.code}").grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)
            row += 1

        # Mostrar ingredientes disponibles
        tk.Label(self.parent, text="Ingredientes:").grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        row += 1

        # Crear un contenedor para los ingredientes
        self.ingredient_frame = tk.Frame(self.parent)
        self.ingredient_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        row += 1

        self.load_ingredients()

        # Botón para guardar la receta
        tk.Button(self.parent, text="Guardar Receta", command=self.save_recipe).grid(row=row, column=0, columnspan=2, pady=10)
        self.parent.focus()

    def load_ingredients(self):
        """Carga los ingredientes desde los archivos PE.txt y COSECHA.txt."""
        def add_ingredient(code, description):
            """Añade un ingrediente a la interfaz con su cantidad."""
            row = len(self.ingredients)  # Determina la fila basada en los ingredientes actuales

            # Checkbox para seleccionar ingrediente
            var = tk.BooleanVar(value=False)
            tk.Checkbutton(
                self.ingredient_frame,
                text=f"{description} ({code})",
                variable=var,
                command=lambda: self.toggle_quantity_entry(var, code)
            ).grid(row=row, column=0, sticky="w", padx=10, pady=2)

            # Entrada para la cantidad del ingrediente
            entry = tk.Entry(self.ingredient_frame, state="disabled")
            entry.grid(row=row, column=1, padx=10, pady=2)

            # Registrar en el diccionario de ingredientes
            self.ingredients[code] = {"var": var, "entry": entry}

        try:
            with open(self.pe_file, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        add_ingredient(parts[0], parts[1])
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {self.pe_file}.")

        try:
            with open(self.cosecha_file, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 4:
                        add_ingredient(parts[0], parts[1])
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {self.cosecha_file}.")

    def toggle_quantity_entry(self, var, code):
        """Activa o desactiva la entrada de cantidad para un ingrediente."""
        entry = self.ingredients[code]["entry"]
        if var.get():
            entry.config(state="normal")
        else:
            entry.delete(0, tk.END)
            entry.config(state="disabled")

    def save_recipe(self):
        """Guarda la receta en el archivo."""
        code = self.code or self.code_entry.get().strip()
        if not code:
            messagebox.showerror("Error", "Debe proporcionar un código de producto.")
            return

        recipe_line = f"{code} {self.description or 'Sin Descripción'}"
        ingredients_data = []

        for ingredient_code, data in self.ingredients.items():
            if data["var"].get():
                quantity = data["entry"].get().strip()
                if not quantity or not self.validate_quantity(quantity):
                    messagebox.showerror("Error", f"Cantidad inválida para {ingredient_code}.")
                    return
                ingredients_data.append(f"{ingredient_code} {quantity}")

        if not ingredients_data:
            messagebox.showerror("Error", "Debe seleccionar al menos un ingrediente.")
            return

        recipe_line += " " + " ".join(ingredients_data)

        try:
            with open(self.recipe_file, 'a') as file:
                file.write("\n") 
                file.write(recipe_line + "\n")
            messagebox.showinfo("Éxito", f"Receta para {code} guardada correctamente.")

            # Llamar al callback si se proporciona
            if self.on_recipe_success:
                self.on_recipe_success()

            # Cerrar ventana tras éxito
            self.parent.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la receta: {e}")

    def validate_quantity(self, quantity):
        """Valida la cantidad ingresada como número flotante o entero."""
        try:
            float(quantity)
            return True
        except ValueError:
            return False


import tkinter as tk
from tkinter import messagebox


class RecipeEditor:
    def __init__(self, parent, recipe_file, pe_file, cosecha_file):
        """
        Inicializa el editor de recetas.
        :param parent: Ventana principal donde se mostrará la interfaz.
        :param recipe_file: Ruta al archivo de recetas.
        :param pe_file: Ruta al archivo de ingredientes PE.
        :param cosecha_file: Ruta al archivo de ingredientes COSECHA.
        """
        self.parent = parent
        self.recipe_file = recipe_file
        self.pe_file = pe_file
        self.cosecha_file = cosecha_file
        self.code = None
        self.description = None
        self.ingredients = {}

        # Crear la interfaz
        self.create_interface()

    def create_interface(self):
        """Crea la interfaz gráfica para editar recetas."""
        row = 0
        # Campo para ingresar el código
        tk.Label(self.parent, text="Código del Producto:").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        self.code_entry = tk.Entry(self.parent)
        self.code_entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Botón para buscar el código en el archivo
        tk.Button(self.parent, text="Buscar Código", command=self.load_recipe).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        # Mostrar ingredientes disponibles
        tk.Label(self.parent, text="Ingredientes:").grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        row += 1

        # Contenedor para los ingredientes
        self.ingredient_frame = tk.Frame(self.parent)
        self.ingredient_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        row += 1

        # Botón para guardar la receta
        tk.Button(self.parent, text="Guardar Receta", command=self.save_recipe).grid(row=row, column=0, columnspan=2, pady=10)

    def load_recipe(self):
        """Busca la receta en el archivo según el código ingresado."""
        code = self.code_entry.get().strip()
        if not code:
            messagebox.showerror("Error", "Debe proporcionar un código.")
            return

        try:
            with open(self.recipe_file, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if parts[0] == code:
                        self.code = parts[0]
                        self.description = parts[1]
                        self.load_ingredients()
                        messagebox.showinfo("Éxito", f"Receta encontrada: {self.description}")
                        return
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {self.recipe_file}.")
            return

        messagebox.showerror("Error", f"No se encontró el código: {code}.")

    def load_ingredients(self):
        """Carga los ingredientes disponibles desde PE.txt y COSECHA.txt."""
        self.ingredients = {}  # Reiniciar los ingredientes actuales
        for widget in self.ingredient_frame.winfo_children():
            widget.destroy()  # Limpiar la interfaz de ingredientes

        def add_ingredient(code, description):
            """Añade un ingrediente a la interfaz."""
            row = len(self.ingredients)  # Determina la fila actual

            # Checkbox para seleccionar el ingrediente
            var = tk.BooleanVar(value=False)
            tk.Checkbutton(
                self.ingredient_frame,
                text=f"{description} ({code})",
                variable=var,
                command=lambda: self.toggle_quantity_entry(var, code)
            ).grid(row=row, column=0, sticky="w", padx=10, pady=2)

            # Campo para la cantidad del ingrediente
            entry = tk.Entry(self.ingredient_frame, state="disabled")
            entry.grid(row=row, column=1, padx=10, pady=2)

            # Registrar en el diccionario de ingredientes
            self.ingredients[code] = {"var": var, "entry": entry}

        # Cargar ingredientes de PE.txt
        self.load_ingredient_file(self.pe_file, add_ingredient)

        # Cargar ingredientes de COSECHA.txt
        self.load_ingredient_file(self.cosecha_file, add_ingredient)

    def load_ingredient_file(self, file_path, add_ingredient_callback):
        """Carga ingredientes desde un archivo dado y los añade con el callback."""
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        add_ingredient_callback(parts[0], parts[1])
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {file_path}.")

    def toggle_quantity_entry(self, var, code):
        """Activa o desactiva el campo de cantidad para un ingrediente."""
        entry = self.ingredients[code]["entry"]
        if var.get():
            entry.config(state="normal")
        else:
            entry.delete(0, tk.END)
            entry.config(state="disabled")

    def save_recipe(self):
        """Guarda la receta en el archivo, sobrescribiendo si ya existe."""
        if not self.code:
            messagebox.showerror("Error", "Debe buscar y cargar un código antes de guardar.")
            return

        # Construir la línea de la receta
        recipe_line = f"{self.code} {self.description}"
        ingredients_data = []

        for ingredient_code, data in self.ingredients.items():
            if data["var"].get():
                quantity = data["entry"].get().strip()
                if not quantity or not self.validate_quantity(quantity):
                    messagebox.showerror("Error", f"Cantidad inválida para {ingredient_code}.")
                    return
                ingredients_data.append(f"{ingredient_code} {quantity}")

        if not ingredients_data:
            messagebox.showerror("Error", "Debe seleccionar al menos un ingrediente.")
            return

        recipe_line += " " + " ".join(ingredients_data)

        # Reemplazar la receta en el archivo
        try:
            self.replace_recipe_line(recipe_line)
            messagebox.showinfo("Éxito", f"Receta para {self.code} guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la receta: {e}")

    def replace_recipe_line(self, new_recipe_line):
        """Reemplaza una línea de receta en el archivo."""
        updated = False
        lines = []

        try:
            with open(self.recipe_file, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            raise Exception(f"El archivo {self.recipe_file} no se encontró.")

        with open(self.recipe_file, 'w') as file:
            for line in lines:
                if line.startswith(self.code):
                    file.write(new_recipe_line)
                    updated = True
                else:
                    file.write(line)
            if not updated:
                raise Exception("Error interno: No se encontró la receta para sobrescribir.")

    def validate_quantity(self, quantity):
        """Valida que la cantidad sea un número válido."""
        try:
            float(quantity)
            return True
        except ValueError:
            return False

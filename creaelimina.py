import tkinter as tk
from tkinter import messagebox, simpledialog

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


# Ejemplo de uso:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestor de Productos")
    app = ProductManager(root, "productos.txt", "admins.txt")
    root.mainloop()

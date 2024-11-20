import tkinter as tk
from botones import Botones  # Importa la clase que creaste

# Función para inicializar y mostrar la ventana con los productos
def mostrar_productos():
    # Crear una instancia de la clase Botones
    botones = Botones()

    # Crear una nueva ventana
    ventana_productos = tk.Toplevel(root)
    ventana_productos.title("Lista de Productos")

    # Llamar al método visualizar_productos
    botones.visualizar_productos(ventana_productos)

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Productos")
root.geometry("400x300")  # Tamaño de la ventana principal

# Etiqueta de bienvenida
label_bienvenida = tk.Label(root, text="Bienvenido al sistema", font=("Arial", 16))
label_bienvenida.pack(pady=20)

# Botón para ver productos
boton_ver_productos = tk.Button(root, text="Ver Productos", command=mostrar_productos, font=("Arial", 12))
boton_ver_productos.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()

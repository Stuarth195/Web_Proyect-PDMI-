import tkinter as tk
import os
from creaelimina import ProductCreator  # Asegúrate de importar correctamente

class Ewstop:
    def __init__(self, parent):
        self.toplevel = tk.Toplevel(parent)
        self.toplevel.withdraw()  # Ocultar inicialmente

    def iniciar_prueba(self,DONDE):
        # Definir rutas exactas según lo indicado
        carpeta = "LISTA PRODUCTO Y RECETAS"
        image_folder = os.path.join("Imagenes", "productos")  # Carpeta para las imágenes
        product_file = os.path.join(carpeta, "M_A.txt")
        pe_file = os.path.join(carpeta, "PE.txt")
        cosecha_file = os.path.join(carpeta, "COSECHA.txt")
        recipe_file = os.path.join(carpeta, "Receta.txt")
        batch_file = os.path.join(carpeta, "Lotes.txt")
        admins_path = os.path.join("admins.txt")

        # Crear carpetas y archivos necesarios
        os.makedirs(carpeta, exist_ok=True)
        os.makedirs(image_folder, exist_ok=True)

        # Crear archivos si no existen
        for file in [product_file, pe_file, cosecha_file, recipe_file, batch_file, admins_path]:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    if file == pe_file:
                        f.write("PE01 Ingrediente1\nPE02 Ingrediente2\n")  # Ejemplo de ingredientes en PE.txt
                    elif file == cosecha_file:
                        f.write("C01 IngredienteC1\nC02 IngredienteC2\n")  # Ejemplo de ingredientes en COSECHA.txt
                    elif file == admins_path:
                        f.write("admin1 1234\nadmin2 5678\n")  # Ejemplo de administradores

        # Crear ventana principal como un Toplevel
        main_window = tk.Toplevel()
        main_window.title("Gestión de Productos")
        main_window.geometry("800x600")

        # Crear instancia de Ewstop
        recipe_window = Ewstop(main_window)

        # Inicializar ProductCreator con las rutas adecuadas
        creator = ProductCreator(
            ventana_receta=recipe_window.toplevel,  # Pasar el Toplevel de la clase Ewstop
            parent=main_window,
            output_path=product_file,
            admins_path=admins_path,
            image_folder=image_folder,
            batch_file=batch_file
        )

        # Ejecutar interfaz principal
        main_window.mainloop()

# Ejecutar prueba
root = tk.Tk()
root.withdraw()  # Ocultar la ventana raíz principal
a = Ewstop(root)
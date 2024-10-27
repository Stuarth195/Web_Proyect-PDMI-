from QuickStart import Data_Base
from tkinter import messagebox

class Instacia_B:
    def __init__(self):
        # Inicializa un objeto de la clase Data_Base para manejar la base de datos
        self.Base_Obj = Data_Base()

    def conecting(self):
        # Conectar a la base de datos
        try:
            self.Base_Obj.conect()
        except Exception as e:
            # Si ocurre un error al conectar, muestra un mensaje de error
            messagebox.showerror("Error", f"No se pudo conectar: {e}")

    def download_A(self, id_archivo, nombre_archivo):
        """Descargar el archivo usando el ID y el nombre del objeto."""
        # Define la ruta de destino para el archivo descargado
        ruta_destino = f"{nombre_archivo}.txt"
        # Llama al método descarga de Base_Obj para descargar el archivo
        self.Base_Obj.descarga(id_archivo, ruta_destino)

    def upload_A(self, ruta_archivo, nombre_archivo):
        """Subir un archivo a Google Drive."""
        # Llama al método subir_archivo de Base_Obj para cargar el archivo
        self.Base_Obj.subir_archivo(ruta_archivo, nombre_archivo)

    def update_A(self, id_archivo, ruta_archivo, nombre_archivo):
        """Actualizar un archivo en Google Drive."""
        try:
            # Llama al método actualizar_archivo para actualizar el archivo en Google Drive
            self.Base_Obj.actualizar_archivo(ruta_archivo, id_archivo, nombre_archivo)  
            # Muestra un mensaje de éxito si el archivo se actualizó correctamente
            messagebox.showinfo("Éxito", f"Archivo '{nombre_archivo}' actualizado exitosamente.")
        except Exception as e:
            # Si ocurre un error durante la actualización, muestra un mensaje de error
            messagebox.showerror("Error", f"No se pudo actualizar el archivo: {e}")

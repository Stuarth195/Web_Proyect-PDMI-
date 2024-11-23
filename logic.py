from QuickStart import Data_Base
from tkinter import messagebox
import os

class Instacia_B:
    def __init__(self):
        self.Base_Obj = Data_Base()

    def conecting(self):
        """Conectar a Google Drive."""
        try:
            self.Base_Obj.conect()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar: {e}")
            raise e

    # ===== Métodos para archivos =====
    def subir_archivo(self, ruta_archivo):
        """Subir un archivo a Google Drive."""
        try:
            nombre_archivo = os.path.basename(ruta_archivo)
            self.Base_Obj.subir_archivo(ruta_archivo, nombre_archivo)
            messagebox.showinfo("Éxito", f"Archivo '{nombre_archivo}' subido exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo subir el archivo: {e}")
            raise e

    def descargar_archivo(self, id_archivo):
        """Descargar un archivo desde Google Drive."""
        try:
            ruta_destino = os.getcwd()
            archivo = self.Base_Obj.drive.CreateFile({'id': id_archivo})
            archivo.FetchMetadata()
            nombre_archivo = archivo['title']
            archivo.GetContentFile(os.path.join(ruta_destino, nombre_archivo))
            messagebox.showinfo("Éxito", f"Archivo '{nombre_archivo}' descargado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar el archivo: {e}")
            raise e

    def actualizar_archivo(self, id_archivo, ruta_archivo):
        """Actualizar un archivo en Google Drive."""
        try:
            if not os.path.exists(ruta_archivo):
                raise FileNotFoundError(f"Archivo no encontrado en '{ruta_archivo}'.")
            self.Base_Obj.actualizar_archivo(ruta_archivo, id_archivo)
            messagebox.showinfo("Éxito", f"Archivo actualizado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el archivo: {e}")
            raise e

    # ===== Métodos para carpetas =====
    def subir_carpeta(self, ruta_carpeta):
        """Subir una carpeta y su contenido a Google Drive."""
        try:
            nombre_carpeta = os.path.basename(ruta_carpeta)
            id_carpeta_drive = self._crear_carpeta(nombre_carpeta, None)  # Crear carpeta en Drive
            self._subir_contenido_carpeta(ruta_carpeta, id_carpeta_drive)
            messagebox.showinfo("Éxito", f"Carpeta '{nombre_carpeta}' subida exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo subir la carpeta: {e}")
            raise e

    def descargar_carpeta(self, id_carpeta):
        """Descargar una carpeta y su contenido desde Google Drive."""
        try:
            ruta_destino = os.getcwd()
            carpeta = self.Base_Obj.drive.CreateFile({'id': id_carpeta})
            carpeta.FetchMetadata()
            nombre_carpeta = carpeta['title']
            ruta_carpeta_local = os.path.join(ruta_destino, nombre_carpeta)
            os.makedirs(ruta_carpeta_local, exist_ok=True)
            self._descargar_contenido_carpeta(id_carpeta, ruta_carpeta_local)
            messagebox.showinfo("Éxito", f"Carpeta '{nombre_carpeta}' descargada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar la carpeta: {e}")
            raise e

    def actualizar_carpeta(self, id_carpeta, ruta_carpeta):
        """Actualizar una carpeta y su contenido en Google Drive."""
        try:
            if not os.path.exists(ruta_carpeta):
                raise FileNotFoundError(f"La carpeta local '{ruta_carpeta}' no existe.")
            self._limpiar_carpeta(id_carpeta)  # Limpiar el contenido de la carpeta en Drive
            self._subir_contenido_carpeta(ruta_carpeta, id_carpeta)  # Subir nuevo contenido
            messagebox.showinfo("Éxito", f"Carpeta actualizada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la carpeta: {e}")
            raise e

    # ===== Métodos auxiliares =====
    def _crear_carpeta(self, nombre_carpeta, id_carpeta_padre):
        """Crear una carpeta en Google Drive."""
        carpeta_drive = self.Base_Obj.drive.CreateFile({
            'title': nombre_carpeta,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{'id': id_carpeta_padre}] if id_carpeta_padre else []
        })
        carpeta_drive.Upload()
        return carpeta_drive['id']

    def _subir_contenido_carpeta(self, ruta_carpeta, id_carpeta_drive):
        """Subir el contenido de una carpeta de forma recursiva."""
        for item in os.listdir(ruta_carpeta):
            ruta_item = os.path.join(ruta_carpeta, item)
            if os.path.isdir(ruta_item):
                id_subcarpeta = self._crear_carpeta(item, id_carpeta_drive)
                self._subir_contenido_carpeta(ruta_item, id_subcarpeta)
            else:
                self.Base_Obj.subir_archivo(ruta_item, item, id_carpeta_drive)

    def _descargar_contenido_carpeta(self, id_carpeta, ruta_destino):
        """Descargar el contenido de una carpeta de forma recursiva."""
        query = f"'{id_carpeta}' in parents and trashed=false"
        contenido = self.Base_Obj.drive.ListFile({'q': query}).GetList()
        for item in contenido:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                nueva_ruta = os.path.join(ruta_destino, item['title'])
                os.makedirs(nueva_ruta, exist_ok=True)
                self._descargar_contenido_carpeta(item['id'], nueva_ruta)
            else:
                ruta_archivo = os.path.join(ruta_destino, item['title'])
                item.GetContentFile(ruta_archivo)

    def _limpiar_carpeta(self, id_carpeta):
        """Eliminar el contenido de una carpeta en Google Drive."""
        query = f"'{id_carpeta}' in parents and trashed=false"
        contenido = self.Base_Obj.drive.ListFile({'q': query}).GetList()
        for item in contenido:
            item.Delete()  # Eliminar cada archivo o subcarpeta dentro de la carpeta

    def subir_por_extension(self, ruta_carpeta, extension, id_carpeta_padre=None):
        """
        Sube todos los archivos con una extensión específica desde una carpeta local a Google Drive.

        :param ruta_carpeta: Ruta local de la carpeta donde buscar los archivos.
        :param extension: Extensión de los archivos a subir (por ejemplo: ".txt", ".png").
        :param id_carpeta_padre: ID de la carpeta en Google Drive donde se subirán los archivos (opcional).
        """
        try:
            # Validar que la carpeta exista
            if not os.path.exists(ruta_carpeta):
                raise FileNotFoundError(f"La carpeta '{ruta_carpeta}' no existe.")

            # Buscar archivos con la extensión especificada
            archivos = [f for f in os.listdir(ruta_carpeta) if f.endswith(extension)]
            if not archivos:
                print(f"No se encontraron archivos con la extensión '{extension}' en '{ruta_carpeta}'.")
                return

            # Subir cada archivo encontrado
            for archivo in archivos:
                ruta_archivo = os.path.join(ruta_carpeta, archivo)
                self.Base_Obj.subir_archivo(ruta_archivo, archivo, id_carpeta_padre)
                print(f"Archivo '{archivo}' subido exitosamente.")

            print(f"Todos los archivos con la extensión '{extension}' se han subido correctamente.")
        except Exception as e:
            print(f"Error al subir archivos con la extensión '{extension}': {e}")
            raise e

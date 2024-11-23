import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Data_Base:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LoadClientConfigFile('client_secret.json')  
        self.authenticate()
        self.drive = GoogleDrive(self.gauth)

    def authenticate(self):
        try:
            if os.path.exists('token.json'):
                self.gauth.LoadCredentialsFile('token.json')
                if self.gauth.credentials is None or self.gauth.access_token_expired:
                    self.gauth.LocalWebserverAuth()
                    self.gauth.SaveCredentialsFile('token.json')
                print("Credenciales cargadas desde token.json.")
            else:
                self.gauth.LocalWebserverAuth()
                self.gauth.SaveCredentialsFile('token.json')
                print("Autenticación exitosa, credenciales guardadas en token.json.")
        except Exception as e:
            print(f"Error durante la autenticación: {e}")

    def conect(self):
        try:
            file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
            for file in file_list:
                print(f'Título: {file["title"]}, ID: {file["id"]}')
        except Exception as e:
            print(f"Error al listar archivos: {e}")

    def descarga(self, id_base, ruta_destino):
        """Descargar un archivo de Google Drive"""
        try:
            file = self.drive.CreateFile({'id': id_base})
            file.GetContentFile(ruta_destino)
            print(f"Archivo '{ruta_destino}' descargado exitosamente.")
        except Exception as e:
            print(f"Error al descargar el archivo: {e}")

    def subir_archivo(self, ruta_archivo, nombre_archivo, id_carpeta_padre=None):
        """Subir un archivo a Google Drive."""
        try:
            archivo_drive = self.drive.CreateFile({
                'title': nombre_archivo,
                'parents': [{'id': id_carpeta_padre}] if id_carpeta_padre else []  # Especificar carpeta destino
            })
            archivo_drive.SetContentFile(ruta_archivo)
            archivo_drive.Upload()
            print(f"Archivo '{nombre_archivo}' subido exitosamente.")
        except Exception as e:
            print(f"Error al subir el archivo: {e}")

    def actualizar_archivo(self, ruta_archivo, file_id):
        try:
            archivo_drive = self.drive.CreateFile({'id': file_id})
            archivo_drive.SetContentFile(ruta_archivo)
            archivo_drive.Upload()
            print(f"Archivo con ID '{file_id}' actualizado exitosamente.")
        except Exception as e:
            print(f"Error al actualizar el archivo: {e}")

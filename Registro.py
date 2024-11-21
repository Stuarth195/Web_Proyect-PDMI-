import os
import tkinter as tk
from tkinter import messagebox
from RevUsuarios import revUsuarios
from TXTReader import LectorTXT
from WriterEnDocumento import Writer
from Pantallas import Pantalla_add


class Emergente:
    def __init__(self, vtkinter = None,canva = None, xMargen= None, yMargen= None, notebook= None):
        self.vtkinter = vtkinter
        self.canva =canva
        self.xMargen = xMargen
        self.yMargen = yMargen
        self.notebook = notebook
        self.register = None
        self.win = 0  # 0 = sin registro, 1 = logeado
        self.username = "User0000"
        self.Etiqueta_Logado = tk.Label(self.vtkinter, text="User0000", font=("Helvetica", 10, "bold"), bg="white")
        self.Etiqueta_Logado.place(x=self.xMargen * 48, y=self.yMargen * 1.8)

        self.Lector = LectorTXT()
        self.MatrizUsuarios = self.Lector.leerTxtFile("Usuarios.txt")
        self.Revisor = revUsuarios(self.MatrizUsuarios)
        self.Escritor = Writer()

        self.Math_admin = self.Lector.leerTxtFile("admins.txt")
        self.Revisor_ad = revUsuarios(self.Math_admin)
        self.archivo_compras_path = os.path.join("RegistroCompras.txt")

        
        # Cargar las imágenes de los botones
        self.boton_login_img = tk.PhotoImage(file=os.path.join("Imagenes", "boton_login.png"))
        self.boton_singin_img = tk.PhotoImage(file=os.path.join("Imagenes", "boton_singin.png"))
        self.boton_entrar_img = tk.PhotoImage(file=os.path.join("Imagenes", "boton_entrar.png"))
        self.boton_atras_img = tk.PhotoImage(file=os.path.join("Imagenes", "boton_atras.png"))
        self.boton_registrarse_img = tk.PhotoImage(file=os.path.join("Imagenes", "boton_register.png"))
        self.boton_logout_img = tk.PhotoImage(file=os.path.join("Imagenes", "boton_logout.png"))

    def registro(self):
        self.MatrizUsuarios = self.Lector.leerTxtFile("Usuarios.txt")
        if self.win == 0:
            if self.register:
                self.register.destroy()
            self.register = tk.Toplevel(self.vtkinter, width=500, height=500)
            self.register.title("Registro")
            self.register.resizable(False, False)
            self.register.focus()

            boton_login = tk.Button(self.register, image=self.boton_login_img, command=self.mostrar_login)
            boton_login.place(x=40, y=300)

            boton_singin = tk.Button(self.register, image=self.boton_singin_img, command=self.mostrar_signin)
            boton_singin.place(x=290, y=300)
        elif self.win == 1:
            self.mostrar_menu_logout()
    def mostrar_login(self):
        if self.register:
            for widget in self.register.winfo_children():
                widget.destroy()

            # Etiqueta de usuario
            tk.Label(self.register, text="Usuario:", font=("Arial", 14)).place(x=20, y=120)
            username_entry = tk.Entry(self.register, font=("Arial", 14), width=20)
            username_entry.place(x=150, y=120)

            # Etiqueta de contraseña
            tk.Label(self.register, text="Contraseña:", font=("Arial", 14)).place(x=20, y=180)
            password_entry = tk.Entry(self.register, font=("Arial", 14), width=20, show="*")
            password_entry.place(x=150, y=180)

            # Botón de entrar
            tk.Button(self.register, image=self.boton_entrar_img,
                    command=lambda: self.Login(username_entry.get(), password_entry.get())).place(x=40, y=300)

            # Botón de atrás
            tk.Button(self.register, image=self.boton_atras_img, command=self.registro).place(x=290, y=300)
        tk.Button(self.register, image=self.boton_atras_img, command=self.registro).place(x=290, y=300)
    
    def mostrar_signin(self):
        if self.register:
            for widget in self.register.winfo_children():
                widget.destroy()

            # Etiqueta de usuario
            tk.Label(self.register, text="Usuario:", font=("Arial", 14)).place(x=20, y=120)
            username_entry = tk.Entry(self.register, font=("Arial", 14), width=20)
            username_entry.place(x=150, y=120)

            # Etiqueta de contraseña
            tk.Label(self.register, text="Contraseña:", font=("Arial", 14)).place(x=20, y=160)
            password_entry = tk.Entry(self.register, font=("Arial", 14), width=20, show="*")
            password_entry.place(x=150, y=160)

            # Etiqueta de confirmar contraseña (ahora en una nueva línea)
            tk.Label(self.register, text="Confirmar", font=("Arial", 14)).place(x=20, y=195)
            tk.Label(self.register, text="Contraseña:", font=("Arial", 14)).place(x=20, y=215)
            confirm_entry = tk.Entry(self.register, font=("Arial", 14), width=20, show="*")
            confirm_entry.place(x=150, y=220)

            # Botón de registrarse
            tk.Button(self.register, image=self.boton_registrarse_img,
                    command=lambda: self.SignIn(username_entry.get(), password_entry.get(), confirm_entry.get())).place(x=100, y=280)

            # Botón de atrás
            tk.Button(self.register, image=self.boton_atras_img, command=self.registro).place(x=290, y=280)

    def Login(self, username, password):

        self.Escritor.limpiartxt("Carrito.txt")

        if self.Revisor_ad.RevisarUsuarioExistente(username, password)==True:
            self.win = 1
            self.username = username
            self.register.destroy()
            self.register = None
            self.mostrar_menu_logout()
            self.Etiqueta_Logado.config(text=username)
            self.admin_win = Pantalla_add(self.vtkinter, self.notebook, self.archivo_compras_path, None,None,self.username)
            self.admin_win.pantalla_oculta("pantalla")
            self.admin_win.crear_boton_historial_usuario(self.canva,self.xMargen*47, self.yMargen*6)
            
        elif self.Revisor.RevisarUsuarioExistente(username, password)==True:
            self.win = 1
            self.username = username
            self.admin_win = Pantalla_add(self.vtkinter, self.notebook, self.archivo_compras_path, None,None,self.username)
            self.register.destroy()
            self.register = None
            self.mostrar_menu_logout()
            self.Etiqueta_Logado.config(text=username)
            self.admin_win.crear_boton_historial_usuario(self.canva,self.xMargen*47, self.yMargen*6)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def SignIn(self, username, password, confirm_password):
        self.Escritor.limpiartxt("Carrito.txt")
        if password == confirm_password:
            self.win = 1
            self.username = username
            self.admin_win = Pantalla_add(self.vtkinter, self.notebook, self.archivo_compras_path, None,None,self.username)
            self.register.destroy()
            self.register = None
            self.mostrar_menu_logout()
            self.Escritor.write("Usuarios.txt", username + " " + password + "\n")
            self.Escritor.write("RegistroCompras.txt", f"{username}")
            self.admin_win.crear_boton_historial_usuario(self.canva,self.xMargen*47, self.yMargen*6)
            self.Etiqueta_Logado.config(text=username)
        else:
            messagebox.showerror("Error", "Las contraseñas no coinciden")

    def mostrar_menu_logout(self):
        logout_menu = tk.Toplevel(self.vtkinter, width=300, height=300)
        logout_menu.title("Menú de Log Out")
        logout_menu.resizable(False, False)

        tk.Label(logout_menu, text=f"Usuario: {self.username}").place(x=100, y=50)

        boton_logout = tk.Button(logout_menu, image=self.boton_logout_img, command=lambda: self.logout(logout_menu))
        boton_logout.place(x=75, y=100)

    def logout(self, ventana):
        self.Etiqueta_Logado.config(text="User0000")
        self.username = "User0000"
        ventana.destroy()
        self.win = 0
        self.registro()
        self.admin_win.destruir_boton_usuario()
        try:
            self.admin_win.reiniciar_pantalla()
        except:
            print("No se pudo reiniciar")

    def getUsername(self):
        return self.username
    



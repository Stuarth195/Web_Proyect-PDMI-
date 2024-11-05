import tkinter as tk
from tkinter import messagebox
from RevUsuarios import revUsuarios
from TXTReader import LectorTXT
from WriterEnDocumento import Writer
from Pantallas import Pantalla_add


class Emergente:
    def __init__(self, vtkinter, xMargen, yMargen, notebook):
        self.vtkinter = vtkinter
        self.xMargen = xMargen
        self.yMargen = yMargen
        self.notebook = notebook
        self.register = None
        self.win = 0  # 0 = sin registro, 1 = logeado
        self.username = None
        self.Etiqueta_Logado = tk.Label(self.vtkinter, text="")
        self.Etiqueta_Logado.place(x=self.xMargen * 48, y=self.yMargen * 1.5)

    
        self.Lector = LectorTXT()
        self.MatrizUsuarios = self.Lector.leerTxtFile("Usuarios.txt")
        self.Revisor = revUsuarios(self.MatrizUsuarios)
        self.Escritor = Writer()

        self.Math_admin=self.Lector.leerTxtFile("admins.txt")
        self.Revisor_ad = revUsuarios(self.Math_admin)


    def registro(self):
        # Muestra la ventana de registro con opciones para Log In y Sign In.
        if self.win == 0:  # Solo muestra la ventana si no está logeado
            if self.register:
                self.register.destroy()
            self.register = tk.Toplevel(self.vtkinter, width=500, height=500)
            self.register.title("Registro")
            self.register.resizable(False, False)  # Evita el redimensionamiento
            self.register.focus()

            # Botón de Log In
            boton_login = tk.Button(self.register, text="Log In", command=self.mostrar_login)
            boton_login.place(x=50, y=50)

            # Botón de Sign In
            boton_singin = tk.Button(self.register, text="Sign In", command=self.mostrar_signin)
            boton_singin.place(x=150, y=50)
        elif self.win == 1:
            # Si el usuario está logeado, muestra el menú de Log Out directamente
            self.mostrar_menu_logout()

    def mostrar_login(self):
        # Despliega formulario para ingresar nombre de usuario y contraseña para Log In.
        if self.register:
            for widget in self.register.winfo_children():
                widget.destroy()

            tk.Label(self.register, text="Usuario:").place(x=50, y=50)
            username_entry = tk.Entry(self.register)
            username_entry.place(x=150, y=50)

            tk.Label(self.register, text="Contraseña:").place(x=50, y=100)
            password_entry = tk.Entry(self.register, show="*")
            password_entry.place(x=150, y=100)

            tk.Button(self.register, text="Entrar",
                      command=lambda: self.Login(username_entry.get(), password_entry.get())).place(x=100, y=150)
            tk.Button(self.register, text="Atrás", command=self.registro).place(x=200, y=150)

    def mostrar_signin(self):
        # Despliega formulario para ingresar nombre de usuario, contraseña y confirmación para Sign In.
        if self.register:
            for widget in self.register.winfo_children():
                widget.destroy()

            tk.Label(self.register, text="Usuario:").place(x=50, y=50)
            username_entry = tk.Entry(self.register)
            username_entry.place(x=150, y=50)

            tk.Label(self.register, text="Contraseña:").place(x=50, y=100)
            password_entry = tk.Entry(self.register, show="*")
            password_entry.place(x=150, y=100)

            tk.Label(self.register, text="Confirmar Contraseña:").place(x=50, y=150)
            confirm_entry = tk.Entry(self.register, show="*")
            confirm_entry.place(x=150, y=150)

            tk.Button(self.register, text="Registrarse",
                      command=lambda: self.SignIn(username_entry.get(), password_entry.get(),
                                                  confirm_entry.get())).place(x=100, y=200)
            tk.Button(self.register, text="Atrás", command=self.registro).place(x=200, y=200)

    def Login(self, username, password):
        if self.Revisor_ad.RevisarUsuarioExistente(username, password)==True:
            self.win = 1
            self.username = username
            self.register.destroy()
            self.register = None
            self.mostrar_menu_logout()
            self.Etiqueta_Logado.config(text=username)
            self.admin_win =Pantalla_add(self.vtkinter,self.notebook,None , None)
            self.admin_win.pantalla_oculta("pantalla")
            
        # Proceso de Log In.
        elif self.Revisor.RevisarUsuarioExistente(username, password)==True:
            self.win = 1
            self.username = self.username
            self.register.destroy()
            self.register = None
            self.mostrar_menu_logout()
            self.Etiqueta_Logado.config(text=username)

        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def SignIn(self, username, password, confirm_password):
        # Proceso de Sign In.
        if password == confirm_password:
            self.win = 1
            self.username = username
            self.register.destroy()
            self.register = None
            self.mostrar_menu_logout()
            self.Escritor.write("Usuarios.txt", username + " " + password + "\n")
            self.Etiqueta_Logado.config(text=username)

        else:
            messagebox.showerror("Error", "Las contraseñas no coinciden")

    def mostrar_menu_logout(self):
        # Muestra el menú de Log Out.
        logout_menu = tk.Toplevel(self.vtkinter, width=300, height=300)
        logout_menu.title("Menú de Log Out")
        logout_menu.resizable(False, False)  # Evita el redimensionamiento

        tk.Label(logout_menu, text=f"Usuario: {self.username}").place(x=100, y=50)

        # Botón para hacer Log Out
        boton_logout = tk.Button(logout_menu, text="Log Out", command=lambda: self.logout(logout_menu))
        boton_logout.place(x=100, y=100)

    def logout(self, ventana):
        # Cierra sesión, destruye la ventana actual y permite volver a registrarse.
        ventana.destroy()
        self.win = 0  # Cambia el estado a sin registro
        self.registro()
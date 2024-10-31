class revUsuarios:

    def __init__(self, listaUsuarios):
        self.listaUsuarios = listaUsuarios
    def RevisarUsuarioExistente(self,nombreUsuario, contrasenaUsuario):
        Exite = False
        for Usuario in self.listaUsuarios:
            if Usuario[0] == nombreUsuario and Usuario[1] == contrasenaUsuario:
                Exite = True
        return Exite

class LectorTXT:

    def leerTxtFile(self, txtFilePath):
        Usuario = ""
        Password = ""
        US = True
        with open(txtFilePath, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                for caracter in linea:
                    if caracter == " ":
                        US = False
                    if US == True:
                        Usuario = Usuario + caracter
                    else:
                        Password = Password + caracter
        print(Password, Usuario)

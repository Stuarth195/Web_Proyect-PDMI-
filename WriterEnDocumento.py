
class Writer():
    def write(self, Filepath, mensaje):
        with open(Filepath, 'a', encoding='utf-8') as archivo:
            archivo.write("\n" + mensaje)
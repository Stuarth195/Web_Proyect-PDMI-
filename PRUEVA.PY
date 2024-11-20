from botones import Botones  # Importamos la clase desde el archivo

# Crear una instancia de la clase Botones
botones = Botones()

# Verificar un código específico
codigo_a_verificar = "CHP-000"
resultado = botones.verifica_codigo(codigo_a_verificar)

# Imprimir el resultado
if resultado:
    print(f"El código '{codigo_a_verificar}' fue encontrado en los archivos.")
else:
    print(f"El código '{codigo_a_verificar}' no existe en los archivos.")

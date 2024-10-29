from PIL import Image
class AJS:
    def __init__(self, Ancho_ventana, Alto_ventana):
        self.Ancho_ventana = Ancho_ventana
        self.Alto_ventana = Alto_ventana


    def ajustarIMG(self, imagen, dimensiones):
        ancho_original, alto_original = imagen.size

        # Calcular la relación de aspecto
        relacion_aspecto = ancho_original / alto_original

        # Calcular el nuevo tamaño manteniendo la proporción
        nuevo_ancho = int(self.Ancho_ventana * dimensiones)  # 50% del ancho de la pantalla
        nuevo_alto = int(nuevo_ancho / relacion_aspecto)

        # Redimensionar la imagen
        imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
        return imagen_redimensionada

from pathlib import Path
import random


class CamaraSimulada:

    def __init__(self):

        # Carpeta principal del catálogo
        self.carpeta = Path("catalogo_camara")

        # Formatos de imagen permitidos
        self.extensiones = {
            ".jpg",
            ".jpeg",
            ".png"
        }


    def capturar_imagen(self):

        # Buscar imágenes dentro de todas las subcarpetas
        imagenes = [
            archivo
            for archivo in self.carpeta.rglob("*")
            if archivo.is_file()
            and archivo.suffix.lower() in self.extensiones
        ]

        if not imagenes:
            return None

        # Seleccionar una imagen aleatoriamente
        imagen = random.choice(imagenes)

        return imagen
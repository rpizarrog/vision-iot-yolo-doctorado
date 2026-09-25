from ultralytics import YOLO


class DetectorVision:

    def __init__(self, modelo="yolo11s.pt"):

        # Cargar el modelo YOLO preentrenado
        self.modelo = YOLO(modelo)


    def detectar(self, imagen):

        # Realizar la detección
        resultados = self.modelo(str(imagen))

        detecciones = []

        # Recorrer los resultados encontrados por YOLO
        for resultado in resultados:

            for caja in resultado.boxes:

                clase = int(caja.cls[0])

                confianza = float(caja.conf[0])

                objeto = self.modelo.names[clase]

                detecciones.append({
                    "objeto": objeto,
                    "confianza": confianza
                })

        return detecciones
import paho.mqtt.client as mqtt
import json
from CCamaraSimulada import CamaraSimulada
from CDetectorVision import DetectorVision
import base64


class ReceptorMQTT:

    def __init__(self):

        self.broker = "test.mosquitto.org"
        self.puerto = 1883

        self.topico = "doctorado/ruben/iot/deteccion"
        self.topico_vision = "doctorado/ruben/iot/vision"

        # Guarda el estado anterior del sensor PIR
        self.movimiento_anterior = 0

        # Crear cámara simulada
        self.camara = CamaraSimulada()

        # Crear detector de visión con YOLO11s
        self.detector = DetectorVision(
            modelo="yolo11s.pt"
        )

        self.cliente = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )



    def f_conectar(self):

        self.cliente.on_connect = self.f_al_conectar
        self.cliente.on_message = self.f_al_recibir_mensaje

        print("Conectando con MQTT...")

        self.cliente.connect(
            self.broker,
            self.puerto,
            60
        )


    def f_al_conectar(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties
    ):

        print("Conectado al broker MQTT")

        print(
            "Suscrito a:",
            self.topico
        )

        client.subscribe(
            self.topico
        )


    def f_al_recibir_mensaje(
        self,
        client,
        userdata,
        msg
    ):

        try:

            datos = json.loads(
                msg.payload.decode("utf-8")
            )

            # Obtener estado actual del PIR
            movimiento_actual = int(
                datos.get("movimiento", 0)
            )

            # Detectar solamente la transición 0 -> 1
            if movimiento_actual == 1 and self.movimiento_anterior == 0:

                print("\n************************************")
                print("       MOVIMIENTO DETECTADO")
                print("************************************")
                print(
                    f"PIR: {self.movimiento_anterior} "
                    f"-> {movimiento_actual}"
                )
                print("ACTIVANDO CAMARA SIMULADA...")

                imagen = self.camara.capturar_imagen()

                if imagen is not None:
                    print("Imagen capturada:")
                    print(imagen)
                    print("\nANALIZANDO CON YOLO11s...")

                    detecciones = self.detector.detectar(imagen)

                    if len(detecciones) > 0:

                        print("\n====================================")
                        print("RESULTADO DE VISION ARTIFICIAL")
                        print("====================================")

                        for deteccion in detecciones:

                            objeto = deteccion["objeto"]

                            confianza = (
                                deteccion["confianza"] * 100
                            )

                            print(
                                f"{objeto:15} "
                                f"{confianza:6.2f} %"
                            )

                        with open(imagen, "rb") as archivo:
                            imagen_base64 = base64.b64encode(archivo.read()).decode("utf-8")
                        # ============================================
                        # CREAR MENSAJE DE VISION
                        # ============================================

                        mensaje_vision = {

                            "imagen": imagen.name,
                            "imagen_base64": imagen_base64,
                            "detecciones": detecciones

                        }


                        # Convertir diccionario Python a JSON
                        mensaje_json = json.dumps(
                            mensaje_vision
                        )


                        # ============================================
                        # PUBLICAR RESULTADO POR MQTT
                        # ============================================

                        self.cliente.publish(
                            self.topico_vision,
                            mensaje_json
                        )


                        print("\nResultado de visión publicado por MQTT")

                        print(
                            "Tópico:",
                            self.topico_vision
                        )

                        print(
                            "Mensaje:",
                            mensaje_json
                        )

                    else:

                        print("\nYOLO no detectó objetos.")
                    
                else:
                    print("No se encontró ninguna imagen.")





            # Guardar el estado actual para el siguiente mensaje
            self.movimiento_anterior = movimiento_actual

            print("\n====================================")
            print("MENSAJE RECIBIDO DESDE WOKWI")
            print("====================================")

            print(
                "Temperatura :",
                datos.get("temperatura")
            )

            print(
                "Humedad     :",
                datos.get("humedad")
            )

            print(
                "Distancia   :",
                datos.get("distancia")
            )

            print(
                "Luminosidad :",
                datos.get("luminosidad")
            )

            print(
                "Movimiento  :",
                datos.get("movimiento")
            )

            print(
                "Clasificación:",
                datos.get("clasificacion")
            )

            print(
                "Alarma      :",
                datos.get("alarma")
            )

        except Exception as error:

            print(
                "Error procesando mensaje:",
                error
            )


    def f_escuchar(self):

        self.f_conectar()

        print(
            "\nEsperando mensajes del ESP32..."
        )

        self.cliente.loop_forever()
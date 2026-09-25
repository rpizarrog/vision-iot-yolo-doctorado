from flask import Flask
from threading import Thread
import os

from CReceptorMQTT import ReceptorMQTT


app = Flask(__name__)


@app.route("/")
def inicio():
    return """
    <h1>Sistema IoT Inteligente</h1>
    <h2>Servicio de Visión Artificial</h2>
    <p>YOLO + MQTT funcionando en la nube.</p>
    """


@app.route("/health")
def health():
    return {
        "estado": "activo",
        "servicio": "Vision Artificial YOLO",
        "mqtt": "escuchando"
    }


def iniciar_mqtt():
    receptor = ReceptorMQTT()
    receptor.f_escuchar()


if __name__ == "__main__":

    # MQTT se ejecuta en un hilo independiente
    hilo_mqtt = Thread(
        target=iniciar_mqtt,
        daemon=True
    )

    hilo_mqtt.start()

    # Puerto proporcionado por Render
    puerto = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=puerto
    )
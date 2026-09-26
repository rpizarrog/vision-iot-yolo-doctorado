from flask import Flask
from threading import Thread
import os
import traceback

from CReceptorMQTT import ReceptorMQTT


# ============================================================
# APLICACIÓN FLASK
# ============================================================

app = Flask(__name__)


@app.route("/")
def inicio():
    return """
    <h1>Sistema IoT Inteligente</h1>
    <h2>Servicio de Visión Artificial</h2>
    <p>Servidor Flask funcionando correctamente en Render.</p>
    <p>Receptor MQTT ejecutándose en segundo plano.</p>
    """


@app.route("/health")
def health():
    return {
        "estado": "OK",
        "servicio": "vision-iot-yolo-doctorado"
    }


# ============================================================
# RECEPTOR MQTT
# ============================================================

def iniciar_mqtt():

    print(">>> Iniciando hilo MQTT...", flush=True)

    try:

        receptor = ReceptorMQTT()

        print(
            ">>> Receptor MQTT creado. Iniciando escucha...",
            flush=True
        )

        receptor.f_escuchar()

    except Exception as error:

        print(
            f">>> ERROR EN MQTT: {error}",
            flush=True
        )

        traceback.print_exc()


# ============================================================
# INICIO DE LA APLICACIÓN
# ============================================================

if __name__ == "__main__":

    print(">>> Iniciando servicio Flask + MQTT...", flush=True)

    # MQTT se ejecuta en un hilo independiente
    hilo_mqtt = Thread(
        target=iniciar_mqtt,
        daemon=True
    )

    hilo_mqtt.start()

    print(">>> HILO MQTT INICIADO", flush=True)

    # Puerto asignado automáticamente por Render
    puerto = int(
        os.environ.get("PORT", 5000)
    )

    print(
        f">>> Iniciando Flask en puerto {puerto}",
        flush=True
    )

    app.run(
        host="0.0.0.0",
        port=puerto,
        debug=False,
        use_reloader=False
    )
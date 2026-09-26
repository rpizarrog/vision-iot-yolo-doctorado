from flask import Flask
from threading import Thread
import paho.mqtt.client as mqtt
import os
import json
import traceback


# ============================================================
# CONFIGURACIÓN
# ============================================================

BROKER = "test.mosquitto.org"
PUERTO_MQTT = 1883
TOPICO = "doctorado/ruben/iot/deteccion"

app = Flask(__name__)


# ============================================================
# FLASK
# ============================================================

@app.route("/")
def inicio():
    return """
    <h1>Sistema IoT Inteligente</h1>
    <h2>Prueba Flask + MQTT en Render</h2>
    <p>Servidor Flask funcionando.</p>
    <p>Receptor MQTT ejecutándose en segundo plano.</p>
    """


@app.route("/health")
def health():
    return {
        "estado": "OK",
        "servicio": "vision-iot-yolo-doctorado",
        "mqtt": "configurado"
    }


# ============================================================
# MQTT
# ============================================================

def al_conectar(client, userdata, flags, reason_code, properties):

    print(
        f">>> MQTT CONECTADO. Código: {reason_code}",
        flush=True
    )

    client.subscribe(TOPICO)

    print(
        f">>> SUSCRITO AL TÓPICO: {TOPICO}",
        flush=True
    )


def al_recibir_mensaje(client, userdata, msg):

    try:
        texto = msg.payload.decode("utf-8")

        print(
            f">>> MENSAJE MQTT RECIBIDO: {texto}",
            flush=True
        )

        datos = json.loads(texto)

        movimiento = datos.get("movimiento")

        print(
            f">>> PIR movimiento = {movimiento}",
            flush=True
        )

    except Exception as error:

        print(
            f">>> ERROR PROCESANDO MQTT: {error}",
            flush=True
        )

        traceback.print_exc()


def iniciar_mqtt():

    print(
        ">>> INICIANDO HILO MQTT...",
        flush=True
    )

    try:

        cliente = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        cliente.on_connect = al_conectar
        cliente.on_message = al_recibir_mensaje

        print(
            f">>> CONECTANDO A {BROKER}:{PUERTO_MQTT}...",
            flush=True
        )

        cliente.connect(
            BROKER,
            PUERTO_MQTT,
            60
        )

        print(
            ">>> MQTT EN MODO ESCUCHA...",
            flush=True
        )

        cliente.loop_forever()

    except Exception as error:

        print(
            f">>> ERROR EN MQTT: {error}",
            flush=True
        )

        traceback.print_exc()


# ============================================================
# INICIO
# ============================================================

if __name__ == "__main__":

    print(
        ">>> INICIANDO SERVICIO FLASK + MQTT...",
        flush=True
    )

    hilo_mqtt = Thread(
        target=iniciar_mqtt,
        daemon=True
    )

    hilo_mqtt.start()

    print(
        ">>> HILO MQTT INICIADO",
        flush=True
    )

    puerto = int(
        os.environ.get("PORT", 5000)
    )

    print(
        f">>> FLASK INICIANDO EN PUERTO {puerto}",
        flush=True
    )

    app.run(
        host="0.0.0.0",
        port=puerto,
        debug=False,
        use_reloader=False
    )

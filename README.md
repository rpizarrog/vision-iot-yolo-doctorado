# Sistema IoT Inteligente con Visión Artificial y YOLO

Proyecto desarrollado como parte del curso de **Conectividad de Dispositivos y Sensores**.

El sistema integra sensores IoT, procesamiento mediante ESP32, lógica difusa, comunicación MQTT, visión artificial con YOLO y visualización mediante Node-RED desplegado en la nube.

## Objetivo

Desarrollar un sistema IoT inteligente capaz de detectar eventos de movimiento, analizar información proveniente de sensores y activar un módulo de visión artificial para identificar objetos mediante YOLO.

El sistema busca integrar diferentes niveles de procesamiento:

- Sensores IoT
- Procesamiento en el borde
- Lógica difusa
- Comunicación MQTT
- Visión artificial
- Reconocimiento de objetos con YOLO
- Dashboard de monitoreo
- Servicios desplegados en la nube

## Arquitectura general

```text
Sensores
   │
   ▼
ESP32 / MicroPython
   │
   ├── Temperatura
   ├── Humedad
   ├── Distancia
   ├── Luminosidad
   └── Movimiento PIR
   │
   ▼
Lógica Difusa
   │
   ▼
MQTT
   │
   ├─────────────────────────────► Node-RED
   │                                  │
   │                                  ▼
   │                              Dashboard
   │
   ▼
Receptor MQTT Python
   │
   ▼
Cámara simulada
   │
   ▼
YOLO11s
   │
   ▼
Detección de objetos
   │
   ▼
MQTT Visión
   │
   ▼
Node-RED en Render
   │
   ▼
Dashboard Web
```

## Funcionamiento del módulo de visión

El módulo de visión artificial permanece conectado al broker MQTT y escucha los mensajes generados por el sistema IoT.

Cuando el sensor PIR detecta una transición de:

```text
0 → 1
```

se considera el inicio de un nuevo evento de movimiento.

En ese momento el sistema:

1. Selecciona una imagen del catálogo de cámara simulada.
2. Procesa la imagen mediante YOLO11s.
3. Identifica los objetos presentes.
4. Obtiene la confianza de la detección.
5. Convierte la imagen a Base64.
6. Construye un mensaje JSON.
7. Publica el resultado mediante MQTT.
8. Node-RED recibe la información.
9. El Dashboard presenta la imagen, objeto y confianza.

## Estructura del proyecto

```text
vision_cloud/
│
├── app.py
├── CCamaraSimulada.py
├── CDetectorVision.py
├── CReceptorMQTT.py
├── inicio escucha MQTT.py
├── requirements.txt
├── yolo11s.pt
├── .gitignore
│
└── catalogo_camara/
    ├── aves/
    ├── gatos/
    ├── perros/
    ├── personas/
    └── varias/
```

## Descripción de los componentes

### `app.py`

Integra el servidor web Flask con el receptor MQTT.

Su propósito es permitir que el módulo de visión artificial pueda ejecutarse posteriormente como un servicio web en la nube, manteniendo simultáneamente la conexión MQTT.

### `CReceptorMQTT.py`

Implementa el cliente MQTT encargado de:

- conectarse al broker;
- suscribirse al tópico de sensores;
- recibir los mensajes enviados por el ESP32;
- detectar la transición del PIR de 0 a 1;
- activar la cámara simulada;
- ejecutar el detector YOLO;
- publicar los resultados de visión artificial.

### `CCamaraSimulada.py`

Simula el funcionamiento de una cámara.

Selecciona aleatoriamente una imagen disponible dentro de `catalogo_camara`.

Esto permite desarrollar y probar el sistema sin depender todavía de una cámara física.

### `CDetectorVision.py`

Implementa el modelo de visión artificial utilizando **Ultralytics YOLO11s**.

El modelo analiza la imagen seleccionada y devuelve información como:

```json
{
    "objeto": "person",
    "confianza": 0.8922
}
```

### `catalogo_camara`

Contiene las imágenes utilizadas para simular las capturas realizadas por una cámara.

El catálogo contiene diferentes tipos de objetos, entre ellos:

- personas;
- perros;
- gatos;
- aves;
- imágenes con múltiples objetos.

## MQTT

Broker utilizado:

```text
test.mosquitto.org
```

Tópico de sensores:

```text
doctorado/ruben/iot/deteccion
```

Tópico de visión artificial:

```text
doctorado/ruben/iot/vision
```

El ESP32 publica los datos de los sensores en el tópico de detección.

El módulo Python de visión artificial recibe estos mensajes y publica los resultados del reconocimiento en el tópico de visión.

## Ejemplo de resultado de visión

```json
{
    "imagen": "persona_034.jpg",
    "detecciones": [
        {
            "objeto": "person",
            "confianza": 0.8922
        }
    ]
}
```

La imagen también puede ser codificada en Base64 para enviarse mediante MQTT y visualizarse directamente en el Dashboard.

## Dashboard

Node-RED presenta información proveniente tanto de los sensores como del módulo de visión artificial.

Entre las variables mostradas se encuentran:

```text
Temperatura
Humedad
Distancia
Luminosidad
Movimiento PIR
Clasificación difusa
Estado de alarma
Imagen seleccionada
Objeto detectado
Confianza de YOLO
```

El Dashboard de Node-RED se encuentra desplegado mediante Docker en Render.

## Pruebas realizadas

Se comprobó exitosamente la integración:

```text
Wokwi
   ↓
ESP32
   ↓
MQTT
   ↓
Python
   ↓
YOLO11s
   ↓
MQTT Visión
   ↓
Node-RED Render Docker
   ↓
Dashboard Web
```

Entre las pruebas realizadas se obtuvieron detecciones como:

```text
Imagen: persona_034.jpg
Objeto: PERSON
Confianza: 89.22 %
```

y:

```text
Imagen: perro_020.jpg
Objeto: DOG
Confianza: 78.14 %
```

Estas pruebas confirmaron que el Dashboard desplegado en Render puede recibir y visualizar los resultados generados por el módulo Python de visión artificial.

## Dependencias

El archivo `requirements.txt` contiene:

```text
ultralytics==8.4.159
paho-mqtt
Flask
gunicorn
```

Las principales tecnologías utilizadas son:

- Python
- Flask
- Ultralytics
- YOLO11s
- Paho MQTT
- Mosquitto MQTT
- Node-RED
- Node-RED Dashboard 2.0
- Docker
- Render
- Git
- GitHub
- Wokwi
- ESP32
- MicroPython

## Ejecución local

Activar el entorno virtual desde la carpeta `vision_cloud`:

```powershell
..\.venv\Scripts\Activate.ps1
```

Ejecutar la aplicación:

```powershell
python app.py
```

El servidor Flask queda disponible localmente en:

```text
http://127.0.0.1:5000
```

Mientras Flask permanece activo, el receptor MQTT escucha los eventos provenientes del sistema IoT.

## Estado actual

Actualmente se ha validado:

- comunicación ESP32 → MQTT;
- lógica difusa;
- Node-RED desplegado mediante Docker en Render;
- Dashboard web;
- receptor MQTT en Python;
- cámara simulada;
- reconocimiento mediante YOLO11s;
- envío de imágenes mediante Base64;
- publicación de resultados mediante MQTT;
- integración Flask + MQTT + YOLO;
- recepción de los resultados de visión en Node-RED Render.

El siguiente objetivo es desplegar el módulo:

```text
Flask + MQTT + YOLO
```

en la nube para eliminar la dependencia de la computadora local durante la ejecución del sistema.

## Persistencia

El servicio Node-RED desplegado en Render utiliza un sistema de archivos efímero.

Por esta razón, los archivos generados durante la ejecución, como historiales CSV, pueden perderse cuando el contenedor se reinicia o reconstruye.

Los archivos esenciales para reconstruir el sistema deben mantenerse versionados en GitHub.

Como trabajo futuro se contempla utilizar almacenamiento persistente para conservar el historial de eventos IoT.

## Autor

**Rubén Pizarro Gurrola**

Proyecto académico  
Doctorado en Tecnologías de la Información  
2026
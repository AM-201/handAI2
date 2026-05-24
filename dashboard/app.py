from __future__ import annotations

import threading
import time

import cv2
import paho.mqtt.client as mqtt

from flask import Flask, Response, jsonify, render_template

app = Flask(__name__)

# Shared frame buffer
latest_frame = {
    "frame": None
}

frame_lock = threading.Lock()

# Dashboard state
dashboard_state = {
    "gesture": "",
    "mqtt_message": "",
    "esp32_status": "",
    "serial_logs": []
}

BROKER_ADDRESS = "10.56.74.139"  #change this to the same broker address as main.py

GESTURE_TOPIC = "handAI2/gesture"
ESP32_STATUS_TOPIC = "handAI2/esp32/status"
SERIAL_TOPIC = "handAI2/serial"


# ---------------- MQTT ---------------- #

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("Dashboard MQTT connected")

        client.subscribe(GESTURE_TOPIC)
        client.subscribe(ESP32_STATUS_TOPIC)
        client.subscribe(SERIAL_TOPIC)

    else:
        print(f"MQTT failed: {rc}")


def on_message(client, userdata, msg):

    payload = msg.payload.decode()

    if msg.topic == GESTURE_TOPIC:
        dashboard_state["gesture"] = payload
        dashboard_state["mqtt_message"] = payload

    elif msg.topic == ESP32_STATUS_TOPIC:
        dashboard_state["esp32_status"] = payload

    elif msg.topic == SERIAL_TOPIC:

        dashboard_state["serial_logs"].append(payload)

        # Keep last 20 logs only
        dashboard_state["serial_logs"] = dashboard_state["serial_logs"][-20:]


mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION1,
    client_id="DashboardClient"
)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(BROKER_ADDRESS, 1883, 60)
mqtt_client.loop_start()


# ---------------- VIDEO STREAM ----------------

def generate_frames():

    while True:

        with frame_lock:
            frame = latest_frame["frame"]

        if frame is None:
            time.sleep(0.01)
            continue

        success, buffer = cv2.imencode(".jpg", frame)

        if not success:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame_bytes +
            b"\r\n"
        )

        time.sleep(0.03)


@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ---------------- API ---------------- #

@app.route("/api/state")
def api_state():

    return jsonify(dashboard_state)


# ---------------- PAGE ---------------- #

@app.route("/")
def index():

    return render_template("index.html")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )
    
    
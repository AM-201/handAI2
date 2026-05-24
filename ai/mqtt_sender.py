from __future__ import annotations

import time
import paho.mqtt.client as mqtt


class MQTTSender:
    def __init__(self, broker_address, port: int = 1883, client_id: str = "PythonGesturePublisher"):
        self.broker_address = broker_address
        self.port = port
        self.client_id = client_id
        self.connected = False

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
            client_id=self.client_id,
            protocol=mqtt.MQTTv311,
        )
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected to MQTT broker.")
        else:
            self.connected = False
            print(f"Failed to connect to MQTT broker, return code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        print(f"Disconnected from MQTT broker with result code {rc}")

    def connect(self):
        try:
            self.client.connect(self.broker_address, self.port, keepalive=60)
            self.client.loop_start()

            # Give it a moment to complete the connection
            timeout = time.time() + 5
            while not self.connected and time.time() < timeout:
                time.sleep(0.05)

            if not self.connected:
                print("MQTT connection did not complete in time.")
                return False

            return True
        except Exception as e:
            print(f"Could not connect to MQTT broker: {e}")
            return False

    def publish(self, topic, message, retain: bool = False, qos: int = 0):
        if not self.connected:
            print("MQTT client not connected. Message not published.")
            return False

        info = self.client.publish(topic, message, qos=qos, retain=retain)
        if info.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Published to topic {topic}: {message}")
            return True

        print(f"Publish failed with code {info.rc}")
        return False

    def disconnect(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        finally:
            self.connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        
        
    
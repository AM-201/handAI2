from __future__ import annotations

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai.mqtt_sender import MQTTSender
from mqtt.topics import GESTURE_TOPIC, ESP32_STATUS_TOPIC, SERIAL_TOPIC


def main():
    # Change this to your broker IP if the broker is not on the same machine.
    broker = "127.0.0.1"

    with MQTTSender(broker, client_id="handAI2_test_sender") as sender:
        print("Sending test gestures...")

        sender.publish(GESTURE_TOPIC, "G", retain=False)
        time.sleep(1)

        sender.publish(GESTURE_TOPIC, "R", retain=False)
        time.sleep(1)

        sender.publish(GESTURE_TOPIC, "W", retain=False)
        time.sleep(1)

        print("Test complete.")
        print(f"Gesture topic: {GESTURE_TOPIC}")
        print(f"Status topic:  {ESP32_STATUS_TOPIC}")
        print(f"Serial topic:   {SERIAL_TOPIC}")


if __name__ == "__main__":
    main()
    
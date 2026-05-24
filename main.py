from __future__ import annotations

import threading
import time
import cv2

from ai.camera import Camera
from ai.hand_tracker import HandTracker
from ai.gesture_logic import GestureLogic
from ai.mqtt_sender import MQTTSender
from mqtt.topics import GESTURE_TOPIC

# Import Flask app objects
from dashboard.app import app, latest_frame, frame_lock

BROKER_ADDRESS = "10.56.74.139" #change ghis to youyr broker address

GESTURE_TO_MQTT = {
    "Open Hand": "G",
    "Closed Fist": "R",
    "Peace Sign": "W",
}


def run_flask():
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )


def main():

    print("Starting handAI2...")

    # Start Flask
    flask_thread = threading.Thread(
        target=run_flask,
        daemon=True
    )

    flask_thread.start()

    print("Dashboard started.")

    time.sleep(2)

    camera = Camera(
        camera_index=0,
        width=640,
        height=480,
        fps=30
    )

    camera.start()

    hand_tracker = HandTracker(max_num_hands=1)

    gesture_logic = GestureLogic(
        stability_threshold=5
    )

    mqtt_sender = MQTTSender(BROKER_ADDRESS)

    mqtt_sender.connect()

    print("System ready.")

    last_sent = None
    last_publish_time = 0
    publish_cooldown = 1.0

    while True:

        try:

            frame = camera.read_frame()

            frame = cv2.resize(frame, (640, 480))

            frame, results = hand_tracker.process_frame(frame)

            frame = hand_tracker.draw_landmarks(
                frame,
                results
            )

            hand_landmarks = hand_tracker.get_hand_landmarks(
                results
            )

            stable_gesture = gesture_logic.recognize_gesture(
                hand_landmarks
            )

            overlay_text = "Waiting..."

            if stable_gesture:

                mqtt_message = GESTURE_TO_MQTT.get(
                    stable_gesture
                )

                if mqtt_message:

                    current_time = time.time()

                    if (
                        mqtt_message != last_sent
                        or current_time - last_publish_time > publish_cooldown
                    ):

                        mqtt_sender.publish(
                            GESTURE_TOPIC,
                            mqtt_message,
                            retain=False
                        )

                        print(
                            f"{stable_gesture} -> {mqtt_message}"
                        )

                        last_sent = mqtt_message
                        last_publish_time = current_time

                    overlay_text = (
                        f"{stable_gesture} -> {mqtt_message}"
                    )

            cv2.putText(
                frame,
                overlay_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # SHARE FRAME
            with frame_lock:
                latest_frame["frame"] = frame.copy()

            time.sleep(0.01)

        except KeyboardInterrupt:
            break

        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(0.1)

    camera.release()
    mqtt_sender.disconnect()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    
    
#Done by A.M.A   :>
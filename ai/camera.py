from __future__ import annotations

import os
import cv2


class Camera:
    def __init__(self, camera_index: int = 0, width: int = 640, height: int = 480, fps: int = 30):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None

    def start(self):
        if self.cap is not None:
            return self

        # Windows: CAP_DSHOW is usually better
        # Linux: CAP_V4L2 is usually fine.
        if os.name == "nt":
            backend = cv2.CAP_DSHOW
        else:
            backend = cv2.CAP_V4L2

        self.cap = cv2.VideoCapture(self.camera_index, backend)

        if not self.cap.isOpened():
            # Fallback if backend selection fails
            self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            raise IOError(f"Could not open camera index {self.camera_index}")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        return self

    def read_frame(self):
        if self.cap is None:
            raise RuntimeError("Camera not started. Call start() first.")

        ok, frame = self.cap.read()
        if not ok or frame is None:
            raise IOError("Failed to read frame from camera.")
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        
        
from __future__ import annotations

import cv2
import mediapipe as mp


class HandTracker:
    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.6,
        min_tracking_confidence: float = 0.6,
    ):
        #this works best if u have mediapipe=0.10.9 or another version that still has mp.solutions
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def process_frame(self, frame):
        # Mirror view for webcam
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return frame, results

    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_hand_landmarks(self, results):
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0]
        return None

    def get_handedness(self, results):
        if results.multi_handedness:
            return results.multi_handedness[0].classification[0].label
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.hands.close()
        
from __future__ import annotations


class GestureLogic:
    """
    Rule-based gesture recognition for 3 gestures:
      - Open Hand
      - Closed Fist
      - Peace Sign
    """

    def __init__(self, stability_threshold: int = 5):
        self.stability_threshold = max(1, stability_threshold)
        self.candidate_gesture = ""
        self.candidate_count = 0
        self.stable_gesture = ""

    @staticmethod
    def _finger_up(lm, tip_idx: int, pip_idx: int) -> bool:
        # In image coordinates, smaller y = higher on the screen
        return lm[tip_idx].y < lm[pip_idx].y

    def _classify_raw(self, hand_landmarks) -> str:
        lm = hand_landmarks.landmark

        index_up = self._finger_up(lm, 8, 6)
        middle_up = self._finger_up(lm, 12, 10)
        ring_up = self._finger_up(lm, 16, 14)
        pinky_up = self._finger_up(lm, 20, 18)

        # rukes
        if index_up and middle_up and ring_up and pinky_up:
            return "Open Hand"

        if not index_up and not middle_up and not ring_up and not pinky_up:
            return "Closed Fist"

        if index_up and middle_up and not ring_up and not pinky_up:
            return "Peace Sign"

        return "Unknown"

    def _reset_state(self):
        self.candidate_gesture = ""
        self.candidate_count = 0
        self.stable_gesture = ""

    def recognize_gesture(self, hand_landmarks):
        if hand_landmarks is None:
            self._reset_state()
            return ""

        raw_gesture = self._classify_raw(hand_landmarks)

        if raw_gesture == "Unknown":
            # to stop spamming unknown.
            self.candidate_gesture = ""
            self.candidate_count = 0
            return ""

        if raw_gesture == self.candidate_gesture:
            self.candidate_count += 1
        else:
            self.candidate_gesture = raw_gesture
            self.candidate_count = 1

        # emit only when the gesture has become stable and is new
        if self.candidate_count >= self.stability_threshold and self.candidate_gesture != self.stable_gesture:
            self.stable_gesture = self.candidate_gesture
            return self.stable_gesture

        return ""
    
    
    
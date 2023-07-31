import cv2
from cv2 import COLOR_BGR2RGB
from mediapipe.python.solutions import drawing_utils, hands


class HandTracker:
    def __init__(
        self,
        image_mode: bool = False,
        max_hands: int = 2,
        model_comp: int = 1,
        detection_conf: float = 0.5,
        tracking_conf: float = 0.5
    ):
        self.hands = hands.Hands(
            image_mode, max_hands, model_comp, detection_conf, tracking_conf
        )
        self.draw = drawing_utils

    def hands_finder(self, image, draw: bool = True):
        image_rgb = cv2.cvtColor(image, COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        self.landmarks = results.multi_hand_landmarks
        if self.landmarks:
            for hand_lms in self.landmarks:
                if draw:
                    self.draw.draw_landmarks(
                        image, hand_lms, hands.HAND_CONNECTIONS
                    )
        return image

    def position_finder(self, image, hand_num: int = 0, draw: bool = True):
        lm_list = []
        if self.landmarks:
            hand = self.landmarks[hand_num]
            for id, lm in enumerate(hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

                if draw:
                    org = (cx, cy)
                    font = cv2.FONT_HERSHEY_COMPLEX
                    color = (255, 255, 255)
                    cv2.putText(image, str(id), org, font, 1, color, 1)
        return lm_list

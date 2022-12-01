import mediapipe as mp
import cv2

class Model:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
    
    def pre_process(self,image):
        processed_img = image.copy()
        processed_img = cv2.flip(processed_img,1)
        processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        return processed_img

    def predict(self,image):
        processed_img = self.pre_process(image)
        image_height, image_width, _ = processed_img.shape
        with self.mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
            results  = hands.process(processed_img)
            if(not results.multi_hand_landmarks):
                return

            hand_landmarks = results.multi_hand_landmarks[0]
            coords = {
                    "idx_x": hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width,
                    "idx_y": hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height,
                    "tmb_x": hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x * image_width,
                    "tmb_y": hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y * image_height
                    }

            #print(coords)
            return coords


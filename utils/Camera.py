import cv2
from . import HandModel
import pyautogui
import math

class VideoFeed:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.model = HandModel.Model()

    def process_frame(self, frame):
        coords = self.model.predict(frame)
        if(not coords):
            return cv2.flip(frame,1)
        processed_frame = self.draw_points(frame, coords)
        return processed_frame
 
    def draw_points(self, frame, coords):
        processed_frame = frame.copy()
        index_coords = (int(coords["idx_x"]),int(coords["idx_y"]))
        thumb_coords = (int(coords["tmb_x"]),int(coords["tmb_y"]))

        processed_frame = cv2.flip(processed_frame,1)
        processed_frame = cv2.circle(processed_frame, index_coords, radius=2, color=(0,0,255), thickness=-1)
        processed_frame = cv2.circle(processed_frame, thumb_coords, radius=2, color=(255,0,0), thickness=-1)

        dist_index2thumb = math.dist(index_coords, thumb_coords)
        processed_frame = cv2.putText(processed_frame, f"Dist: {round(dist_index2thumb,2)}", (20,20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1, cv2.LINE_AA)
        
        midpoint = (int((coords["idx_x"]+coords["tmb_x"])//2) , int((coords["idx_y"]+coords["tmb_y"])//2))
        
        processed_frame = cv2.circle(processed_frame, midpoint, radius=2, color=(0,0,0), thickness=-1)

        pyautogui.moveTo(100,100)

        return processed_frame

    def  start(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                continue

            frame.flags.writeable = False
            processed_frame = self.process_frame(frame)
            
            cv2.imshow("AirDraw", processed_frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    def __del__(self):
        self.cap.release()


if __name__ == "__main__":
    cam = VideoFeed()
    cam.start()


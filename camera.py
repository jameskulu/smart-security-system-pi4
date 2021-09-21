import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import pickle


with open('labels', 'rb') as f:
    dicti = pickle.load(f)
    f.close()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml") 
font = cv2.FONT_HERSHEY_SIMPLEX


class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_object(self, classifier):
        
        found_objects = False
        frame = self.flip_if_needed(self.vs.read()).copy() 
        ret, jpeg = cv2.imencode('.jpg', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in objects:
            roiGray = gray[y:y+h, x:x+w]

            id_, conf = recognizer.predict(roiGray)

            for name, value in dicti.items():
                if value == id_:
                    print("-----------------------------")

            if conf <= 70:
                found_objects = False

                # Draw a rectangle around the objects
                for (x, y, w, h) in objects:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                ret, jpeg = cv2.imencode('.jpg', frame)
                return (jpeg.tobytes(), found_objects)
            else:
                print("Unauthorized person detected !!!!")
                ret, jpeg = cv2.imencode('.jpg', frame)
                found_objects = True
                return (jpeg.tobytes(), found_objects)
        return (jpeg.tobytes(), found_objects)



        



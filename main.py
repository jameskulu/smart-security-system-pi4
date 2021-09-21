import cv2
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading
import RPi.GPIO as GPIO
from time import sleep

email_update_interval = 120  # sends an email only once in this time interval
# creates a camera object, flip vertically
video_camera = VideoCamera(flip=False)
object_classifier = cv2.CascadeClassifier(
    "models/facial_recognition_model.xml")  # an opencv classifier

# App Globals
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'james'
app.config['BASIC_AUTH_PASSWORD'] = 'james'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0


buzzerPIN = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(buzzerPIN, GPIO.OUT)


def check_for_objects():
    global last_epoch
    while True:
        try:
            frame, found_obj = video_camera.get_object(object_classifier)
            if found_obj and (time.time() - last_epoch) > email_update_interval:
                last_epoch = time.time()
                for i in range(3):
                    GPIO.output(buzzerPIN, GPIO.HIGH)
                    sleep(0.5)
                    GPIO.output(buzzerPIN, GPIO.LOW)
                    sleep(0.5)
                print("Sending email...")
                sendEmail(frame)
                print("done!")
        except Exception as e:
            print(e)


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)

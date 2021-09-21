# Home Security System Using Raspberry Pi 4

### Project Overview

IOT Raspberry Pi security camera running OpenCV for object detection. The camera will send an email with an image of any objects it detects an unauthorized person and buzzer will also be buzzed to alert the owner.

### Things used in this project

* Raspberry Pi 4
* Pi camera
* Buzzer
* Breadboard
* Jumper Wires


### How to use

First part is to install the dependencies using `pip3 install -r requirements.txt` command.

After that you need to create a `.env` file and add the information shown in `.env.example` file.

After the project initialization is completed you need to run certion command to run this application

First part is save the face of an authorized person. For that, you need to run some command as follows:

* Run command `python3 data_gathering.py` to store the images of an authorized person.
* Run command `python3 trainer.py` to create a labels for face detection. It will create two files (labels and trainer.xml)

After the face image storing part is done. We can now use the application to secure from an unauthorized person. For that you need to

* Run the command `python3 main.py` and go to `http://192.168.1.115:5000` this url in your browser to view the live security feed.

If the application detect an unauthorized person then the email messsage with the image of that person will be sent to the configured email and buzzer will be buzzed 3 times for an extra security.
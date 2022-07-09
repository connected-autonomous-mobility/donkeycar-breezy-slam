from re import I
import time
from donkeycar import Vehicle
from donkeycar.parts.cv import CvCam
from donkeycar.parts.camera import Webcam
from donkeycar.parts.tub_v2 import TubWriter
V = Vehicle()

IMAGE_W = 160
IMAGE_H = 120
IMAGE_DEPTH = 3

#Add a camera part
#cam = CvCam(image_w=IMAGE_W, image_h=IMAGE_H, image_d=IMAGE_DEPTH, iCam=0)
cam = Webcam(image_w=IMAGE_W, image_h=IMAGE_H, image_d=IMAGE_DEPTH,  framerate = 20, camera_index = 1)

V.add(cam, outputs=['image'], threaded=True)

#warmup camera
while cam.run() is None:
    time.sleep(1)

#add tub part to record images
tub = TubWriter(base_path='./mydata', inputs=['image'], types=['image_array'])
V.add(tub, inputs=['image'], outputs=['num_records'])

#start the drive loop at 10 Hz
V.start(rate_hz=10)
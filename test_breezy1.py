from re import I
import time
from donkeycar import Vehicle
#from donkeycar.parts.cv import CvCam
from donkeycar.parts.camera import Webcam
from donkeycar.parts.tub_v2 import TubWriter

# -----------------------------------------------------------------------------
# setting from lidar.py
# -----------------------------------------------------------------------------

import logging
import sys
import time
import math
import pickle
import serial
import numpy as np
from donkeycar.utils import norm_deg, dist, deg2rad, arr_to_img
from PIL import Image, ImageDraw

CLOCKWISE = 1
COUNTER_CLOCKWISE = -1

def limit_angle(angle):
    """
    make sure angle is 0 <= angle <= 360
    """
    while angle < 0:
        angle += 360
    while angle > 360:
        angle -= 360
    return angle


def angle_in_bounds(angle, min_angle, max_angle):
    """
    Determine if an angle is between two other angles.
    """
    if min_angle <= max_angle:
        return min_angle <= angle <= max_angle
    else:
        # If min_angle < max_angle then range crosses
        # zero degrees, so break up test
        # into two ranges
        return (min_angle <= angle <= 360) or (max_angle >= angle >= 0)

# -----------------------------------------------------------------------------
# 1 setup donkeycar pipeline
# -----------------------------------------------------------------------------

V = Vehicle()

IMAGE_W = 160
IMAGE_H = 120
IMAGE_DEPTH = 3

# -----------------------------------------------------------------------------
# 2 Add a camera part
# -----------------------------------------------------------------------------

#cam = CvCam(image_w=IMAGE_W, image_h=IMAGE_H, image_d=IMAGE_DEPTH, iCam=0)
cam = Webcam(image_w=IMAGE_W, image_h=IMAGE_H, image_d=IMAGE_DEPTH,  framerate = 20, camera_index = 1)

V.add(cam, outputs=['image'], threaded=True)

#warmup camera
while cam.run() is None:
    time.sleep(1)

# -----------------------------------------------------------------------------
# 3 add BreezySLAM part from lidar.py
# -----------------------------------------------------------------------------
# https://www.hackster.io/shahizat005/building-a-map-using-lidar-with-ros-melodic-on-jetson-nano-2f92dd
from donkeycar.parts.lidar import BreezySLAM, BreezyMap
breezy = BreezySLAM(MAP_SIZE_PIXELS=500, MAP_SIZE_METERS=10)

#add tub part to record images
tub = TubWriter(base_path='./mydata', inputs=['image'], types=['image_array'])
V.add(tub, inputs=['image'], outputs=['num_records'])

#start the drive loop at 10 Hz
V.start(rate_hz=10)
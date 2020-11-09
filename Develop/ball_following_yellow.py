from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

camera = PiCamera()
image_width = 640
image_height = 480
camera.resolution = (image_width, image_height)
camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(image_width, image_height))
center_image_x = image_width / 2
center_image_y = image_height / 2
minimum_area = 250
maximum_area = 100000

HUE_VAL = 29

lower_color = np.array([HUE_VAL - 10, 100, 100])
upper_color = np.array([HUE_VAL + 10, 255, 255])


def LocationOfObject():

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        color_mask = cv2.inRange(hsv, lower_color, upper_color)

        countours, _ = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        object_area = 0
        object_x = 0
        object_y = 0

        for contour in countours:

            x, y, width, height = cv2.boundingRect(contour)
            found_area = width * height
            center_x = x + (width / 2)
            center_y = y + (height / 2)

            if object_area < found_area:
                object_area = found_area
                object_x = center_x
                object_y = center_y

        if object_area > 0:
            yellow_object_location = [object_area, object_x, object_y]

        else:
            yellow_object_location = None

        if yellow_object_location:

            if (yellow_object_location[0] > minimum_area) and (yellow_object_location[0] < maximum_area):

                if yellow_object_location[1] > (center_image_x + (image_width/3)):
                    # print("Turning right")
                    rawCapture.truncate(0)
                    return "right"
                elif yellow_object_location[1] < (center_image_x - (image_width/3)):
                    # print("Turning left")
                    rawCapture.truncate(0)
                    return "left"
                else:
                    # print("Forward")
                    rawCapture.truncate(0)
                    return "forward"

            elif yellow_object_location[0] < minimum_area:
                # print("Target isn't large enough, searching")
                rawCapture.truncate(0)
                return "Target isn't large enough, searching"
            else:
                # print("Target large enough, stopping")
                rawCapture.truncate(0)
                return "Target large enough, stopping"
        else:
            # print("Target not found, searching")
            rawCapture.truncate(0)
            return "Target not found, searching"

    rawCapture.truncate(0)

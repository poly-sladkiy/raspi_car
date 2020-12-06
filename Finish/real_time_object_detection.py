from .Class_motors import *
from imutils.video import VideoStream
import numpy as np
import imutils
import cv2

# инициализация машины и запуск на движние
car = PiCar()
car.drive()

# load our serialized model from disk
print("[INFO] loading model...")

# file with the model and prototxt file, also confidence
prototxt = 'MobileNetSSD_deploy.prototxt.txt'
model = 'MobileNetSSD_deploy.caffemodel'
confidence = 0.6
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
(h, w) = (300, 400)

try:
    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # grab the frame dimensions and convert it to a blob

        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            conf = detections[0, 0, i, 2]
            idx = int(detections[0, 0, i, 1])
            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if (conf > confidence) and (idx == 15):
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                object_center = (endX - startX) // 2
                if object_center < (400 // 3):
                    car.left()
                elif (400 // 3) <= object_center <= (2 * 400 // 3):
                    car.forward()
                elif object_center > (400 // 3):
                    car.right()
                else:
                    car.stop()

                cv2.line(frame, (startX, startY), (endX, endY), (255, 255, 255))
                # cv2.rectangle(frame, (startX, startY), (endX, endY),
                #               (0, 255, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                break

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

finally:
    car.stop()
    car.clear_all()

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

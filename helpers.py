import cv2
import numpy as np


def captureBoard():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    # return frame[20:430, 110:510]
    return frame[40:410, 130:490]


def detectHand(img):
    img = img[:, 0:40]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 2, np.pi / 180, 400)
    if lines is None:
        return True
    else:
        return False

import cv2
import matplotlib.pyplot as plt


def captureBoard():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    return frame[40:410, 130:490]

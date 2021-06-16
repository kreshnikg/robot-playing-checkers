import cv2


def captureBoard():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    # return frame[20:430, 110:510]
    return frame[40:410, 130:490]

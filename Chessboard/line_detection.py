import cv2
import numpy as np
from time import sleep
import helpers

def detectLines(img):
    img = img[:, 0:40]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 2, np.pi / 180, 400)
    if lines is None:
        return None
    else:
        return True
    # for rho, theta in lines[0]:
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000 * (-b))
    #     y1 = int(y0 + 1000 * (a))
    #     x2 = int(x0 - 1000 * (-b))
    #     y2 = int(y0 - 1000 * (a))
    #
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # return True

# img = cv2.imread('../img/checkers_scanner_hand_1.jpg')
# img = cv2.imread('../img/checkers_scanner_pieces_2.jpg')



while True:
    img = helpers.captureBoard()
    lineDetected = detectLines(img)
    if lineDetected:
        print("Hand Not Detected!")
    else:
        print("Hand Detected!")
    # sleep(1)


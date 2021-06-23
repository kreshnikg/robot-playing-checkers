import cv2
import numpy as np
from matplotlib import pyplot as plt



# img = cv2.imread("../img/checkers_scanner_pieces_2.jpg")
#
# output = img.copy()
# output = cv2.bitwise_not(output)
# cv2.imshow('output', output)
cap = cv2.VideoCapture(1)
ret, img = cap.read()
img = img[40:410, 130:490]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
boardDimension = (7,7)
retval, corners = cv2.findChessboardCorners(img, boardDimension,0, 0)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
imgpoints = []  # 2d points in image plane.
count = 0
if retval == True:
    print(corners)
    cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    imgpoints.append(corners)
    # Draw and display the corners
    cv2.drawChessboardCorners(img, boardDimension, corners, retval)
    cv2.imshow('img', img)
    cv2.waitKey(0)
import cv2
import numpy as np
from matplotlib import pyplot as plt


# img = cv2.imread("img/coordination.jpg")
img = cv2.imread("../img/checkers_scanner_pieces_2.jpg")
# cap = cv2.VideoCapture(1)
# ret, img = cap.read()
# img = img[40:410, 130:490]

# img = cv2.flip(img, 0)

# cv2.imwrite("img/coordination.jpg", img)

# Reference point
# cv2.circle(img, (205, 207), 2, (0, 255, 0), 4)
cv2.circle(img, (30, 32), 2, (0, 255, 0), 4)
cv2.circle(img, (74, 31), 2, (0, 255, 0), 4)
cv2.circle(img, (117, 31), 2, (0, 255, 0), 4)
#
# cv2.circle(img, (345, 247), 2, (0, 255, 0), 4)

plt.imshow(img)
plt.show()

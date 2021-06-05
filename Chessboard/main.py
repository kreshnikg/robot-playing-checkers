import cv2
import numpy as np
from matplotlib import pyplot as plt


def getROIavgColor(frame, x, y, r):
    roi_values = frame[int(y - r / 2):int(y + r / 2), int(x - r / 2):int(x + r / 2)]
    avg = (np.mean(roi_values[:, :, 0]) + np.mean(roi_values[:, :, 1]) + np.mean(roi_values[:, :, 2])) / 3
    return avg

# cap = cv2.VideoCapture(1)
# ret, img = cap.read()
# img = img[40:410, 130:490]
img = cv2.imread("../img/checkers_scanner_pieces_2.jpg")

# img = cv2.imread("img/checkers_scanner.jpg")
# img = ~img
# img = cv2.resize(img, (800, 800))
# img = cv2.resize(img, (640, 480))

# ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

img = cv2.medianBlur(img, 5)
# img = img[30:435, 130:515]

output = img.copy()

height, width = img.shape[:2]
maxRadius = int(0.1 * width)
minRadius = int(0.02 * width)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(image=gray,
                           method=cv2.HOUGH_GRADIENT,
                           dp=1.5,
                           minDist=maxRadius,
                           param1=45,
                           param2=40,
                           minRadius=minRadius,
                           maxRadius=maxRadius)

if circles is not None:
    circlesRound = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circlesRound:
        avg = getROIavgColor(img, x, y, r)
        print(x, y)
        if avg >= 140:
            # White => green
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        else:
            # Black => red
            cv2.circle(output, (x, y), r, (255, 0, 0), 4)
    plt.imshow(output)
else:
    print('No circles found')

plt.show()

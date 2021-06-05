import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
print(frame)
plt.imshow(frame)
plt.show()
# frame = frame[40:410, 130:490]
# cv2.imwrite("../img/checkers_scanner_pieces_2.jpg", frame)

cap.release()
cv2.destroyAllWindows()

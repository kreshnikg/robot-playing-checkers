import Chessboard
import cv2
from matplotlib import pyplot as plt
import numpy as np

chb = Chessboard.Chessboard()

# cap = cv2.VideoCapture(1)
# ret, img = cap.read()
# img = img[40:410, 130:490]

img = cv2.imread("../img/checkers_scanner_pieces_2.jpg")

corners = Chessboard.detectBoardCorners(img)
pieces = chb.detectPieces(img)

# print("corners", corners)
print("pieces", pieces)

board = {}
letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
lastLetter = letters[0]
i = 0
for letter in letters:
    if letter != lastLetter:
        lastLetter = letter
        i = i + 1
    for number in numbers:
        if i % 2 == 0:
            if (number % 2) == 0:
                continue
        else:
            if (number % 2) > 0:
                continue
        board[letter + str(number)] = 0

print(board)

boardPieces = board.copy()

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (int(corners[0][0][0] / 2), int(corners[0][0][1] / 2))
fontScale = 0.5
fontColor = (255, 255, 255)
lineType = 2


def text(x, y, pos):
    color = tuple(np.random.choice(range(255), size=3))
    cv2.putText(img,
                pos,
                (x, y),
                font,
                fontScale,
                (int(color[0]), int(color[1]), int(color[2])),
                lineType)


# cv2.imshow("img",img)
# cv2.waitKey(0)

# (118, 26) =>

boardKeys = list(board.keys())


def appendPosition(x, y, pos):
    board[pos] = [x, y]
    cv2.circle(img, (x, y), 2, (0, 255, 0), 4)
    text(x, y, pos)


def getNextEmptyPos(skipPositions=0):
    for i in range(len(boardKeys)):
        if (board[boardKeys[i]]) == 0:
            return boardKeys[i + skipPositions]


for i in range(len(corners)):
    x, y = corners[i][0][0], corners[i][0][1]
    if i % 2 == 0:
        appendPosition(round(x - 22), round(y - 22), getNextEmptyPos())
        if (i >= 42) & (i < 48):
            appendPosition(round(x + 22), round(y + 22), getNextEmptyPos(3))
        if i == 48:
            appendPosition(round(x + 22), round(y + 22), getNextEmptyPos())
    else:
        if (i + 1) % 7 == 0:
            appendPosition(round(x + 22), round(y - 22), getNextEmptyPos())


plt.imshow(img)
plt.show()
print(board)


# check if piece is inside a position
def pointInCircle(point, circle, radius):
    # ((pointX - circleX)**2 + (pointY - circleY)**2) < radius**2
    return ((point[0] - circle[0]) ** 2 + (point[1] - circle[1]) ** 2) < radius ** 2

for boardKey in boardKeys:
    position = board[boardKey]
    for blackPiece in pieces["black"]:
        if pointInCircle(position, blackPiece, 6):
            boardPieces[boardKey] = -1

    for whitePiece in pieces["white"]:
        if pointInCircle(position, whitePiece, 6):
            boardPieces[boardKey] = 1

print(boardPieces)
